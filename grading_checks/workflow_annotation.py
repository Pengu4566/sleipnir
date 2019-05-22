import untangle
import pandas as pd
import re
import sys


def populate_workflow_annotation_dataframe(filePath):

    # init dataframe
    df_annotation = pd.DataFrame(columns=['workflowName', 'filePath'])

    with open(filePath, encoding='utf-8', mode='r') as f:
        numWfAnnotError = 0
        for line in f:
            if (line.strip(" ").startswith("<ui:InvokeWorkflowFile") and
                    "WorkflowFileName=" in line.strip(" ")):
                try:
                    workflowName = re.search('WorkflowFileName=\"[^\"]*\.xaml\"', line.strip(" ")).group(0)
                    workflowName = workflowName[(len('WorkflowFileName="')):-1]
                    df_annotation = df_annotation.append({'workflowName': workflowName,
                                                          'annotated': False},
                                                         ignore_index=True)
                # no workflow name found in the invoke workflow block, need to be resolved
                except AttributeError:
                    numWfAnnotError += 1

    df_annotation = df_annotation.drop_duplicates()
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

    #print(str(df_annotation))

    return [df_annotation, completeProject]

def grade_workflow_annotation(df_annotation):

    # checks if df_annotation length is zero and returns zeros for all scores
    if len(df_annotation) == 0:
        return [0, 0]

    numWf = len(df_annotation.workflowName)
    notAnnotatedWf = list(
        df_annotation[df_annotation.annotated == 0].workflowName)
    wfAnnotationScore = 100 - (len(notAnnotatedWf) / numWf * 100)

    return [wfAnnotationScore, notAnnotatedWf]

