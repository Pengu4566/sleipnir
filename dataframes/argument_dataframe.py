import pandas as pd
import re
import xml.etree.ElementTree as ET


def populate_argument_dataframe(filePath):
    temp_df_argument = pd.DataFrame(columns=['argumentName', 'argumentType', 'filePath', 'dataType', 'count'])
    tree = ET.parse(filePath)
    root = tree.getroot()
    lst_args = root.findall('.//{http://schemas.microsoft.com/winfx/2006/xaml}Members')
    if len(lst_args) > 0:
        for member in lst_args:
            for arg in member.findall('.//'):
                argumentName = arg.attrib['Name']
                dataType = arg.attrib['Type'].split(":")[1].split(")")[0].split("(")[0].lower()
                argumentType = arg.attrib['Type'].split("(")[0]
                temp_df_argument = temp_df_argument.append({'argumentName': argumentName,
                                                            'argumentType': argumentType,
                                                            'filePath': filePath,
                                                            'dataType': dataType,
                                                            'count': 1},
                                                           ignore_index=True)

    if len(temp_df_argument['count']) > 0:
        with open(filePath, encoding='utf-8', mode='r') as f:
            lst_lines = f.readlines()
            f.close()

        def arg_count_file(df_row):
            def arg_count_line(argumentName, line):
                if re.search(('\[.*' + argumentName + '.*\]'), line) is not None:
                    return 1
                else:
                    return 0

            lst_count = list(map(arg_count_line, [df_row['argumentName']] * len(lst_lines), lst_lines))
            return sum(lst_count) + 1

        temp_df_argument['count'] = temp_df_argument.apply(arg_count_file, axis=1)

    return temp_df_argument
