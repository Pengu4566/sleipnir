import os
from builtins import len, open, list
import pandas as pd
import untangle
import re
import sys
import matplotlib.pyplot as plt
#from werkzeug import secure_filename
import shutil
from math import pi
from werkzeug.utils import secure_filename\

from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__, static_folder='./static/dist', template_folder="./static")

# dont save cache in web browser (updating results image correctly)
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_PATH'] = '/file/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'xaml', 'zip'])

# check variable's naming conventions
def CheckVariableName(df_variable):
    numVariables = len(df_variable.variableName)

    # check if variable name is proper in df_variable
    def ProperVariableNaming(df_variable_row):
        dic_type_abbreviation = {'String': 'str',
                                 'Int32': 'int',
                                 'DataColumn': 'dclm',
                                 'Double': 'dbl',
                                 'DateTime': 'date',
                                 'Array': 'arr',
                                 'List': 'lst',
                                 'Dictionary': 'dic',
                                 'Exception': 'ept',
                                 'QueueItem': 'qi'}

        # check camel case naming for everything right of the '_'
        # For everything right of "_" apply:
        # 	First character may not be upper
        # 	If > 2 upper case character
        #     Any upper case may be not be next to another upper case
        for j in df_variable['variableName']:
            # if it contains a "_", split on it and extract everything after
            if "_" in j:
                afterUnderscoreString = j.split('_')[1]
                #print(afterUnderscoreString,file=sys.stderr)

                # first char must not be upper
                if afterUnderscoreString[0].isupper():
                    return False

                # uppercase letters must not be next to each other
                counter = 0
                previousLetterUpper = False
                while counter < len(afterUnderscoreString):
                    currentLetterUpper = afterUnderscoreString[counter].isupper()
                    if previousLetterUpper & currentLetterUpper:
                        return False
                    else:
                        previousLetterUpper = currentLetterUpper
                        currentLetterUpper = False
                    # print(afterUnderscoreString[counter] + " " + afterUnderscoreString[counter - 1], file=sys.stderr)
                    counter = counter + 1
            return True

        #always
        #print("hello", file=sys.stderr)

        # variable type is in dict above and format matches ['abbreviation''_''anything'] i.e.(int_counter, str_thing)
        if (df_variable_row['variableType'] in dic_type_abbreviation.keys()) and \
                (df_variable_row['variableName'].startswith(dic_type_abbreviation[df_variable_row['variableType']] + '_')):
            return True
        # variable type is not in above dict but format still matches ['abbreviation''_''anything']
        elif (not df_variable_row['variableType'] in dic_type_abbreviation.keys()) and \
                ('_' in df_variable_row['variableName']):
            ind = 0
            abb = True
            for j in df_variable_row['variableName'].split('_')[0]:
                if (j in df_variable_row[df_variable_row['variableName']]) and \
                        (df_variable_row[df_variable_row['variableName']].find(j) <= ind):
                    abb = (abb and True)
                else:
                    abb = (abb and False)

                ind = df_variable_row[df_variable_row['variableName']].find(j)
                return abb
        else:
            return False

    df_variable['properNamed'] = df_variable.apply(ProperVariableNaming, axis=1)

    # return lists
    improperNamedVariable = list(df_variable.loc[df_variable.properNamed == False].variableName)
    unusedVariable = list(df_variable.loc[df_variable['count'] == 1].variableName)
    variableUsageScore = len(df_variable.loc[df_variable['count'] > 1]['count']) / numVariables * 100
    variableNamingScore = len(df_variable.loc[df_variable.properNamed == True].variableName) / numVariables * 100

    return [variableNamingScore, variableUsageScore, improperNamedVariable, unusedVariable]


# check argument in/out
def checkArgumentName(df_argument):
    numArgument = len(df_argument) / 100

    # check if argument name is proper in df_argument
    def proper(df_argument_row):
        if (df_argument_row['argumentType'] == 'InArgument') and \
                (df_argument_row['argumentName'].startswith('in_')):
            return True
        elif (df_argument_row['argumentType'] == 'OutArgument') and \
                (df_argument_row['argumentName'].startswith('out_')):
            return True
        elif (df_argument_row['argumentType'] == 'InOutArgument') and \
                (df_argument_row['argumentName'].startswith('io_')):
            return True
        else:
            return False

    df_argument['properNamed'] = df_argument.apply(proper, axis=1)

    # return lists
    argumentNamingScore = len(
        df_argument[df_argument['properNamed'] == True]) / numArgument
    # improperNamedArguments = list(df_argument[df_argument['properNamed']!= True].argumentName)
    temp_improperNamedArguments = list(
        df_argument[df_argument['properNamed'] != True].argumentName)
    improperNamedArguments = [
        x for x in temp_improperNamedArguments if x is not None]

    return [argumentNamingScore, improperNamedArguments]


# end check argument in/out

# activity naming
def ActivityNamingCheck(df_activity):
    # return listss
    df_activity['customizedName'] = (
        df_activity['activityName'] != df_activity['activityType'])
    activityNamingScore = len(df_activity[df_activity['customizedName'] == True].customizedName) / len(
        df_activity.customizedName) * 100
    improperNamedActivities = list(
        df_activity[df_activity['customizedName'] != True].activityName)

    return [activityNamingScore, improperNamedActivities]


# end activity naming

# screenshot in try catch block
def CheckSsinTC(df_catches):
    # checks if try/catch activities have screenshots within them
    if True in df_catches.groupby(['Screenshot Included']).size().index:
        numWSs = df_catches.groupby(['Screenshot Included']).size()[True]
    else:
        numWSs = 0

    if False in df_catches.groupby(['Screenshot Included']).size().index:
        noSsException = list(
            df_catches[df_catches['Screenshot Included'] == False]['Catch Id'])

    numCatch = len(df_catches['Screenshot Included'])

    if numCatch == 0:
        screenshotScore = 0
    else:
        screenshotScore = numWSs / numCatch * 100

    return [screenshotScore, noSsException]


# end screenshot in try catch block

# check invoke workflow annotation
def checkWfAnnotation(df_annotation):
    numWf = len(df_annotation.workflowName)
    notAnnotatedWf = list(
        df_annotation[df_annotation.annotated == 0].workflowName)
    wfAnnotationScore = 100 - (len(notAnnotatedWf) / numWf * 100)

    return [wfAnnotationScore, notAnnotatedWf]


# end check invoke workflow annotation

# check log message in try catch
def CheckLMinTC(df_catches):
    # checks if try/catch activities have log messages within them
    if True in df_catches.groupby(['Log Message Included']).size().index:
        numWLM = df_catches.groupby(['Log Message Included']).size()[True]
    else:
        numWLM = 0

    if False in df_catches.groupby(['Log Message Included']).size().index:
        noLMException = list(
            df_catches[df_catches['Log Message Included'] == False]['Catch Id'])

    numCatch = len(df_catches['Log Message Included'])
    logMessageScore = numWLM / numCatch * 100

    return [logMessageScore, noLMException]


# end check log message in try catch

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
        # check if the post request has the file part
        if 'file' not in request.files:
            return "You must pick a file! Use your browser's back button and try again."
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path)
            filename = filename.replace("\\", "/")

            # top will run locally (saving to michael's computer), bottom will run on Azure (linux)
            if __name__ == "__main__":
                file.save("C:/Users/Michael/Documents/sleipnir" + app.config['UPLOAD_PATH'] + filename)
            else:
                file.save("/home/site/wwwroot" + app.config['UPLOAD_PATH'] + filename)
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
    df_variable = pd.DataFrame(columns=['variableType', 'variableName',
                                        'count', 'filePath'])
    df_argument = pd.DataFrame(columns=['argumentName', 'argumentType',
                                        'filePath'])
    df_activity = pd.DataFrame(columns=['activityName', 'activityType',
                                        'filePath'])
    df_catches = pd.DataFrame(columns=['Catch Id', 'Screenshot Included',
                                       'filePath', 'Log Message Included'])
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

        # variables dataframe
        with open(filePath, encoding='utf-8', mode='r') as f:
            for line in f:
                if line.strip(" ").startswith('<Variable x:'):
                    variableName = untangle.parse(line.strip(" ")) \
                        .children[0]['Name']
                    dataType = untangle.parse(line.strip(" ")) \
                        .children[0]['x:TypeArguments'] \
                        .split(":")[1].split("(")[0]
                    if '[]' in dataType:
                        dataType = 'Array'
                    if (filePath not in list(df_variable[df_variable.variableName
                                                         == variableName].filePath)):
                        df_variable = df_variable.append({'variableType': dataType,
                                                          'variableName':
                                                              variableName,
                                                          'count': 1,
                                                          'filePath': filePath},
                                                         ignore_index=True)
        with open(filePath, encoding='utf-8', mode='r') as f:
            for line in f:
                for index, row in df_variable.iterrows():
                    if (re.search(('\[.*' + row['variableName'] + '.*\]'), line) is not None) and \
                            (filePath == row['filePath']):
                        row['count'] += 1
        # end variables dataframe

        # argument dataframe
        with open(filePath, encoding='utf-8', mode='r') as f:
            printLine = False
            style = 1
            for line in f:
                if 'ui:InvokeWorkflowFile.Arguments>' in line.strip(" "):
                    printLine = not printLine
                    style = 1
                if printLine and \
                        ('ui:InvokeWorkflowFile.Arguments>' not in line.strip(" ")) and \
                        (style == 1):
                    argumentName = untangle.parse(line.strip(" ")) \
                        .children[0]['x:Key']
                    argumentType = untangle.parse(line.strip(" ")) \
                        .children[0]._name
                    df_argument = df_argument.append({'argumentName': argumentName,
                                                      'argumentType':
                                                          argumentType,
                                                      'filePath': filePath},
                                                     ignore_index=True)
                if ('<x:Members>' in line.strip(" ")) or \
                        ('</x:Members>' in line.strip(" ")):
                    printLine = not printLine
                    style = 2
                if printLine and \
                        ('<x:Members>' not in line.strip(" ")) and (style == 2):
                    argumentName = untangle.parse(line.strip(" ")) \
                        .children[0]['Name']
                    argumentType = untangle.parse(line.strip(" ")) \
                        .children[0]['Type']
                    argumentType = argumentType[:argumentType.index('(')]
                    df_argument = df_argument.append({'argumentName': argumentName,
                                                      'argumentType':
                                                          argumentType,
                                                      'filePath': filePath},
                                                     ignore_index=True)
        # end argument dataframe

        # activity dataframe
        with open(filePath, encoding='utf-8', mode='r') as f:
            for line in f:
                if 'DisplayName=' in line:
                    name = re.search('DisplayName=\"[^\"]*\"',
                                     line.strip(' ')) \
                        .group(0)[len("DisplayName=\""):-1]
                    activity = line.strip(' ').split(' ')[0].strip('<')
                    activity = activity if 'ui:' not in activity else activity[3:]
                    df_activity = df_activity.append({'activityName': name,
                                                      'activityType': activity,
                                                      'filePath': filePath},
                                                     ignore_index=True)
        # end activity dataframe

        # try catch dataframe
        with open(filePath, encoding='utf-8', mode='r') as f:
            printLine = False
            activityList = []
            evaluate = False
            catchId = ''
            for line in f:
                if line.strip(" ").startswith('<Catch x:'):
                    activityList = []
                    printLine = not printLine
                    if 'sap2010:WorkflowViewState.IdRef' in line:
                        name = re.search("sap2010:WorkflowViewState.IdRef=\"[^\"]*\"",
                                         line.strip(" ")).group(0)
                        catchId = name[len(
                            "sap2010:WorkflowViewState.IdRef=\""):-1]
                if '</Catch>' in line.strip(" "):
                    printLine = not printLine
                    evaluate = True
                if printLine and (catchId == ''):
                    if ('<sap2010:WorkflowViewState.IdRef>' in line.strip(" ")) and \
                            ('</sap2010:WorkflowViewState.IdRef>' in line.strip(" ")) and \
                            ('Catch`' in line.strip(" ")):
                        catchId = re.search(
                            "Catch[^<]*", line.strip(" ")).group(0)
                if printLine and ('<Catch x:' not in line.strip(" ")):
                    activityList.append(line.strip(
                        " ").split(" ")[0].strip("<"))
                if evaluate:
                    evaluate = False
                    screenshotIncluded = False
                    logMessageIncluded = False
                    for i in activityList:
                        if 'ui:TakeScreenshot' == i:
                            screenshotIncluded = True
                        if 'ui:LogMessage' == i:
                            logMessageIncluded = True
                    df_catches = df_catches.append({'Catch Id': catchId,
                                                    'Screenshot Included':
                                                        screenshotIncluded,
                                                    'filePath': filePath,
                                                    'Log Message Included':
                                                        logMessageIncluded},
                                                   ignore_index=True)
                    catchId = ''
        # end try catch dataframe

        # annotation dataframe
        with open(filePath, encoding='utf-8', mode='r') as f:
            for line in f:
                if (line.strip(" ").startswith("<ui:InvokeWorkflowFile") and
                        "WorkflowFileName=" in line.strip(" ")):
                    workflowName = re.search('WorkflowFileName=\"[^\"]*\.xaml\"',
                                             line.strip(" ")).group(0)
                    workflowName = workflowName[(len('WorkflowFileName="')):-1]
                    df_annotation = df_annotation.append({'workflowName':
                                                          workflowName,
                                                          'annotated': False},
                                                         ignore_index=True)
        df_annotation = df_annotation.drop_duplicates()

    completeProject = True
    for workflowPath in list(df_annotation['workflowName']):
        try:
            workflowPath = workflowPath.replace("\\", "/")
            with open("file/" + workflowPath, encoding='utf-8', mode='r') as workflow:
                for line in workflow:
                    if "DisplayName=" in line:
                        if "AnnotationText=" in line:
                            df_annotation.loc[df_annotation.workflowName ==
                                              workflowPath, 'annotated'] = 1
                            break
        except FileNotFoundError:
            completeProject = False
    # end annotation dataframe

    # check variable naming convention
    [variableNamingScore, variableUsageScore, improperNamedVariable,unusedVariable] = CheckVariableName(df_variable)
    # check argument in/out
    [argumentNamingScore, improperNamedArguments] = checkArgumentName(df_argument)
    # check activity names
    [activityNamingScore, improperNamedActivities] = ActivityNamingCheck(df_activity)
    # screenshot in try/catch block
    [screenshotScore, noSsException] = CheckSsinTC(df_catches)
    # log message in try/catch block
    [logMessageScore, noLMException] = CheckLMinTC(df_catches)
    # workflow annotation
    if completeProject:
        [wfAnnotationScore, notAnnotatedWf] = checkWfAnnotation(df_annotation)
    else:
        [wfAnnotationScore, notAnnotatedWf] = [0, []]

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

__main__()
