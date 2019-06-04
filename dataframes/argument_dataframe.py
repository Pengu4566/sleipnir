import untangle
import pandas as pd
import re


def populate_argument_dataframe(df_argument, filePath):
    temp_df_argument = pd.DataFrame(columns=['argumentName', 'argumentType', 'filePath', 'dataType', 'count'])
    with open(filePath, encoding='utf-8', mode='r') as f:
        printLine = False
        style = 1
        for line in f:
            if 'ui:InvokeWorkflowFile.Arguments>' in line.strip(" "):
                printLine = not printLine
                style = 1
            if printLine and ('ui:InvokeWorkflowFile.Arguments>' not in line.strip(" ")) and (style == 1):
                argumentName = untangle.parse(line.strip(" ")).children[0]['x:Key']
                dataType = untangle.parse(line.strip(" ")).children[0]['x:TypeArguments'].split(":")[1].split("(")[0]
                argumentType = untangle.parse(line.strip(" ")).children[0]._name
                if argumentName != None:
                    temp_df_argument = temp_df_argument.append({'argumentName': argumentName,
                                                                'argumentType': argumentType,
                                                                'filePath': filePath,
                                                                'dataType': dataType,
                                                                'count': 1},
                                                                ignore_index=True)

            if ('<x:Members>' in line.strip(" ")) or ('</x:Members>' in line.strip(" ")):
                printLine = not printLine
                style = 2
            if printLine and ('<x:Members>' not in line.strip(" ")) and (style == 2):
                argumentName = untangle.parse(line.strip(" ")).children[0]['Name']
                temp_argumentType = untangle.parse(line.strip(" ")).children[0]['Type']
                argumentType = temp_argumentType[:temp_argumentType.index('(')]
                dataType = temp_argumentType[temp_argumentType.index('('):-1].split(":")[1].split("(")[0]
                if argumentName != None:
                    temp_df_argument = temp_df_argument.append({'argumentName': argumentName,
                                                                'argumentType': argumentType,
                                                                'filePath': filePath,
                                                                'dataType': dataType,
                                                                'count': 1},
                                                                ignore_index=True)
    if len(temp_df_argument['count']) > 0:
        with open(filePath, encoding='utf-8', mode='r') as f:
            for line in f:
                for index, row in temp_df_argument.iterrows():
                    # need to fix
                    if (re.search(('\[.*' + row['argumentName'] + '.*\]'), line) is not None) and (filePath == row['filePath']):
                        row['count'] += 1
        return pd.concat([df_argument,temp_df_argument], ignore_index=True, sort=False)
    else:
        return df_argument