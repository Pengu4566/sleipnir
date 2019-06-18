import sys
import os
import re

# 1. Logging contents
# 2. Log messages in catches
# 3. Screenshot in catches
# 4. Project.json (name and description)
# 5. Annotations in invoked workflow and main
# 6. Arguments should be at least mentioned in annotation
# 7. Comments


# 2. Log messages in catches
def grade_log_message_in_catches(df_catches):
    numCatch = len(df_catches['Log Message Included'])
    if numCatch > 0:
        # checks if try/catch activities have log messages within them
        if True in df_catches.groupby(['Log Message Included']).size().index:
            numWLM = df_catches.groupby(['Log Message Included']).size()[True]
        else:
            numWLM = 0

        if False in df_catches.groupby(['Log Message Included']).size().index:
            noLMException = list(
                df_catches[df_catches['Log Message Included'] == False]['Catch Id'])
        else:
            noLMException = []

        logMessageScore = numWLM / numCatch * 100
    else:
        [logMessageScore, noLMException] = [0, ["There is no catch in your project."]]

    return [logMessageScore, noLMException]
# end 2. Log messages in catches


# 3. Screenshot in catches
def grade_screenshot_in_catches(df_catches):
    numCatch = len(df_catches['Screenshot Included'])
    if numCatch > 0:
        # checks if try/catch activities have screenshots within them
        if True in df_catches.groupby(['Screenshot Included']).size().index:
            numWSs = df_catches.groupby(['Screenshot Included']).size()[True]
        else:
            numWSs = 0

        if False in df_catches.groupby(['Screenshot Included']).size().index:
            noSsException = list(
                df_catches[df_catches['Screenshot Included'] == False]['Catch Id'])
        else:
            noSsException = []
        screenshotScore = numWSs / numCatch * 100
    else:
        [screenshotScore, noSsException] = [0, ["There is no catch in your project."]]

    return [screenshotScore, noSsException]
# end 3. Screenshot in catches

# 4. Project.json (name and description)
def grade_project_json_name_desc():
    fileName = "project.json"
    project_name = "NO PROJECT FOUND"
    project_description = "NO DESCRIPTION FOUND"
    json_name_score = 0
    json_description_score = 0
    for root, dirs, file in os.walk("file/"):
        if fileName in file:
            project_folder_name = root.replace("\\","/")
            # open file and collect data
            with open(project_folder_name + "/" + fileName, encoding='utf-8', mode='r') as project_json:
                for line in project_json:
                    if "\"name\":" in line:
                        project_name = line.split(":")[1].split("\"")[1]
                    if "\"description\":" in line:
                        project_description = line.split(":")[1].split("\"")[1]
                    if "\"main\":" in line:
                        main_file = line.split(":")[1].split("\"")[1].replace("\\", "/")
                        if "/" in main_file:
                            main_location = project_folder_name + "/" + "/".join(main_file.split("/")[:-1])
                        else:
                            main_location = project_folder_name
                #print("PROJECT NAME-" + project_name, file=sys.stderr)
                #print("PROJECT DESCRIPTION-" + project_description, file=sys.stderr)
            break
            # perform json grading checks
    if (project_description != "Blank Process") and (project_description != "Robotic Enterprise Framework")\
            and (project_description != "Blank Project"):
        json_description_score = 100
    if (project_name != "Template_QueuesNew") and (project_name != "Template_NonQueues")\
            and (project_name != "NonRepetativeFramework"):
        json_name_score = 100
    project_detail =[project_name, project_description]
    return [json_name_score, json_description_score, project_detail, main_location]
# end 4. Project.json (name and description)

# 5. Annotations in invoked workflow
def grade_annotation_in_workflow(df_annotation, main_location):
    df_annotation['workflowName'] = main_location + "/" + df_annotation['workflowName']
    df_annotation['invokedBy'] = main_location + "/" + df_annotation['invokedBy']
    completeProject = True
    for workflowPath in list(df_annotation['workflowName']):
        try:
            workflowPath = workflowPath.replace("\\", "/")
            with open(workflowPath + ".xaml", encoding='utf-8', mode='r') as workflow:
                for line in workflow:
                    if "DisplayName=" in line:
                        if "AnnotationText=" in line:
                            df_annotation.loc[df_annotation.workflowName == workflowPath, 'annotated'] = 1
                            break
        except FileNotFoundError:
            print(workflowPath + ".xaml")
            completeProject = False
            break
    if completeProject:
        numWf = len(df_annotation.workflowName)
        if numWf > 0:
            notAnnotatedWf = list(
                df_annotation[df_annotation.annotated == 0].workflowName)
            wfAnnotationScore = 100 - (len(notAnnotatedWf) / numWf * 100)
        else:
            [wfAnnotationScore, notAnnotatedWf] = [0, ["There is no invoked workflow in your project."]]
    else:
        [wfAnnotationScore, notAnnotatedWf] = [0, ["The file you uploaded is not completed."]]

    return [wfAnnotationScore, notAnnotatedWf]

# end 5. Annotations in invoked workflow


# 6.Arguments should be at least mentioned in annotation
def grade_annotation_contains_arguments(df_annotation, main_location):
    completeProject = True
    missing_arguments_list = []
    num_args_in_annotation = 0
    AnnotationArgumentScore = 0
    # get project name for accurate filepath during grading
    for workflowPath in list(df_annotation['workflowName']):
        try:
            # print(workflowPath, file=sys.stderr)
            workflowPath = workflowPath.replace("\\", "/")
            with open(workflowPath + ".xaml", encoding='utf-8', mode='r') as workflow:
                # print("OPENING - " + "file/" + project_folder_name + "/" + workflowPath, file=sys.stderr)
                # build list of arguments to search for in annotation
                argument_list = []
                for line in workflow:
                    if "x:Property Name" in line:
                        argument_list.append(line.split("\"")[1].split("\"")[0])
                    # search for matching arguments in invoked workflow annotation
                    # (use first occurence for top level sequence annotation only)
                    if "AnnotationText" in line:
                        for arg in argument_list:
                            if arg in line:
                                num_args_in_annotation = num_args_in_annotation + 1
                            else:
                                missing_arguments_list.append(arg)
                        break
                # search for arguments in invoke activity annotation
                # (there is no easy way to obtain the calling method from a workflow. )
                #argument_list = df_argument.loc[:, "argumentName"]
                # print("ARGUMENTS - " + str(argument_list), file=sys.stderr)
        except FileNotFoundError:
            print(workflowPath + ".xaml")
            completeProject = False
            break
    if completeProject:
        # score is number of arguments in annotation out of total number of args mobile
        if (len(missing_arguments_list) + num_args_in_annotation) != 0:
            AnnotationArgumentScore = (num_args_in_annotation / (len(missing_arguments_list) + num_args_in_annotation)) * 100
        else:
            AnnotationArgumentScore = 0
            missing_arguments_list = "There is no argument in this project."
    else:
        return [0, ["The file you uploaded is not completed."]]
    # print("ARG SCORE " + str(AnnotationArgumentScore) + "%", file=sys.stderr)
    # print("MISSING ARGS " + str(missing_arguments_list), file=sys.stderr)
    # print("NUM ARGS OK " + str(num_args_in_annotation), file=sys.stderr)
    return [AnnotationArgumentScore, missing_arguments_list]
# end 6.Arguments should be at least mentioned in annotation
####
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