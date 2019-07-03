import pandas as pd
import xml.etree.ElementTree as ET


def populate_activity_dataframe(filePath):
    temp_df_activity = pd.DataFrame(columns=['activityName', 'activityType', 'filePath'])
    tree = ET.parse(filePath)
    root = tree.getroot()
    lst_acts = root.findall('.//')

    def extract_act_info(act):
        if '{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}WorkflowViewState.IdRef' in act.attrib.keys():
            try:
                name = act.attrib['DisplayName']
                activity = act.attrib[
                    '{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}WorkflowViewState.IdRef'].split(
                    "_")[0]
            except Exception:
                name = activity = act.attrib['{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}WorkflowViewState.IdRef'].split("_")[0]

            return {'activityName': name, 'activityType': activity, 'filePath': filePath}
        else:
            return None

    lst_df_act_rows = list(filter(lambda x: x is not None, list(map(extract_act_info, lst_acts))))

    for df_row in lst_df_act_rows:
        temp_df_activity = temp_df_activity.append(df_row, ignore_index=True)

    return temp_df_activity