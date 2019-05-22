import untangle
import pandas as pd
import re
import sys


# check invoke workflow annotation
def checkWfAnnotation(df_annotation):
    numWf = len(df_annotation.workflowName)
    notAnnotatedWf = list(
        df_annotation[df_annotation.annotated == 0].workflowName)
    wfAnnotationScore = 100 - (len(notAnnotatedWf) / numWf * 100)

    return [wfAnnotationScore, notAnnotatedWf]


# end check invoke workflow annotation


# annotation dataframe
def populate_workflow_annotation_dataframe():
    with open(filePath, encoding='utf-8', mode='r') as f:
        for line in f:
            if (line.strip(" ").startswith("<ui:InvokeWorkflowFile") and "WorkflowFileName=" in line.strip(" ")):
                workflowName = re.search('WorkflowFileName=\"[^\"]*\.xaml\"', line.strip(" ")).group(0)
                workflowName = workflowName[(len('WorkflowFileName="')):-1]
                df_annotation = df_annotation.append({'workflowName': workflowName, 'annotated': False}, ignore_index=True)
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
    # end annotation dataframe