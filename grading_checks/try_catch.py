import untangle
import pandas as pd
import re
import sys


# checks for log messages and screenshots in trycatch
def populate_try_catch_dataframe():
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
                        name = re.search("sap2010:WorkflowViewState.IdRef=\"[^\"]*\"",
                                         line.strip(" ")).group(0)
                        catchId = name[len(
                            "sap2010:WorkflowViewState.IdRef=\""):-1]
                if '</Catch>' in line.strip(" "):
                    printLine = not printLine
                    evaluate = True
                if printLine and (catchId == ''):
                    if ('<sap2010:WorkflowViewState.IdRef>' in line.strip(" ")) and \
                            ('</sap2010:WorkflowViewState.IdRef>' in line.strip(" ")) and \
                            ('Catch`' in line.strip(" ")):
                        catchId = re.search(
                            "Catch[^<]*", line.strip(" ")).group(0)
                if printLine and ('<Catch x:' not in line.strip(" ")):
                    activityList.append(line.strip(
                        " ").split(" ")[0].strip("<"))
                if evaluate:
                    evaluate = False
                    screenshotIncluded = False
                    logMessageIncluded = False
                    for i in activityList:
                        if 'ui:TakeScreenshot' == i:
                            screenshotIncluded = True
                        if 'ui:LogMessage' == i:
                            logMessageIncluded = True
                    df_catches = df_catches.append({'Catch Id': catchId,
                                                    'Screenshot Included':
                                                        screenshotIncluded,
                                                    'filePath': filePath,
                                                    'Log Message Included':
                                                        logMessageIncluded},
                                                   ignore_index=True)
                    catchId = ''
        # end try catch dataframe

# screenshot in try catch block
def CheckSsinTC(df_catches):
    # checks if try/catch activities have screenshots within them
    if True in df_catches.groupby(['Screenshot Included']).size().index:
        numWSs = df_catches.groupby(['Screenshot Included']).size()[True]
    else:
        numWSs = 0

    if False in df_catches.groupby(['Screenshot Included']).size().index:
        noSsException = list(
            df_catches[df_catches['Screenshot Included'] == False]['Catch Id'])

    numCatch = len(df_catches['Screenshot Included'])

    if numCatch == 0:
        screenshotScore = 0
    else:
        screenshotScore = numWSs / numCatch * 100

    return [screenshotScore, noSsException]


# end screenshot in try catch block

# check log message in try catch
def CheckLMinTC(df_catches):
    # checks if try/catch activities have log messages within them
    if True in df_catches.groupby(['Log Message Included']).size().index:
        numWLM = df_catches.groupby(['Log Message Included']).size()[True]
    else:
        numWLM = 0

    if False in df_catches.groupby(['Log Message Included']).size().index:
        noLMException = list(
            df_catches[df_catches['Log Message Included'] == False]['Catch Id'])

    numCatch = len(df_catches['Log Message Included'])
    logMessageScore = numWLM / numCatch * 100

    return [logMessageScore, noLMException]


# end check log message in try catch