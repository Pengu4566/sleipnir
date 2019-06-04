import os
import pandas as pd
import zipfile
from werkzeug.utils import secure_filename

# dataframes
from dataframes import variable_dataframe, argument_dataframe, activity_dataframe, catch_dataframe, annotation_dataframe

#functions
from charts import radar_plot
from grading_checks import naming, usage, documentation_logging, error_handling
from soft_checks import activity_stats, project_folder_structure, project_structure

from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__, static_folder='./static/dist', template_folder="./static")

# dont save cache in web browser (updating results image correctly)
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_PATH'] = '/file/'
app.config['ALLOWED_EXTENSIONS'] = set(['zip'])


@app.route('/')
def upload():
    with app.app_context():
        return render_template('fileUpload.html')


@app.route("/uploader", methods=['GET', 'POST'])
def handle_upload():
    if request.method == 'POST':
        # clear out content in file folder
        for r, d, f in os.walk(app.config['UPLOAD_PATH'].strip("/")):
            for file in f:
                os.remove((os.getcwd() + "/" + r + "/" + file).replace("\\", "/"))
        folders = []
        for r, d, f in os.walk(app.config['UPLOAD_PATH'].strip("/")):
            folders = [(os.getcwd() + "/" + r).replace("\\", "/")] + folders
        folders = folders[:-1]
        for folder in folders:
            os.rmdir(folder)
        # check if the post request has the file part
        if 'file' not in request.files:
            return "You must pick a file! Use your browser's back button and try again."
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
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

            # top will run locally (saving to michael's computer), bottom will run on Azure (linux)
            if __name__ == "__main__":
                file.save((os.getcwd() + app.config['UPLOAD_PATH'] + filename).replace("\\", "/"))
                zipFile = zipfile.ZipFile((os.getcwd() + app.config['UPLOAD_PATH'] + filename).replace("\\","/"))
                zipFile.extractall((os.getcwd() + app.config['UPLOAD_PATH']).replace("\\", "/"))
            else:
                file.save("/home/site/wwwroot" + app.config['UPLOAD_PATH'] + filename)
                zipFile = zipfile.ZipFile("/home/site/wwwroot" + app.config['UPLOAD_PATH'] + filename)
                zipFile.extractall("/home/site/wwwroot" + app.config['UPLOAD_PATH'])
            return redirect("/analyze")


@app.route("/analyze")
def __main__():
    # old local filepath
    # filePath = "file\\"

    # azure filepaths
    filePath = "file"
    files = []

    for r, d, f in os.walk(filePath):
        for file in f:
            if '.xaml' in file:
                files.append(os.path.join(r, file))

    # dataframe initiation
    df_variable = pd.DataFrame(columns=['variableType', 'variableName', 'count', 'filePath'])
    df_argument = pd.DataFrame(columns=['argumentName', 'argumentType', 'filePath', 'dataType', 'count'])
    df_activity = pd.DataFrame(columns=['activityName', 'activityType', 'filePath'])
    df_catches = pd.DataFrame(columns=['Catch Id', 'Screenshot Included', 'filePath', 'Log Message Included'])
    df_annotation = pd.DataFrame(columns=['workflowName', 'invokedBy'])
    # end dataframe initiation

    fileCount = 1
    numFiles = len(files)

    # checks for empty files list, program should end if this gets triggered
    if (files == []):
        return "Could not find project files! Did you put them in the right place?"

    # scans all project files and populates dataframes with relevant info
    for filePath in files:
        print("Progress %d/%d: Scanning %s" % (fileCount, numFiles, filePath))
        fileCount += 1

        # variables dataframe
        df_variable = variable_dataframe.populate_variables_dataframe(df_variable = df_variable, filePath = filePath)
        # argument dataframe
        df_argument = argument_dataframe.populate_argument_dataframe(df_argument = df_argument, filePath = filePath)
        # activity dataframe
        df_activity = activity_dataframe.populate_activity_dataframe(df_activity=df_activity, filePath=filePath)
        # try catch dataframe
        df_catches = catch_dataframe.populate_catch_dataframe(df_catches=df_catches, filePath=filePath)
        # annotation dataframe
        df_annotation = annotation_dataframe.populate_annotation_dataframe(df_annotation=df_annotation, filePath=filePath)

    # level 1: grading checks

    # level 2: name
    # level 3: variable naming
    [variableNamingScore, improperNamedVariable] = naming.grade_variable_name(df_variable)
    # level 3: argument naming
    [argumentNamingScore, improperNamedArguments] = naming.grade_argument_name(df_argument)
    # level 3: activity naming
    [activityNamingScore, improperNamedActivities] = naming.grade_activity_name(df_activity)
    # level 2: naming score
    namingScore = (variableNamingScore + argumentNamingScore + activityNamingScore)/2

    # level 2: usage
    # level 3: variable usage
    [variableUsageScore, unusedVariable] = usage.grade_variable_usage(df_variable)
    # level 3: argument usage
    [argumentUsageScore, unusedArgument] = usage.grade_argument_usage(df_argument)
    # level 2: usage score
    usageScore = (variableUsageScore + argumentUsageScore)/2

    # level 2: documentation_logging
    # level 3: workflow annotation
    [wfAnnotationScore, notAnnotatedWf] = documentation_logging.grade_annotation_in_workflow(df_annotation=df_annotation)
    # level 3: log message in catches
    [logMessageScore, noLMException] = documentation_logging.grade_log_message_in_catches(df_catches=df_catches)
    # level 3: screenshot in catches
    [screenshotScore, noSsException] = documentation_logging.grade_screenshot_in_catches(df_catches=df_catches)
    # level 2: documentation_logging score
    docScore = (wfAnnotationScore + logMessageScore + screenshotScore)/3

    # outputs a perfentage score of the number of correct arguments and a list of missing arguments
    [AnnotationArgumentScore, missing_arguments_list] = documentation_logging.grade_annotation_contains_arguments(df_annotation=df_annotation)

    # establish score list and name list
    lst_score = [namingScore, usageScore, docScore]
    lst_tolerance = [90, 90, 100]
    lst_checkName = ['Naming', 'Usage', 'Documentation']

    # level 1: soft checks
    # level 2: activity stats
    activityStats = activity_stats.get_activity_stats(df_activity=df_activity)
    # level 2: folder structure
    if __name__ == "__main__":
        folderStructure = project_folder_structure.list_files(os.getcwd() + app.config['UPLOAD_PATH'])
    else:
        folderStructure = project_folder_structure.list_files("/home/site/wwwroot" + app.config['UPLOAD_PATH'])
    # level 2: project structure
    project_structure.get_project_structure(df_annotation)

    # radar plot
    radar_plot.radarPlot(lst_score=lst_score, lst_tolerance=lst_tolerance, lst_checkName=lst_checkName)

    improperNamedVar = str(improperNamedVariable).replace("'", "")
    unusedVar = str(unusedVariable).replace("'", "")
    improperNamedArg = str(improperNamedArguments).replace("'", "")
    improperNamedAct = str(improperNamedActivities).replace("'", "")
    noSsExp = str(noSsException).replace("'", "")
    notAnnotWf = str(notAnnotatedWf).replace("'", "")
    noLMExp = str(noLMException).replace("'", "")
    unusedArgument = str(unusedArgument).replace("'", "")

    with app.app_context():
        return render_template('index.html',
                               improperNamedVar=improperNamedVar,
                               unusedVar=unusedVar,
                               improperNamedArg=improperNamedArg,
                               improperNamedAct=improperNamedAct,
                               activityStats=activityStats,
                               noSsExp=noSsExp,
                               notAnnotWf=notAnnotWf,
                               noLMExp=noLMExp,
                               folderStructure=folderStructure,
                               unusedArgument=unusedArgument)


# only run when executing locally (if this doesnt run then remove the if statement)
if __name__ == "__main__":
    app.run(debug=True)
    upload()
