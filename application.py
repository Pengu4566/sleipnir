import os
import json
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
from soft_checks import activity_stats, project_folder_structure, project_structure, template_check, selector_check

from flask import Flask, request, render_template, redirect, url_for, session, jsonify, Response, send_file, make_response
from flask_session import Session
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL
import MySQLdb.cursors
from passlib.hash import sha256_crypt
import pdfkit

# es = Elasticsearch(['https://098b8510b627461cb0e77d37d10c4511.us-east-1.aws.found.io:9243'],
#                    http_auth=('elastic', '5mKdXBb77D2hLuukmTHwThkc'))
application = app = Flask(__name__, static_folder='./static/dist', template_folder="./static")

# dont save cache in web browser (updating results image correctly)
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_PATH'] = '/file/'
app.config['ALLOWED_EXTENSIONS'] = set(['zip'])
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SECRET_KEY'] = randint(0,99999999999999999999)

app.config['MYSQL_HOST'] = 'us-sql01.mysql.database.azure.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'us-evalsql01@us-sql01'
app.config['MYSQL_PASSWORD'] = 'LoraSQL123'
app.config['MYSQL_DB'] = 'sleipnir'
app.config['APP_ADMIN_RIGHT'] = 'admin'
mysql = MySQL(app)

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
pepper = 'zxf98g7yq3whretgih'

######

@app.route("/")
def login():
    with app.app_context():
        folderPathList = [os.getcwd().replace("\\", "/") + app.config['UPLOAD_PATH'] + path for path in
                          os.listdir(os.getcwd() + app.config['UPLOAD_PATH'])]
        filteredFolderPathList = [path for path in folderPathList if time.time() - os.path.getmtime(path) > 900]
        for folder in filteredFolderPathList:
            shutil.rmtree(folder, True)
        sessionPathList = [os.getcwd().replace("\\", "/") + '/flask_session/' + path for path in
                          os.listdir(os.getcwd() + '/flask_session/')]
        filteredSessionPathList = [path for path in sessionPathList if time.time() - os.path.getmtime(path) > 900]
        for ses in filteredSessionPathList:
            print(ses)
            os.remove(ses)

        if session.get("loggedin"):
            return redirect(url_for('upload'))
        else:
            return render_template('login.html')

@app.route("/login", methods=['POST'])
def validate_user():
    with app.app_context():
        requestData = json.loads(str(request.data, encoding="utf-8"))
        tenant = requestData['tenant']
        username = requestData['username']
        password = requestData['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id FROM tenants WHERE tenant_name = %s", (tenant,))
        tenant_record = cursor.fetchone()
        if tenant_record:
            tenant_id = tenant_record["id"]
            cursor.execute('SELECT id, password FROM users WHERE username = %s AND tenant_id = %s', (username, tenant_id,))
            user_record = cursor.fetchone()
            if user_record:
                user_id = user_record["id"]
                storedHashedPassword = user_record["password"]
                if sha256_crypt.verify(password+pepper, storedHashedPassword):
                    resp = jsonify({"result": render_template('fileUpload.html',
                                                              username=username,
                                                              user_id=user_id)})
                    session['loggedin'] = True
                    session['id'] = user_id
                    session['username'] = username
                    cursor.close()
                    return make_response(resp, 200)
                else:
                    cursor.close()
                    resp = jsonify({"message": "Wrong password"})
                    return make_response(resp, 400)
            else:
                cursor.close()
                resp = jsonify({"message": "User not exists"})
                return make_response(resp, 400)
        else:
            cursor.close()
            resp = jsonify({"message": "Tenant not exists"})
            return make_response(resp, 400)


@app.route('/logout')
def logout():
    with app.app_context():
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        return redirect(url_for('login'))

@app.route("/admin", methods=['GET'])
def admin():
    with app.app_context():
        if session.get('loggedin'):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users_rights WHERE user_id = %s "
                           "AND right_id IN (SELECT id FROM rights WHERE `right` = %s);",
                           (int(session.get('id')), app.config['APP_ADMIN_RIGHT'],))
            if cursor.fetchone():
                cursor.close()
                return render_template('adminPanel.html',
                                       username=session.get('username'),
                                       user_id=session.get('id'))
            else:
                cursor.close()
                return "Not Authorized"
        else:
            return "Please login first"


@app.route('/upload')
def upload():
    with app.app_context():
        folderPathList = [os.getcwd().replace("\\", "/") + app.config['UPLOAD_PATH'] + path for path in os.listdir(os.getcwd() + app.config['UPLOAD_PATH'])]
        filteredFolderPathList = [path for path in folderPathList if time.time() - os.path.getmtime(path) > 900]
        for folder in filteredFolderPathList:
            shutil.rmtree(folder, True)
        if session.get('loggedin'):
            return render_template('fileUpload.html',
                                   username=session.get('username'),
                                   user_id=session.get('id'))
        else:
            return "Please login first"


def background_thread():
    while True:
        socketio.emit('message', {'alive': "Alive"})
        socketio.sleep(60)


@socketio.on('connect')
def connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)


@app.route("/processing", methods=["POST"])
def processing():
    requestData=json.loads(str(request.data, encoding="utf-8"))

    # Get related info from Project.json (name and description)
    folderPath = session.get('folderPath')
    fileLocationStr = session.get('fileLocationStr')
    files = session.get('files')

    df_json = documentation_logging.grade_project_json_name_desc(folderPath)
    df_json_exp = pd.DataFrame(df_json.subfiles.tolist(), index=df_json['index']).stack().reset_index()
    df_json_exp.columns = ['projectId', 'fileIndex', 'filePath']
    lst_name = []
    df_json['projectName'] = df_json.apply(lambda x: x['projectDetail']['projectName'], axis=1)
    for name in list(df_json['projectName']):
        if name not in lst_name:
            lst_name.append(name)
        else:
            count = 2
            dup_name = name + '_' + str(count)
            while dup_name in lst_name:
                count += 1
                dup_name = name + '_' + str(count)
            lst_name.append(dup_name)
    df_json['projectName'] = lst_name
    df_json_exp = pd.merge(df_json_exp, df_json.loc[:, ["mainFolder", 'projectName']].reset_index(), how="left",
                           left_on="projectId", right_on="index")
    df_json_exp.drop(columns=['fileIndex', "index"], inplace=True)

    if requestData["setting"]["jsonLog"]:
        project_detail = list(df_json.copy().reset_index().loc[:, ['index', 'projectDetail', 'projectName']]
                              .T.to_dict().values())
        json_name_score = df_json.namingScore.sum() / len(df_json.namingScore)
        json_description_score = df_json.descriptionScore.sum() / len(df_json.descriptionScore)
    else:
        json_name_score = "[Not evaluated]"
        json_description_score = "[Not evaluated]"
        project_detail = ['Not evaluated']

    # scans all project files and populates dataframes with relevant info
    socketio.emit('progress', {'data': 'Processing Files ...'})
    socketio.sleep(0.1)

    lst_sub_df = [dataframe.populate_dataframe(files[i], df_json) for i in range(len(files))]

    df_variable = pd.merge(pd.concat([x[0] for x in lst_sub_df], ignore_index=True).drop_duplicates(inplace=False),
                           df_json_exp, how="left", on="filePath")

    df_argument = pd.merge(pd.concat([x[1] for x in lst_sub_df], ignore_index=True).drop_duplicates(inplace=False),
                           df_json_exp, how="left", on="filePath")

    df_catches = pd.merge(pd.concat([x[2] for x in lst_sub_df], ignore_index=True).drop_duplicates(inplace=False),
                          df_json_exp, how="left", on="filePath")

    df_activity = pd.merge(pd.concat([x[3] for x in lst_sub_df], ignore_index=True).drop_duplicates(inplace=False),
                           df_json_exp, how="left", on="filePath")

    df_annotation = pd.concat([x[4] for x in lst_sub_df], ignore_index=True).drop_duplicates(inplace=False)

    df_selector = pd.merge(pd.concat([x[5] for x in lst_sub_df], ignore_index=True).drop_duplicates(inplace=False),
                           df_json_exp, how="left", on="filePath")

    dict_score = {}
    # level 1: grading checks

    # level 2: name
    # if session.get("naming"):
    if True:
        # level 3: variable naming
        if requestData["setting"]['varName']:
            [variableNamingScore, improperNamedVariable] = naming.grade_variable_name(df_variable=df_variable)
            improperNamedVar = improperNamedVariable
        else:
            improperNamedVar = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
            variableNamingScore = "[Not evaluated]"

        # level 3: argument naming
        if requestData["setting"]['argName']:
            [argumentNamingScore, improperNamedArguments] = naming.grade_argument_name(df_argument=df_argument)
            improperNamedArg = improperNamedArguments
        else:
            improperNamedArg = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
            argumentNamingScore = "[Not evaluated]"

        # level 3: activity naming
        if requestData["setting"]['actName']:
            [activityNamingScore, improperNamedActivities] = naming.grade_activity_name(df_activity=df_activity)
            improperNamedAct = improperNamedActivities
        else:
            improperNamedAct = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
            activityNamingScore = "[Not evaluated]"

        lt_namingScore = [variableNamingScore, argumentNamingScore, activityNamingScore]
        namingScore = 0
        count = 0
        for i in lt_namingScore:
            if i != "[Not evaluated]":
                namingScore += i
                count += 1
        if count==0:
            namingScore = "[Not evaluated]"
        else:
            namingScore = int(namingScore / count)

    else:
        improperNamedVar = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
        improperNamedArg = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
        improperNamedAct = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
        namingScore = "[Not evaluated]"

    dict_score['naming'] = namingScore

    # level 2: usage
    # if session["usage"]:
    if True:
        # level 3: variable usage
        if requestData["setting"]['varUsage']:
            [variableUsageScore, unusedVariable] = usage.grade_variable_usage(df_variable=df_variable)
            unusedVar = unusedVariable
        else:
            unusedVar = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
            variableUsageScore = "[Not evaluated]"

        # level 3: argument usage
        if requestData["setting"]['argUsage']:
            [argumentUsageScore, unusedArgument] = usage.grade_argument_usage(df_argument=df_argument)
            unusedArgument = unusedArgument
        else:
            unusedArgument = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
            argumentUsageScore = "[Not evaluated]"

        # level 2: usage score
        lt_usageScore = [variableUsageScore, argumentUsageScore]
        usageScore = 0
        count = 0
        for i in lt_usageScore:
            if i != "[Not evaluated]":
                usageScore += i
                count += 1
        if count==0:
            usageScore = "[Not evaluated]"
        else:
            usageScore = int(usageScore / count)

    else:
        unusedVar = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
        unusedArgument = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
        usageScore = "[Not evaluated]"

    dict_score['usage'] = usageScore

    # level 2: documentation_logging
    # if session["documentation"]:
    if True:
        # level 3: log message in catches
        if requestData["setting"]['tcLog']:
            [logMessageScore, noLMException] = documentation_logging.grade_log_message_in_catches(df_catches=df_catches)

            noLMExp = noLMException
        else:
            logMessageScore = "[Not evaluated]"
            noLMExp = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])

        # level 3: screenshot in catches
        if requestData["setting"]['tcSs']:
            [screenshotScore, noSsException] = documentation_logging.grade_screenshot_in_catches(df_catches=df_catches)
            noSsExp = noSsException
        else:
            screenshotScore = "[Not evaluated]"
            noSsExp = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])

        # level 3: workflow annotation
        [wfAnnotationScore, notAnnotatedWf, AnnotationArgumentScore, missing_arguments] =\
            documentation_logging.grade_annotation_in_workflow(df_annotation=df_annotation,
                                                               df_argument=df_argument)
        if requestData["setting"]['wfAnnot']:
            notAnnotWf = notAnnotatedWf
        else:
            wfAnnotationScore = "[Not evaluated]"
            notAnnotWf = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])

        # level 3: Arguments should be at least mentioned in annotation
        # outputs a percentage score of the number of correct arguments and a list of missing arguments
        if requestData["setting"]['argExp']:
            missing_arguments = missing_arguments
        else:
            missing_arguments = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
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
        if count==0:
            docScore = "[Not evaluated]"
        else:
            docScore = int(docScore / count)

    else:
        noSsExp = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
        notAnnotWf = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
        noLMExp = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
        missing_arguments = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
        project_detail = ['Not evaluated']
        docScore = "[Not evaluated]"

    dict_score['documentation'] = docScore

    # establish score list and name list
    dict_tolerance = {'naming': 90, 'usage': 90, 'documentation': 100}
    lst_score = []
    lst_tolerance = []
    lst_checkName = []
    for checks in ['naming', 'usage', 'documentation']:
        lst_score.append(dict_score[checks])
        lst_tolerance.append(dict_tolerance[checks])
        lst_checkName.append(checks.capitalize())

    # level 1: soft checks
    # level 2: activity stats

    # activityStats = activity_stats.get_activity_stats(df_activity=df_activity)
    df_activityStats = activity_stats.get_activity_stats(df_activity=df_activity)
    activityStats = list(df_activityStats.reset_index(drop=True).reset_index(drop=False).T.to_dict().values())
    activityTypes = [{'index': -1, 'activityType': 'All Activities'}] + list(df_activityStats.loc[:, ['activityType']]
                                                                             .drop_duplicates(inplace=False)
                                                                             .sort_values('activityType')
                                                                             .reset_index(drop=True)
                                                                             .reset_index(drop=False).T.to_dict().values())

    # level 2: folder structure
    folderStructure = project_folder_structure.list_files(fileLocationStr=fileLocationStr)
    session['folderStructure'] = folderStructure

    # level 2: project structure
    gexf = project_structure.generate_gexf(df_annotation=df_annotation, fileLocationStr=fileLocationStr)
    session['gexf'] = gexf

    #level 2: check template
    df_templateComment = template_check.check_template(df_json_exp=df_json_exp, df_annotation=df_annotation,
                                                       df_activity=df_activity, df_json=df_json)
    for project in project_detail:
        project['templateComment'] = df_templateComment[df_templateComment['index'] == project['index']].template_comment.values[0]

    #level 2: check selectors
    lst_selector_data = selector_check.selector_check(df_selector=df_selector)

    # pass along the variables
    df_table1 = pd.concat([improperNamedVar, unusedVar, improperNamedArg, unusedArgument,
                           improperNamedAct, noSsExp, noLMExp,
                           notAnnotWf, missing_arguments], ignore_index=True)

    table1File = [{'index': -1, 'file': 'All Files'}] + list(df_table1.loc[:, ['file']].drop_duplicates(inplace=False)
                                                       .sort_values('file').reset_index(drop=True)
                                                       .reset_index(drop=False).T.to_dict().values())
    table1Type = [{'index': -1, 'type': 'All Types'}] + list(df_table1.loc[:, ['type']].drop_duplicates(inplace=False)
                                                       .sort_values('type').reset_index(drop=True)
                                                       .reset_index(drop=False).T.to_dict().values())
    table1Error = [{'index': -1, 'error': 'All Errors'}] + list(df_table1.loc[:, ['error']].drop_duplicates(inplace=False)
                                                         .sort_values('error').reset_index(drop=True)
                                                         .reset_index(drop=False).T.to_dict().values())
    table1Project = [{'index': -1, 'project': 'All Projects'}] + list(df_table1.loc[:, ['project']]
                                                             .drop_duplicates(inplace=False).sort_values('project')
                                                             .reset_index(drop=True).reset_index(drop=False)
                                                             .T.to_dict().values())

    session['namingScore'] = namingScore
    session['usageScore'] = usageScore
    session['docScore'] = docScore
    session['table1'] = list(df_table1.reset_index(drop=True).reset_index(drop=False).T.to_dict().values())
    session['table1File'] = table1File
    session['table1Type'] = table1Type
    session['table1Error'] = table1Error
    session['table1Project'] = table1Project
    session['activityStats'] = activityStats
    session['activityTypes'] = activityTypes
    session['project_detail'] = project_detail
    session['selector'] = lst_selector_data

    resp = jsonify({"result": "success"})
    return make_response(resp, 200)

@app.route("/result")
def result():
    with app.app_context():
        return render_template('index.html',
                               username=session.get('username'),
                               user_id=session.get('id'),
                               namingScore=session['namingScore'],
                               usageScore=session['usageScore'],
                               docScore=session['docScore'],
                               table1={'data': session['table1'],
                                       'file': session['table1File'],
                                       'type': session['table1Type'],
                                       'error': session['table1Error'],
                                       'project': session['table1Project']},
                               actStats={"data": session['activityStats'],
                                         "activity": session['activityTypes'],
                                         "file": session['table1File'],
                                         "project": session['table1Project']},
                               project_detail={"data": session['project_detail']},
                               selectorEval={"data": session['selector'],
                                             "file": session['table1File'],
                                             "project": session['table1Project']})

@app.route("/retry")
def delete_pics():
    with app.app_context():
        return redirect(url_for('upload'))


@app.route("/fileUploading", methods=["POST"])
def fileUploading():
    with app.app_context():
        file = request.files['file']
        filename = secure_filename(file.filename).replace("\\", "/")
        generatedFileNaming = filename.replace(".zip", "") + str(time.time()).replace(".", "") + \
                              str(randint(1, 999999999999)) + ".zip"
        if os.path.isfile(os.getcwd() + app.config['UPLOAD_PATH'] + generatedFileNaming):
            nameDup = True
            while nameDup:
                generatedFileNaming = filename.replace(".zip", "") + str(time.time()).replace(".", "") + \
                                      str(randint(1, 999999999999)) + ".zip"
                nameDup = os.path.isfile(os.getcwd() + app.config['UPLOAD_PATH'] + generatedFileNaming)
        file.save((os.getcwd() + app.config['UPLOAD_PATH'] + generatedFileNaming).replace("\\", "/"))
        generatedFolderName = filename[:-4] + str(time.time()).replace(".", "") + str(randint(1, 999999999999))

        if os.path.isdir((os.getcwd() + app.config['UPLOAD_PATH'] + generatedFolderName).replace("\\", "/")):
            folderExist = True
            while folderExist:
                generatedFolderName = filename[:-4] + str(time.time()).replace(".", "") + \
                                      str(randint(1, 999999999999))
                folderExist = os.path.isdir((os.getcwd() + app.config['UPLOAD_PATH'] +
                                             generatedFolderName).replace("\\", "/"))

        folderPath = (os.getcwd() + app.config['UPLOAD_PATH'] + generatedFolderName).replace("\\", "/")

        zipFile = zipfile.ZipFile(
            (os.getcwd() + app.config['UPLOAD_PATH'] + generatedFileNaming).replace("\\", "/"))
        zipFile.extractall(folderPath)
        zipFile.close()

        os.remove((os.getcwd() + app.config['UPLOAD_PATH'] + generatedFileNaming).replace("\\", "/"))
        session['folderPath'] = folderPath

        files = []
        for r, d, f in os.walk(folderPath):
            for file in f:
                if '.xaml' in file:
                    files.append(os.path.join(r, file).replace("\\", "/"))
        fileLocationStr = (os.getcwd() + app.config['UPLOAD_PATH'] + generatedFolderName).replace("\\", "/") + "/"
        for r, d, f in os.walk(folderPath):
            if len(d) == 1:
                fileLocationStr = r.replace("\\", "/") + "/" + d[0] + "/"
            else:
                break
        session['fileLocationStr'] = fileLocationStr
        session['files'] = files
        if (files == []):
            return {"message": "There is no xaml file in the zip file."}, 400
        else:
            resp = jsonify({"message": "File uploaded successfully.", "fileLocation": folderPath})
            return make_response(resp, 200)



# @app.route("/elastic")
# def send_data():
#     ipAddress = request.remote_addr
#     body = {
#         'namingScore': session.get("namingScore"),
#         'usageScore': session.get("usageScore"),
#         'docScore': session.get("docScore"),
#         'improperNamedVar': session.get("improperNamedVar"),
#         'unusedVar': session.get("unusedVar"),
#         'improperNamedArg': session.get("improperNamedArg"),
#         'improperNamedAct': session.get("improperNamedAct"),
#         'activityStats': session.get("activityStats"),
#         'noSsExp': session.get("noSsExp"),
#         'notAnnotWf': session.get("notAnnotWf"),
#         'noLMExp': session.get("noLMExp"),
#         'project_detail': session.get("project_detail"),
#         'missing_arguments_list': session.get("missing_arguments_list"),
#         'unusedArgument': session.get("unusedArgument"),
#         'selectorEval': session.get('selector')
#     }
#
#     id = str(ipAddress)+'-'+str(time.time()).split('.')[0]
#
#     result = es.index(index='sleipnirdb', doc_type='projectdata', id=id, body=body)
#
#     return jsonify(result)


@app.route("/download/queue")
def return_file_queue():
    return send_file(os.getcwd().replace("\\", "/") + '/static/akoa_template/Queue_Template.zip', attachment_filename='Queue Template.zip')

@app.route("/download/nonqueue")
def return_file_nonqueue():
    return send_file(os.getcwd().replace("\\", "/") + '/static/akoa_template/Non-queue_Template.zip', attachment_filename='Non-Queue Template.zip')

@app.route("/download/nonrepetitive")
def return_file_nonrepetitive():
    return send_file(os.getcwd().replace("\\", "/") + '/static/akoa_template/Non-repetitive_Template.zip', attachment_filename='Non-Repetitive Template.zip')


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


@app.route("/folder", methods=['GET'])
def folder_graph():
    message = session.get("folderStructure")
    return jsonify(message)


@app.route("/getreport", methods=['GET'])
def getReport():
    config = pdfkit.configuration(wkhtmltopdf=(os.getcwd().replace("\\", "/")+'/wkhtmltox/bin/wkhtmltopdf.exe'))
    html_string = render_template('report.html',
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
                                 unusedArgument={"data": session.get("unusedArgument")},
                                 selectorEval=str({"data": session.get('selector')}).replace("\"", "'"))
    report = pdfkit.from_string(html_string, False, configuration=config)

    return Response(
        report,
        mimetype="application/pdf",
        headers={"Content-disposition":
                 "attachment; filename=Report.pdf"}
    )



# only run when executing locally
if __name__ == "__main__":
    socketio.run(app, debug=True)
    upload()
