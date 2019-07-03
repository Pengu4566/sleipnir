import pandas as pd
import xml.etree.ElementTree as ET


def populate_catch_dataframe(filePath):
    temp_df_catches = pd.DataFrame(columns=['Catch Id', 'Screenshot Included', 'filePath', 'Log Message Included'])
    tree = ET.parse(filePath)
    root = tree.getroot()
    lst_catches = root.findall('.//{http://schemas.microsoft.com/netfx/2009/xaml/activities}Catch')

    def extract_catch_content(catch):
        catchId = catch.attrib['{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}WorkflowViewState.IdRef']
        screenshotIncluded = True if len(catch.findall('.//{http://schemas.uipath.com/workflow/activities}TakeScreenshot'))>0 else False
        logMessageIncluded = True if len(catch.findall('.//{http://schemas.uipath.com/workflow/activities}LogMessage'))>0 else False

        return {'Catch Id': catchId, 'Screenshot Included': screenshotIncluded, 'filePath': filePath, 'Log Message Included': logMessageIncluded}

    lst_df_catch_rows = list(map(extract_catch_content, lst_catches))
    if len(lst_df_catch_rows) > 0:
        for df_row in lst_df_catch_rows:
            temp_df_catches = temp_df_catches.append(df_row, ignore_index=True)

    return temp_df_catches