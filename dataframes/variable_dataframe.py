import untangle
import pandas as pd
import re
import xml

def populate_variables_dataframe(df_variable, filePath):
    temp_df_variable = pd.DataFrame(columns=['variableType', 'variableName', 'count', 'filePath'])
    # capture variables bound by tags
    with open(filePath, encoding='utf-8', mode='r') as f:
        for line in f:
            if line.strip(" ").startswith('<Variable x:'):
                try:
                    variableName = untangle.parse(line.strip(" ")).children[0]['Name']
                    dataType = untangle.parse(line.strip(" ")).children[0]['x:TypeArguments'].split(":")[1]\
                        .split("(")[0].lower()
                except xml.sax._exceptions.SAXParseException:
                    variableName = re.search("Name=\"[^\"]*\"", line).group(0).replace("Name='", "").replace("'", "")
                    dataType = re.search("x:TypeArguments=\"[^\"]*\"", line).group(0).split(":")[1].split("(")[0].lower()
                if '[]' in dataType:
                    dataType = 'array'
                if filePath not in list(df_variable[df_variable.variableName == variableName].filePath):
                    temp_df_variable = temp_df_variable.append({'variableType': dataType, 'variableName': variableName,
                                                                'count': 1, 'filePath': filePath}, ignore_index=True)
    if len(temp_df_variable.variableName) > 0:
        with open(filePath, encoding='utf-8', mode='r') as f:
            for line in f:
                for index, row in temp_df_variable.iterrows():
                    if (re.search(('\[.*' + row['variableName'] + '.*\]'), line) is not None) and (filePath == row['filePath']):
                        row['count'] += 1
        return pd.concat([df_variable,temp_df_variable], ignore_index=True, sort=False)
    else:
        return df_variable