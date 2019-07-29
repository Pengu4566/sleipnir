import sys
import os
import json
import pandas as pd
import xml.etree.ElementTree as ET

# 1. Logging contents
# 2. Log messages in catches
# 3. Screenshot in catches
# 4. Project.json (name and description)
# 5. Annotations in invoked workflow and main
# 6. Arguments should be at least mentioned in annotation
# 7. Comments


# 2. Log messages in catches
def grade_log_message_in_catches(df_catches, fileLocationStr):
    # columns=['Catch Id', 'Screenshot Included', 'filePath', 'Log Message Included']
    df_catches_dup = df_catches.loc[:, :]
    df_catches_dup.filePath = df_catches_dup.filePath.str.replace(fileLocationStr,'')
    numCatch = len(df_catches_dup['Log Message Included'])
    if numCatch > 0:
        # checks if try/catch activities have log messages within them
        logMessageScore = df_catches_dup['Log Message Included'].sum() / numCatch * 100
        if df_catches_dup['Log Message Included'].sum() < numCatch:
            noLMException = list(df_catches_dup[df_catches_dup['Log Message Included'] == False].dropna()
                                 .reset_index(drop=True).reset_index()
                                 .loc[:, ['index', 'Catch Id', 'filePath']].T.to_dict().values())
        else:
            noLMException = []

    else:
        [logMessageScore, noLMException] = [0, ["There is no catch in your project."]]

    return [logMessageScore, noLMException]
# end 2. Log messages in catches

# 3. Screenshot in catches
def grade_screenshot_in_catches(df_catches, fileLocationStr):
    df_catches_dup = df_catches.loc[:, :]
    df_catches_dup.filePath = df_catches_dup.filePath.str.replace(fileLocationStr,'')
    numCatch = len(df_catches_dup['Screenshot Included'])
    if numCatch > 0:
        # checks if try/catch activities have screenshots within them
        screenshotScore = df_catches_dup['Screenshot Included'].sum() / numCatch * 100
        if df_catches_dup['Screenshot Included'].sum() < numCatch:
            noSsException = list(df_catches[df_catches['Screenshot Included'] == False].dropna()
                                 .reset_index(drop=True).reset_index()
                                 .loc[:, ['index', 'Catch Id', 'filePath']].T.to_dict().values())
        else:
            noSsException = []

    else:
        [screenshotScore, noSsException] = [0, ["There is no catch in your project."]]

    return [screenshotScore, noSsException]
# end 3. Screenshot in catches

# 4. Project.json (name and description)
def grade_project_json_name_desc(folderPath):
    fileName = "project.json"
    lst_json = []
    for root, dirs, file in os.walk(folderPath):
        if fileName in file:
            project_folder_name = root.replace("\\", "/")
            fileLocation = project_folder_name + "/" + fileName
            lst_wf_associated = []
            for r, d, f in os.walk(project_folder_name):
                for xamlFile in f:
                    if '.xaml' in xamlFile:
                        lst_wf_associated.append(r.replace("\\", "/") + '/' + xamlFile)
            lst_json.append({fileLocation: lst_wf_associated})

    def collect_json_data(json_dic):
        # open file and collect data
        fileLocation = list(json_dic.keys())[0]
        with open(fileLocation, encoding='utf-8', mode='r') as project_json:
            jsonFile = json.load(project_json)
            project_json.close()
        project_name = jsonFile["name"]
        project_description = jsonFile["description"]
        if (project_description != "Blank Process") and (project_description != "Robotic Enterprise Framework") \
                and (project_description != "Blank Project"):
            json_description_score = 100
        else:
            json_description_score = 0
        if (project_name != "Template_QueuesNew") and (project_name != "Template_NonQueues") \
                and (project_name != "NonRepetativeFramework"):
            json_name_score = 100
        else:
            json_name_score = 0
        project_detail = {'projectName':project_name, 'projectDescription': project_description}
        row = pd.DataFrame.from_dict({'fileLocation': [fileLocation],
                                      'projectDetail': [project_detail],
                                      'mainFolder': [fileLocation[:-(len(fileName) + 1)]],
                                      'subfiles': [list(json_dic.values())[0]],
                                      'namingScore': [json_name_score],
                                      'descriptionScore': [json_description_score]})
        return row
    lst_df_json_row = list(map(collect_json_data, lst_json))
    df_json = pd.concat(lst_df_json_row, ignore_index=True)
    df_json = df_json.reset_index(drop=False)
    return df_json
# end 4. Project.json (name and description)

# 5. Annotations in invoked workflow
def grade_annotation_in_workflow(df_annotation, fileLocationStr, df_argument):
    # columns=['workflowName', 'invokedBy', 'mainLocation', 'annotated', 'annotation']
    df_annotation_dup = df_annotation.copy()
    df_annotation_dup['fileExists'] = df_annotation_dup.apply(lambda x: os.path.exists(x['workflowName']), axis=1)

    def extract_annot(df_row):
        wfPath = df_row['workflowName']
        try:
            tree = ET.parse(wfPath)
            root = tree.getroot()
            i = root.find('./{http://schemas.microsoft.com/netfx/2009/xaml/activities}Sequence')
            try:
                annot_text = i.attrib['{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}Annotation.AnnotationText']
            except AttributeError:
                annot_text = ''
            except KeyError:
                annot_text = ''
        except FileNotFoundError:
            annot_text = ''
        return annot_text

    df_annotation_dup['annotation'] = df_annotation_dup.apply(extract_annot, axis=1)
    df_annotation_dup['annotated'] = (df_annotation_dup['annotation'] != '')

    numWf = len(df_annotation_dup.workflowName)
    if numWf > 0:
        df_annotation_dup.workflowName = df_annotation_dup.workflowName.str.replace(fileLocationStr,'')
        notAnnotatedWf = list(df_annotation_dup[df_annotation_dup.annotated == 0].dropna()
                              .reset_index(drop=True).reset_index()
                              .loc[:, ['index', 'workflowName']].T.to_dict().values())
        wfAnnotationScore = 100 - (len(notAnnotatedWf) / numWf * 100)
    else:
        [wfAnnotationScore, notAnnotatedWf] = [0, ["There is no invoked workflow in your project."]]

    # 6.Arguments should be at least mentioned in annotation
    df_join_arg_annot = pd.merge(df_argument.copy().loc[:, ['argumentName', 'filePath']], df_annotation_dup.loc[:, ['workflowName', 'annotation']], left_on='filePath', right_on='workflowName', how='left').drop_duplicates(inplace=False)
    df_join_arg_annot.annotation.fillna('')
    def arginAnnot(df_join_row):
        if df_join_row['annotation'] == '':
            return False
        else:
            return str(df_join_row['argumentName']) in str(df_join_row['annotation'])
    df_join_arg_annot['arginAnnot'] = df_join_arg_annot.apply(arginAnnot, axis=1)
    if len(df_join_arg_annot) > 0:
        df_join_arg_annot.filePath = df_join_arg_annot.filePath.str.replace(fileLocationStr, '')
        missing_arguments_list = list(df_join_arg_annot[df_join_arg_annot['arginAnnot'] == False]
                                      .reset_index(drop=True).reset_index()
                                      .loc[:, ['index', 'argumentName', 'filePath']].T.to_dict().values())
    else:
        missing_arguments_list = ["There is no argument in this project."]
    AnnotationArgumentScore = len(missing_arguments_list)/len(df_join_arg_annot) if len(df_join_arg_annot) > 0 else 0

    return [wfAnnotationScore, notAnnotatedWf, AnnotationArgumentScore, missing_arguments_list]
# end 5. Annotations in invoked workflow
# end 6.Arguments should be at least mentioned in annotation


# 7. Comments
def grade_comments(df_annotation):
    completeProject = True
    commentsScore = 0
    # get project name for accurate filepath during grading
    comment_contents = "NO COMMENTS FOUND"
    for root, dirs, file in os.walk("file/"):
        if "project.json" in file:
            project_name = root.split("/", 1)[1]
            break
    for workflowPath in list(df_annotation['workflowName']):
        try:
            print(workflowPath, file=sys.stderr)
            workflowPath = workflowPath.replace("\\", "/")
            with open("file/" + project_name + "/" + workflowPath, encoding='utf-8', mode='r') as workflow:
                for line in workflow:
                    if "<ui:Comment" in line:
                        #try:
                        print(workflowPath, file=sys.stderr)
                        print(line.split("Text=")[1].split("\"")[1], file=sys.stderr)
                        #except IndexError:
        except FileNotFoundError:
            completeProject = False
    return commentsScore
# end 7. Comments