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


# 5. Annotations in invoked workflow
def grade_annotation_in_workflow(df_annotation):
    completeProject = True
    for workflowPath in list(df_annotation['workflowName']):
        try:
            workflowPath = workflowPath.replace("\\", "/")
            with open("file/" + workflowPath, encoding='utf-8', mode='r') as workflow:
                for line in workflow:
                    if "DisplayName=" in line:
                        if "AnnotationText=" in line:
                            df_annotation.loc[df_annotation.workflowName == workflowPath, 'annotated'] = 1
                            break
        except FileNotFoundError:
            completeProject = False
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