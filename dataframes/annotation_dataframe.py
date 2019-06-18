import pandas as pd
import re


def populate_annotation_dataframe(df_annotation, filePath):
    temp_df_annotation = pd.DataFrame(columns=['workflowName', 'invokedBy'])
    with open(filePath, encoding='utf-8', mode='r') as f:
        numWfAnnotError = 0
        invokedBy = "/".join(filePath.split("/")[2:])

        for line in f:
            if (line.strip(" ").startswith("<ui:InvokeWorkflowFile") and
                    "WorkflowFileName=" in line.strip(" ")):
                try:
                    workflowName = re.search('WorkflowFileName=\"[^\"]*\.xaml\"', line.strip(" ")).group(0)
                    workflowName = workflowName[(len('WorkflowFileName="')):-6]
                    temp_df_annotation = temp_df_annotation.append({'workflowName': workflowName.replace("\\", "/"),
                                                                    'invokedBy': invokedBy.replace(".xaml", ""),
                                                                    'annotated': False,
                                                                    'annotation': ''},
                                                                   ignore_index=True)
                # no workflow name found in the invoke workflow block, need to be resolved
                except AttributeError:
                    numWfAnnotError += 1
    df_annotation = pd.concat([df_annotation, temp_df_annotation], ignore_index=True, sort=False).drop_duplicates()
    return df_annotation