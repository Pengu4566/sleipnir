import os
import pandas as pd
import zipfile
from werkzeug.utils import secure_filename
import shutil
import time
from random import randint
from datetime import timedelta
import tempfile
import sys
from elasticsearch import Elasticsearch
##
##
# dataframes
from dataframes import dataframe
# functions
from grading_checks import naming, usage, documentation_logging, error_handling
from soft_checks import activity_stats, project_folder_structure, project_structure

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit

es = Elasticsearch(['https://098b8510b627461cb0e77d37d10c4511.us-east-1.aws.found.io:9243'],
                   http_auth=('elastic', '5mKdXBb77D2hLuukmTHwThkc'))
application = app = Flask(__name__, static_folder='./static/dist', template_folder="./static")

# dont save cache in web browser (updating results image correctly)
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_PATH'] = '/file/'
app.config['ALLOWED_EXTENSIONS'] = set(['zip'])
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SECRET_KEY'] = randint(0,99999999999999999999)

# Check Configuration section for more details
Session(app)
socketio = SocketIO(app, async_mode="eventlet")
thread = None

######
gexf = ''
df_annotation = []
main_location = ""
dict_score = {}
df_invokeWf = []

######


@app.route('/')
def upload():
    with app.app_context():
        return render_template('fileUpload.html')


def background_thread():
    while True:
        socketio.emit('message', {'alive': "Alive"})
        socketio.sleep(60)


@socketio.on('connect')
def connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)


@app.route("/uploader", methods=['GET', 'POST'])
def handle_upload():

    if request.method == 'POST':
        socketio.emit('progress', {'data': str(request.remote_addr)})
        socketio.sleep(0.1)

        socketio.emit('progress', {'data': 'Getting Check Info ...'})
        socketio.sleep(0.1)

        # get checks info
        def get_checks_info(ele_lst_info):
            return True if request.form.get(ele_lst_info) == ele_lst_info else False
        lst_info = ['Naming', 'VariableNaming', 'ArgumentNaming', 'ActivityNaming',
                    'Usage', 'VariableUsage', 'ArgumentUsage',
                    'Documentation', 'WorkflowAnnotation', 'TryCatchLogging', 'TryCatchScreenshot', 'JsonLogging', 'ArgExpAnnot']
        start = time.time()
        [session['naming'], session['varNaming'], session['argNaming'], session['actNaming'],
         session['usage'], session['varUsage'], session['argUsage'],
         session['documentation'], session['wfAnnot'], session['tcLog'], session['tcSs'], session['jsonLog'], session['arginAnnot']] = map(get_checks_info,lst_info)
        print('Get checks info takes %s seconds' % (time.time() - start))
        # check if the post request has the file part
        socketio.emit('progress', {'data': 'Getting File Info ...'})
        socketio.sleep(0.1)

        if ('file' not in request.files) or (request.files['file'].filename == ''):
            return "You must pick a file! Use your browser's back button and try again."
        file = request.files['file']

        def allowed_file(file_name):
            return '.' in file_name and file_name.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

        if not allowed_file(file.filename):
            with app.app_context():
                return render_template("wrongFile.html")
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename).replace("\\", "/")

            # save, unzip, and remove zip
            socketio.emit('progress', {'data': 'Saving File ...'})
            socketio.sleep(0.1)
            generatedFileNaming = filename[:-4] + str(time.time()).replace(".", "") +\
                                  str(randint(1, 999999999999)) + ".zip"
            if os.path.isfile(os.getcwd() + app.config['UPLOAD_PATH'] + generatedFileNaming):
                nameDup = True
                while nameDup:
                    generatedFileNaming = filename[:-4] + str(time.time()).replace(".", "") +\
                                          str(randint(1, 999999999999)) + ".zip"
                    nameDup = os.path.isfile(os.getcwd() + app.config['UPLOAD_PATH'] + generatedFileNaming)
            file.save((os.getcwd() + app.config['UPLOAD_PATH'] + generatedFileNaming).replace("\\", "/"))
            generatedFolderName = filename[:-4] + str(time.time()).replace(".", "") + str(randint(1, 999999999999))

            if os.path.isdir((os.getcwd() + app.config['UPLOAD_PATH'] + generatedFolderName).replace("\\", "/")):
                folderExist = True
                while folderExist:
                    generatedFolderName = filename[:-4] + str(time.time()).replace(".", "") +\
                                          str(randint(1, 999999999999))
                    folderExist = os.path.isdir((os.getcwd() + app.config['UPLOAD_PATH'] +
                                                 generatedFolderName).replace("\\", "/"))

            folderPath = (os.getcwd() + app.config['UPLOAD_PATH'] + generatedFolderName).replace("\\", "/")

            socketio.emit('progress', {'data': 'Unzipping ...'})
            socketio.sleep(0.1)
            start = time.time()

            zipFile = zipfile.ZipFile((os.getcwd() + app.config['UPLOAD_PATH'] + generatedFileNaming).replace("\\", "/"))
            zipFile.extractall(folderPath)
            zipFile.close()

            print('Unzipping takes %s seconds' % (time.time() - start))

            os.remove((os.getcwd() + app.config['UPLOAD_PATH'] + generatedFileNaming).replace("\\", "/"))
            session['folderPath'] = folderPath

            ##########################################################################################################
            global gexf
            # file processing
            files = []
            start = time.time()
            for r, d, f in os.walk(folderPath):
                for file in f:
                    if '.xaml' in file:
                        files.append(os.path.join(r, file).replace("\\", "/"))
            print('Get list of all xaml files takes %s seconds' % (time.time() - start))
            fileLocationStr = (os.getcwd() + app.config['UPLOAD_PATH'] + generatedFolderName).replace("\\", "/") + "/"
            for r, d, f in os.walk(folderPath):
                if len(d) == 1:
                    fileLocationStr = r.replace("\\","/") + "/" + d[0] + "/"
                else:
                    break
            session['fileLocationStr'] = fileLocationStr
            session['files'] = files
            # checks for empty files list, program should end if this gets triggered
            if (files == []):
                return "Could not find project files! Did you put them in the right place?"
            else:
                return redirect(url_for('processing'))


@app.route("/processing")
def processing():

    # Get related info from Project.json (name and description)
    folderPath = session.get('folderPath')
    fileLocationStr = session.get('fileLocationStr')
    files = session.get('files')

    df_json = documentation_logging.grade_project_json_name_desc(folderPath)
    if session.get('jsonLog'):
        project_detail = list(df_json.copy().reset_index().loc[:, ['index', 'projectDetail']].T.to_dict().values())
        json_name_score = df_json.namingScore.sum() / len(df_json.namingScore)
        json_description_score = df_json.descriptionScore.sum() / len(df_json.descriptionScore)
    else:
        json_name_score = "[Not evaluated]"
        json_description_score = "[Not evaluated]"
        project_detail = ['Not evaluated']

    # scans all project files and populates dataframes with relevant info
    socketio.emit('progress', {'data': 'Processing Files ...'})
    socketio.sleep(0.1)

    start = time.time()
    lst_sub_df = [dataframe.populate_dataframe(files[i], df_json) for i in range(len(files))]
    print('Generate all takes %s secondss' % (time.time() - start))
    df_variable = pd.concat([x[0] for x in lst_sub_df], ignore_index=True).drop_duplicates(inplace=False)
    df_argument = pd.concat([x[1] for x in lst_sub_df], ignore_index=True).drop_duplicates(inplace=False)
    df_catches = pd.concat([x[2] for x in lst_sub_df], ignore_index=True).drop_duplicates(inplace=False)
    df_activity = pd.concat([x[3] for x in lst_sub_df], ignore_index=True).drop_duplicates(inplace=False)
    df_annotation = pd.concat([x[4] for x in lst_sub_df], ignore_index=True).drop_duplicates(inplace=False)

    dict_score = {}
    # level 1: grading checks

    # level 2: name
    if session.get("naming"):
        # level 3: variable naming
        if session.get('varNaming'):
            [variableNamingScore, improperNamedVariable] = naming.grade_variable_name(df_variable=df_variable,
                                                                                      fileLocationStr=fileLocationStr)
            improperNamedVar = improperNamedVariable
        else:
            improperNamedVar = ['Not evaluated']
            variableNamingScore = "[Not evaluated]"

        # level 3: argument naming
        if session.get('argNaming'):
            [argumentNamingScore, improperNamedArguments] = naming.grade_argument_name(df_argument=df_argument,
                                                                                       fileLocationStr=fileLocationStr)
            improperNamedArg = improperNamedArguments
        else:
            improperNamedArg = ['Not evaluated']
            argumentNamingScore = "[Not evaluated]"

        # level 3: activity naming
        if session['actNaming']:
            [activityNamingScore, improperNamedActivities] = naming.grade_activity_name(df_activity=df_activity,
                                                                                        fileLocationStr=fileLocationStr)
            improperNamedAct = improperNamedActivities
        else:
            improperNamedAct = ['Not evaluated']
            activityNamingScore = "[Not evaluated]"

        lt_namingScore = [variableNamingScore, argumentNamingScore, activityNamingScore]
        namingScore = 0
        count = 0
        for i in lt_namingScore:
            if i != "[Not evaluated]":
                namingScore += i
                count += 1
        namingScore = int(namingScore / count)

    else:
        improperNamedVar = ['Not evaluated']
        improperNamedArg = ['Not evaluated']
        improperNamedAct = ['Not evaluated']
        namingScore = "[Not evaluated]"

    dict_score['naming'] = namingScore

    # level 2: usage
    if session["usage"]:
        # level 3: variable usage
        if session['varUsage']:
            [variableUsageScore, unusedVariable] = usage.grade_variable_usage(df_variable=df_variable,
                                                                              fileLocationStr=fileLocationStr)
            unusedVar = unusedVariable
        else:
            unusedVar = ['Not evaluated']
            variableUsageScore = "[Not evaluated]"

        # level 3: argument usage
        if session['argUsage']:
            [argumentUsageScore, unusedArgument] = usage.grade_argument_usage(df_argument=df_argument,
                                                                              fileLocationStr=fileLocationStr)
            unusedArgument = unusedArgument
        else:
            unusedArgument = ['Not evaluated']
            argumentUsageScore = "[Not evaluated]"

        # level 2: usage score
        lt_usageScore = [variableUsageScore, argumentUsageScore]
        usageScore = 0
        count = 0
        for i in lt_usageScore:
            if i != "[Not evaluated]":
                usageScore += i
                count += 1
        usageScore = int(usageScore / count)

    else:
        unusedVar = ['Not evaluated']
        unusedArgument = ['Not evaluated']
        usageScore = "[Not evaluated]"

    dict_score['usage'] = usageScore

    # level 2: documentation_logging
    if session["documentation"]:

        # level 3: log message in catches
        if session['tcLog']:
            [logMessageScore, noLMException] = documentation_logging.grade_log_message_in_catches(
                df_catches=df_catches, fileLocationStr=fileLocationStr)

            noLMExp = noLMException
        else:
            logMessageScore = "[Not evaluated]"
            noLMExp = ['Not evaluated']

        # level 3: screenshot in catches
        if session['tcSs']:
            [screenshotScore, noSsException] = documentation_logging.grade_screenshot_in_catches(
                df_catches=df_catches, fileLocationStr=fileLocationStr)
            noSsExp = noSsException
        else:
            screenshotScore = "[Not evaluated]"
            noSsExp = ['Not evaluated']

        # level 3: workflow annotation
        [wfAnnotationScore, notAnnotatedWf, AnnotationArgumentScore, missing_arguments_list] =\
            documentation_logging.grade_annotation_in_workflow(df_annotation=df_annotation,
                                                               fileLocationStr=fileLocationStr,
                                                               df_argument=df_argument)
        if session['wfAnnot']:
            notAnnotWf = notAnnotatedWf
        else:
            wfAnnotationScore = "[Not evaluated]"
            notAnnotWf = ['Not evaluated']

        # level 3: Arguments should be at least mentioned in annotation
        # outputs a percentage score of the number of correct arguments and a list of missing arguments
        if session['arginAnnot']:
            missing_arguments_list = missing_arguments_list
        else:
            missing_arguments_list = ['Not evaluated']
            AnnotationArgumentScore = "[Not evaluated]"

        # level 3: Comments
        # commentScore = documentation_logging.grade_comments(df_annotation=df_annotation)

        # level 2: documentation_logging score
        lt_docScore = [wfAnnotationScore, logMessageScore, screenshotScore, json_name_score,
                       json_description_score, AnnotationArgumentScore]
        docScore = 0
        count = 0
        for i in lt_docScore:
            if i != "[Not evaluated]":
                docScore += i
                count += 1
        docScore = int(docScore / count)

    else:
        noSsExp = ['Not evaluated']
        notAnnotWf = ['Not evaluated']
        noLMExp = ['Not evaluated']
        missing_arguments_list = ['Not evaluated']
        project_detail = ['Not evaluated']
        docScore = "[Not evaluated]"

    dict_score['documentation'] = docScore

    # establish score list and name list
    dict_tolerance = {'naming': 90, 'usage': 90, 'documentation': 100}
    lst_score = []
    lst_tolerance = []
    lst_checkName = []
    for checks in ['naming', 'usage', 'documentation']:
        if session[checks]:
            lst_score.append(dict_score[checks])
            lst_tolerance.append(dict_tolerance[checks])
            lst_checkName.append(checks.capitalize())

    # level 1: soft checks
    # level 2: activity stats
    activityStats = activity_stats.get_activity_stats(df_activity=df_activity, fileLocationStr=fileLocationStr,
                                                      df_json=df_json, df_annotation=df_annotation)
    # level 2: folder structure
    folderStructure = project_folder_structure.list_files(fileLocationStr=fileLocationStr)
    # level 2: project structure
    gexf = project_structure.generate_gexf(df_annotation=df_annotation, fileLocationStr=fileLocationStr)

    # pass along the variables
    session['namingScore'] = namingScore
    session['usageScore'] = usageScore
    session['docScore'] = docScore
    session['improperNamedVar'] = improperNamedVar
    session['unusedVar'] = unusedVar
    session['improperNamedArg'] = improperNamedArg
    session['improperNamedAct'] = improperNamedAct
    session['activityStats'] = activityStats
    session['noSsExp'] = noSsExp
    session['notAnnotWf'] = notAnnotWf
    session['noLMExp'] = noLMExp
    session['project_detail'] = project_detail
    session['missing_arguments_list'] = missing_arguments_list
    session['folderStructure'] = folderStructure
    session['unusedArgument'] = unusedArgument
    session['gexf'] = gexf

    ##########################################################################################################

    return redirect(url_for('.__main__'))


@app.route("/analyze")
def __main__():

    with app.app_context():
        # clear out content in file folder
        shutil.rmtree(session.get("folderPath"))

        return render_template('index.html',
                               namingScore=session.get("namingScore"),
                               usageScore=session.get("usageScore"),
                               docScore=session.get("docScore"),
                               improperNamedVar={"data": session.get("improperNamedVar")},
                               unusedVar={"data": session.get("unusedVar")},
                               improperNamedArg={"data": session.get("improperNamedArg")},
                               improperNamedAct={"data": session.get("improperNamedAct")},
                               activityStats={"data": session.get("activityStats")},
                               noSsExp={"data": session.get("noSsExp")},
                               notAnnotWf={"data": session.get("notAnnotWf")},
                               noLMExp={"data": session.get("noLMExp")},
                               project_detail={"data": session.get("project_detail")},
                               missing_arguments_list={"data": session.get("missing_arguments_list")},
                               folderStructure=session.get("folderStructure"),
                               unusedArgument={"data": session.get("unusedArgument")})


@app.route("/retry")
def delete_pics():
    with app.app_context():
        return redirect(url_for('upload'))


@app.route("/elastic")
def send_data():
    ipAddress = request.remote_addr
    body = {
        'namingScore': session.get("namingScore"),
        'usageScore': session.get("usageScore"),
        'docScore': session.get("docScore"),
        'improperNamedVar': session.get("improperNamedVar"),
        'unusedVar': session.get("unusedVar"),
        'improperNamedArg': session.get("improperNamedArg"),
        'improperNamedAct': session.get("improperNamedAct"),
        'activityStats': session.get("activityStats"),
        'noSsExp': session.get("noSsExp"),
        'notAnnotWf': session.get("notAnnotWf"),
        'noLMExp': session.get("noLMExp"),
        'project_detail': session.get("project_detail"),
        'missing_arguments_list': session.get("missing_arguments_list"),
        'unusedArgument': session.get("unusedArgument")
    }

    id = str(ipAddress)+'-'+str(time.time()).split('.')[0]

    result = es.index(index='sleipnirdb', doc_type='projectdata', id=id, body=body)

    return jsonify(result)


# echarts graphs go here
@app.route("/radar", methods=['GET'])
def radar_plot_data():
    message = {'usage': session.get("usageScore"),
               'documentation': session.get("docScore"),
               'naming': session.get("namingScore")}
    return jsonify(message)


@app.route("/structure", methods=['GET'])
def project_structure_data():
    message = {'gexf': session.get("gexf")}
    return jsonify(message)

@app.route("/file_tree_map", methods=['GET'])
def tree_map():
    projectPath = session.get('fileLocationStr')
    fileTreeJson = project_folder_structure.list_files_json(projectPath)

    print("the json string is: " + str(fileTreeJson))

    return fileTreeJson

# only run when executing locally
if __name__ == "__main__":
    socketio.run(app, debug=True)
    upload()
