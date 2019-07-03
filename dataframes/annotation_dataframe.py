import pandas as pd
import xml.etree.ElementTree as ET


def populate_annotation_dataframe(filePath):
    temp_df_annotation = pd.DataFrame(columns=['workflowName', 'invokedBy', 'annotated', 'annotation'])
    tree = ET.parse(filePath)
    root = tree.getroot()
    lst_invokes = root.findall('.//{http://schemas.uipath.com/workflow/activities}InvokeWorkflowFile')
    invokedBy = filePath.replace(".xaml", "")

    if len(lst_invokes) > 0:

        def extract_invoke_info(invoke):
            workflowName = invoke.attrib['WorkflowFileName'].replace("\\", "/").replace(".xaml","")
            return {'workflowName': workflowName, 'invokedBy': invokedBy,
                    'annotated': False, 'annotation': ''}

        lst_df_annot_rows = list(map(extract_invoke_info, lst_invokes))

        for df_row in lst_df_annot_rows:
            temp_df_annotation = temp_df_annotation.append(df_row, ignore_index=True)

    return temp_df_annotation