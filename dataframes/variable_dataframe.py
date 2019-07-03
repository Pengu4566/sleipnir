import pandas as pd
import re
import xml.etree.ElementTree as ET

def populate_variables_dataframe(filePath):
    temp_df_variable = pd.DataFrame(columns=['variableType', 'variableName', 'count', 'filePath'])
    tree = ET.parse(filePath)
    root = tree.getroot()
    lst_vars = root.findall('.//{http://schemas.microsoft.com/netfx/2009/xaml/activities}Variable')

    def extract_var_info(var):
        variableName = var.attrib['Name']
        dataType = var.attrib['{http://schemas.microsoft.com/winfx/2006/xaml}TypeArguments'].split(":")[1].lower()
        if '[]' in dataType:
            dataType = 'array'
        return {'variableType': dataType, 'variableName': variableName, 'count': 1, 'filePath': filePath}

    lst_processed = list(map(extract_var_info, lst_vars.copy()))

    for i in lst_processed:
        temp_df_variable = temp_df_variable.append(i, ignore_index=True)
    temp_df_variable.drop_duplicates(inplace=True)

    if len(temp_df_variable.variableName) > 0:
        with open(filePath, encoding='utf-8', mode='r') as f:
            lst_lines = f.readlines()
            f.close()

        def var_count_file(df_row):
            def var_count_line(variableName, line):
                if re.search(('\[.*' + variableName + '.*\]'), line) is not None:
                    return 1
                else:
                    return 0
            lst_count = list(map(var_count_line, [df_row['variableName']]*len(lst_lines), lst_lines))
            return sum(lst_count) + 1
        temp_df_variable['count'] = temp_df_variable.apply(var_count_file, axis=1)

    return temp_df_variable
