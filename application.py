import os
from builtins import len, open, list
import sys
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
from math import pi
from werkzeug.utils import secure_filename

# import grading functions
from grading_checks import variable_naming
from grading_checks import arguments_io
from grading_checks import activity_naming
from grading_checks import try_catch
from grading_checks import workflow_annotation

# flask init
from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__, static_folder='./static/dist', template_folder="./static")

# dont save cache in web browser (updating results image correctly)
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_PATH'] = '/file/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'xaml', 'zip'])

# radar chart
def radarPlot(variableNamingScore, variableUsageScore, argumentNamingScore,
              activityNamingScore, screenshotScore, wfAnnotationScore, logMessageScore):
    # Set data
    df = pd.DataFrame({
        'group': ['Score', 'tolerance'],
        'Variable Naming': [variableNamingScore, 90],
        'Variable Usage': [variableUsageScore, 100],
        'Argument Naming': [argumentNamingScore, 90],
        'Activity Naming': [activityNamingScore, 100],
        'Exception Screenshot': [screenshotScore, 100],
        'Exception Log Message': [logMessageScore, 100],
        'Workflow Annotation': [wfAnnotationScore, 100]
    })

    categories = list(df)[1:]
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], categories, color='Blue', size=12)
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60",
                                       "80", "100"], color="grey", size=10)
    plt.ylim(0, 100)

    # Actual
    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=0, linestyle='solid', label="group A")
    ax.fill(angles, values, 'b', alpha=0.1)

    # Tolerance
    values = df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='--', label="group B")

    # finish up
    plt.savefig('static/dist/Score.png')
    plt.close()
# end radar chart

@app.route('/')
def upload():
    return render_template('fileUpload.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


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
            return('No selected file')
        if not allowed_file(file.filename):
            with app.app_context():
                return render_template("wrongFile.html")
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path)
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
    # testing file structure
    # import os
    # files = os.listdir('file')
    # print(files)
    # return str(files)

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
    df_activity = pd.DataFrame(columns=['activityName', 'activityType', 'filePath'])
    df_catches = pd.DataFrame(columns=['Catch Id', 'Screenshot Included', 'filePath', 'Log Message Included'])
    df_annotation = pd.DataFrame(columns=['workflowName', 'filePath'])
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

        # populate dataframes
        df_variable = variable_naming.populate_variables_dataframe(filePath)
        df_argument = arguments_io.populate_args_dataframe(filePath)
        # df_activity = activity_naming.populate_activity_dataframe()
        # try/catch populating (2)
        # df_annotation = workflow_annotation.populate_workflow_annotation_dataframe()

        print(str(df_argument), file=sys.stderr)

    # grade variable naming convention
    [variableNamingScore, variableUsageScore, improperNamedVariable,unusedVariable] = \
        variable_naming.grade_variable_name(df_variable)

    # grade argument in/out
    [argumentNamingScore, improperNamedArguments] = arguments_io.grade_arguments_io(df_argument)

    # grade activity names
    #[activityNamingScore, improperNamedActivities] = activity_naming.activity_naming_check(df_activity)

    # screenshot in try/catch block
    #[screenshotScore, noSsException] = CheckSsinTC(df_catches)
    # log message in try/catch block
    #[logMessageScore, noLMException] = CheckLMinTC(df_catches)

    # workflow annotation
    #if completeProject:
    #    [wfAnnotationScore, notAnnotatedWf] = checkWfAnnotation(df_annotation)
    #else:
    #    [wfAnnotationScore, notAnnotatedWf] = [0, []]

    radarPlot(variableNamingScore=variableNamingScore,
              variableUsageScore=variableUsageScore,
              argumentNamingScore=argumentNamingScore,
              activityNamingScore=activityNamingScore,
              screenshotScore=screenshotScore,
              wfAnnotationScore=wfAnnotationScore,
              logMessageScore=logMessageScore)

    improperNamedVar = str(improperNamedVariable).replace("'", "")
    unusedVar = str(unusedVariable).replace("'", "")
    improperNamedArg = str(improperNamedArguments).replace("'", "")
    improperNamedAct = str(improperNamedActivities).replace("'", "")
    noSsExp = str(noSsException).replace("'", "")
    notAnnotWf = str(notAnnotatedWf).replace(
        "'", "") if completeProject else "The file you uploaded is not completed."
    noLMExp = str(noLMException).replace("'", "")


    with app.app_context():
        return render_template('index.html',
                               improperNamedVar=improperNamedVar,
                               unusedVar=unusedVar,
                               improperNamedArg=improperNamedArg,
                               improperNamedAct=improperNamedAct,
                               noSsExp=noSsExp,
                               notAnnotWf=notAnnotWf,
                               noLMExp=noLMExp)

# only run when executing locally (if this doesnt run then remove the if statement)
if __name__ == "__main__":
    app.run(debug=True)

upload()