import pandas as pd
import re


def populate_catch_dataframe(df_catches, filePath):
    temp_df_catches = pd.DataFrame(columns=['Catch Id', 'Screenshot Included', 'filePath', 'Log Message Included'])

    with open(filePath, encoding='utf-8', mode='r') as f:
        printLine = False
        activityList = []
        evaluate = False
        catchId = ''
        for line in f:
            if line.strip(" ").startswith('<Catch x:'):
                activityList = []
                printLine = not printLine
                if 'sap2010:WorkflowViewState.IdRef' in line:
                    name = re.search("sap2010:WorkflowViewState.IdRef=\"[^\"]*\"", line.strip(" ")).group(0)
                    catchId = name[len("sap2010:WorkflowViewState.IdRef=\""):-1]
            if '</Catch>' in line.strip(" "):
                printLine = not printLine
                evaluate = True
            if printLine and (catchId == ''):
                if ('<sap2010:WorkflowViewState.IdRef>' in line.strip(" ")) and \
                        ('</sap2010:WorkflowViewState.IdRef>' in line.strip(" ")) and \
                        ('Catch`' in line.strip(" ")):
                    catchId = re.search("Catch[^<]*", line.strip(" ")).group(0)
            if printLine and ('<Catch x:' not in line.strip(" ")):
                activityList.append(line.strip(" ").split(" ")[0].strip("<"))
            if evaluate:
                evaluate = False
                screenshotIncluded = False
                logMessageIncluded = False
                for i in activityList:
                    if 'ui:TakeScreenshot' == i:
                        screenshotIncluded = True
                    if 'ui:LogMessage' == i:
                        logMessageIncluded = True
                temp_df_catches = temp_df_catches.append({'Catch Id': catchId,
                                                          'Screenshot Included': screenshotIncluded,
                                                          'filePath': filePath,
                                                          'Log Message Included': logMessageIncluded},
                                                         ignore_index=True)
                catchId = ''
    return pd.concat([df_catches, temp_df_catches], ignore_index=True, sort=False)