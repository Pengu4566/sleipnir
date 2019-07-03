import os
import pandas as pd
import zipfile
from werkzeug.utils import secure_filename
import shutil
import time
from random import randint
from datetime import datetime, timedelta
import eventlet
import tempfile
import sys
##
##
# dataframes
from dataframes import variable_dataframe, argument_dataframe, activity_dataframe, catch_dataframe, annotation_dataframe

# functions
from grading_checks import naming, usage, documentation_logging, error_handling
from soft_checks import activity_stats, project_folder_structure, project_structure

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit


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
        socketio.emit('message', {'alive': "test"}, namespace="/")
        socketio.sleep(0)
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

        socketio.emit('progress', {'data': 'Uploading ...'})
        socketio.sleep(0)

        # get value of checkboxes
        session['naming'] = False
        session['varNaming'] = False
        session['argNaming'] = False
        session['actNaming'] = False

        session['usage'] = False
        session['varUsage'] = False
        session['argUsage'] = False

        session['documentation'] = False
        session['wfAnnot'] = False
        session['tcLog'] = False
        session['tcSs'] = False
        session['jsonLog'] = False
        session['arginAnnot'] = False

        # naming
        if request.form.get('Naming') == "Naming":
            session['naming'] = True

        if request.form.get('VariableNaming') == "VariableNaming":
            session['varNaming'] = True

        if request.form.get('ArgumentNaming') == "ArgumentNaming":
            session['argNaming'] = True

        if request.form.get('ActivityNaming') == "ActivityNaming":
            session['actNaming'] = True


        # usage
        if request.form.get('Usage') == "Usage":
            session['usage'] = True

        if request.form.get('VariableUsage') == "VariableUsage":
            session['varUsage'] = True

        if request.form.get('ArgumentUsage') == "ArgumentUsage":
            session['argUsage'] = True


        # documentation
        if request.form.get('Documentation') == "Documentation":
            session['documentation'] = True

        if request.form.get('WorkflowAnnotation') == "WorkflowAnnotation":
            session['wfAnnot'] = True

        if request.form.get('TryCatchLogging') == "TryCatchLogging":
            session['tcLog'] = True

        if request.form.get('TryCatchScreenshot') == "TryCatchScreenshot":
            session['tcSs'] = True

        if request.form.get('JsonLogging') == "JsonLogging":
            session['jsonLog'] = True

        if request.form.get('ArgExpAnnot') == "ArgExpAnnot":
            session['arginAnnot'] = True

        # check if the post request has the file part
        if 'file' not in request.files:
            return "You must pick a file! Use your browser's back button and try again."
        file = request.files['file']
        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            return'No selected file'

        def allowed_file(file_name):
            return '.' in file_name and file_name.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

        if not allowed_file(file.filename):
            with app.app_context():
                return render_template("wrongFile.html")
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = filename.replace("\\", "/")

            # save, unzip, and remove zip
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

            socketio.emit('progress', {'data': 'Unzipping ...'})
            socketio.sleep(0)

            folderPath = (os.getcwd() + app.config['UPLOAD_PATH'] + generatedFolderName).replace("\\", "/")
            zipFile = zipfile.ZipFile((os.getcwd() + app.config['UPLOAD_PATH'] +
                                       generatedFileNaming).replace("\\", "/"))


            zipFile.extractall(folderPath)

            zipFile.close()
            os.remove((os.getcwd() + app.config['UPLOAD_PATH'] + generatedFileNaming).replace("\\", "/"))
            session['folderPath'] = folderPath
            fileLocationStr = folderPath + "/" + filename[:-4] + "/"

            ##########################################################################################################
            global gexf
            # file processing
            files = []

            for r, d, f in os.walk(folderPath):
                for file in f:
                    if '.xaml' in file:
                        files.append(os.path.join(r, file).replace("\\", "/"))


            # checks for empty files list, program should end if this gets triggered
            if (files == []):
                return "Could not find project files! Did you put them in the right place?"



            # scans all project files and populates dataframes with relevant info
            # variables dataframe
            socketio.emit('progress', {'data': 'Processing Files ...'})
            socketio.sleep(0)

            # variables dataframe
            socketio.emit('progress', {'data': 'Step 1 ...'})
            socketio.sleep(0)
            lst_sub_df_variable = list(map(variable_dataframe.populate_variables_dataframe, files))
            df_variable = pd.concat(lst_sub_df_variable, ignore_index=True)

            # argument dataframe
            socketio.emit('progress', {'data': 'Step 2 ...'})
            socketio.sleep(0)
            lst_sub_df_argument = list(map(argument_dataframe.populate_argument_dataframe, files))
            df_argument = pd.concat(lst_sub_df_argument, ignore_index=True)

            # activity dataframe
            socketio.emit('progress', {'data': 'Step 3 ...'})
            socketio.sleep(0)
            lst_sub_df_activity = list(map(activity_dataframe.populate_activity_dataframe, files))
            df_activity = pd.concat(lst_sub_df_activity, ignore_index=True)

            # annotation dataframe
            socketio.emit('progress', {'data': 'Step 4 ...'})
            socketio.sleep(0)
            lst_sub_df_annotation = list(map(annotation_dataframe.populate_annotation_dataframe, files))
            df_annotation = pd.concat(lst_sub_df_annotation, ignore_index=True)

            # try catch dataframe
            socketio.emit('progress', {'data': 'Step 5 ...'})
            socketio.sleep(0)
            lst_sub_df_catch = list(map(catch_dataframe.populate_catch_dataframe, files))
            df_catches = pd.concat(lst_sub_df_catch, ignore_index=True)

            socketio.emit('progress', {'data': 'Processing Files Finished. Start Analyzing ...'})
            socketio.sleep(0)

            dict_score = {}
            # level 1: grading checks

            # level 2: name
            if session["naming"]:
                # level 3: variable naming
                if session['varNaming']:
                    [variableNamingScore, improperNamedVariable] = naming.grade_variable_name(df_variable)
                    improperNamedVar = str(improperNamedVariable).replace("'", "")
                else:
                    improperNamedVar = "[Not evaluated]"
                    variableNamingScore = "[Not evaluated]"

                # level 3: argument naming
                if session['argNaming']:
                    [argumentNamingScore, improperNamedArguments] = naming.grade_argument_name(df_argument)
                    improperNamedArg = str(improperNamedArguments).replace("'", "")
                else:
                    improperNamedArg = "[Not evaluated]"
                    argumentNamingScore = "[Not evaluated]"

                # level 3: activity naming
                if session['actNaming']:
                    [activityNamingScore, improperNamedActivities] = naming.grade_activity_name(df_activity)
                    improperNamedAct = str(improperNamedActivities).replace("'", "")
                else:
                    improperNamedAct = "[Not evaluated]"
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
                improperNamedVar = "[Not evaluated]"
                improperNamedArg = "[Not evaluated]"
                improperNamedAct = "[Not evaluated]"
                namingScore = "[Not evaluated]"

            dict_score['naming'] = namingScore

            # level 2: usage
            if session["usage"]:
                # level 3: variable usage
                if session['varUsage']:
                    [variableUsageScore, unusedVariable] = usage.grade_variable_usage(df_variable)
                    unusedVar = str(unusedVariable).replace("'", "")
                else:
                    unusedVar = "[Not evaluated]"
                    variableUsageScore = "[Not evaluated]"

                # level 3: argument usage
                if session['argUsage']:
                    [argumentUsageScore, unusedArgument] = usage.grade_argument_usage(df_argument)
                    unusedArgument = str(unusedArgument).replace("'", "")
                else:
                    unusedArgument = "[Not evaluated]"
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
                unusedVar = "[Not evaluated]"
                unusedArgument = "[Not evaluated]"
                usageScore = "[Not evaluated]"

            dict_score['usage'] = usageScore

            # level 2: documentation_logging
            if session["documentation"]:

                # level 3: log message in catches
                if session['tcLog']:
                    [logMessageScore, noLMException] = documentation_logging.grade_log_message_in_catches(
                        df_catches=df_catches)

                    noLMExp = str(noLMException).replace("'", "")
                else:
                    logMessageScore = "[Not evaluated]"
                    noLMExp = "[Not evaluated]"

                # level 3: screenshot in catches
                if session['tcSs']:
                    [screenshotScore, noSsException] = documentation_logging.grade_screenshot_in_catches(
                        df_catches=df_catches)
                    noSsExp = str(noSsException).replace("'", "")
                else:
                    screenshotScore = "[Not evaluated]"
                    noSsExp = "[Not evaluated]"

                # level 3: Project.json (name and description)
                if session['jsonLog']:
                    [json_name_score, json_description_score, project_detail, main_location] = \
                        documentation_logging.grade_project_json_name_desc(folderPath)
                    project_detail = str(project_detail).replace("'", "")
                else:
                    json_name_score = "[Not evaluated]"
                    json_description_score = "[Not evaluated]"
                    project_detail = "[Not evaluated]"

                # level 3: workflow annotation
                [wfAnnotationScore, notAnnotatedWf] = documentation_logging.grade_annotation_in_workflow(
                    df_annotation=df_annotation,
                    main_location=main_location)
                if session['wfAnnot']:
                    notAnnotWf = str(notAnnotatedWf).replace("'", "")
                else:
                    wfAnnotationScore = "[Not evaluated]"
                    notAnnotWf = "[Not evaluated]"

                # level 3: Arguments should be at least mentioned in annotation
                # outputs a percentage score of the number of correct arguments and a list of missing arguments
                if session['arginAnnot']:
                    [AnnotationArgumentScore, missing_arguments_list] = \
                        documentation_logging.grade_annotation_contains_arguments(df_annotation=df_annotation,
                                                                                  main_location=main_location)
                    missing_arguments_list = str(missing_arguments_list).replace("'", "")
                else:
                    missing_arguments_list = "[Not evaluated]"
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
                noSsExp = "[Not evaluated]"
                notAnnotWf = "[Not evaluated]"
                noLMExp = "[Not evaluated]"
                missing_arguments_list = "[Not evaluated]"
                project_detail = "[Not evaluated]"
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
            activityStats = activity_stats.get_activity_stats(df_activity=df_activity)
            # level 2: folder structure
            folderStructure = project_folder_structure.list_files(main_location=main_location)
            # level 2: project structure
            main_location = documentation_logging.grade_project_json_name_desc(folderPath)[3]
            gexf = project_structure.generate_gexf(df_annotation=df_annotation, fileLocationStr=fileLocationStr)
            # generate project structure dataframe (echarts)
            # str_replace = main_location + "/"
            # df_annotation['workflowName'] = df_annotation['workflowName'].str.replace(str_replace, "")
            # df_annotation['invokedBy'] = df_annotation['invokedBy'].str.replace(str_replace, "")
            # # Create tree object
            # df_invokeWf = df_annotation.loc[:, ['workflowName', 'invokedBy']].drop_duplicates()


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
                               improperNamedVar=session.get("improperNamedVar"),
                               unusedVar=session.get("unusedVar"),
                               improperNamedArg=session.get("improperNamedArg"),
                               improperNamedAct=session.get("improperNamedAct"),
                               activityStats=session.get("activityStats"),
                               noSsExp=session.get("noSsExp"),
                               notAnnotWf=session.get("notAnnotWf"),
                               noLMExp=session.get("noLMExp"),
                               project_detail=session.get("project_detail"),
                               missing_arguments_list=session.get("missing_arguments_list"),
                               folderStructure=session.get("folderStructure"),
                               unusedArgument=session.get("unusedArgument"))

                               # namingScore=namingScore,
                               # usageScore=usageScore,
                               # docScore=docScore,
                               # improperNamedVar=improperNamedVar,
                               # unusedVar=unusedVar,
                               # improperNamedArg=improperNamedArg,
                               # improperNamedAct=improperNamedAct,
                               # activityStats=activityStats,
                               # noSsExp=noSsExp,
                               # notAnnotWf=notAnnotWf,
                               # noLMExp=noLMExp,
                               # project_detail=project_detail,
                               # missing_arguments_list=missing_arguments_list,
                               # folderStructure=folderStructure,
                               # unusedArgument=unusedArgument,
                               # structurePath=structurePath,
                               # radarChartPath=radarChartPath)




@app.route("/retry")
def delete_pics():
    with app.app_context():
        return redirect(url_for('upload'))


# echarts graphs go here
@app.route("/radar", methods=['GET'])
def radar_plot_data():
    #print("THIS IS A LOG MESSAGE" + str(dict_score['naming']), file=sys.stderr)
    message = {'usage': session.get("usageScore"),
               'documentation': session.get("docScore"),
               'naming': session.get("namingScore")}
    return jsonify(message)


@app.route("/structure", methods=['GET'])
def project_structure_data():
    #gexf = project_structure.generate_gexf(df_annotation=df_annotation, main_location=main_location)
    #print("DF_ANNOTATION" + str(df_annotation), file=sys.stderr)
    message = {'gexf': session.get("gexf")}
    return jsonify(message)



# only run when executing locally (if this doesnt run then remove the if statement)
if __name__ == "__main__":
    socketio.run(app, debug=True)
    upload()
