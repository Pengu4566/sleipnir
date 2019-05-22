import untangle
import pandas as pd
import re
import sys


def populate_try_catch_dataframe(filePath):

    df_trycatch = pd.DataFrame(columns=['Catch Id', 'Screenshot Included', 'filePath', 'Log Message Included'])

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
                    ('</sap2010:WorkflowViewState.IdRef>' in line.strip(" ")) and ('Catch`' in line.strip(" ")):
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
                df_trycatch = df_trycatch.append({'Catch Id': catchId,
                                                'Screenshot Included': screenshotIncluded,
                                                'filePath': filePath,
                                                'Log Message Included': logMessageIncluded},
                                                ignore_index=True)
                catchId = ''

    return df_trycatch


def grade_screenshot_in_trycatch(df_trycatch):
    # checks if df_trycatch length is zero and returns zeros for all scores
    if len(df_trycatch) == 0:
        return [0, 0]

    # checks if try/catch activities have screenshots within them
    if True in df_trycatch.groupby(['Screenshot Included']).size().index:
        numWSs = df_trycatch.groupby(['Screenshot Included']).size()[True]
    else:
        numWSs = 0

    if False in df_trycatch.groupby(['Screenshot Included']).size().index:
        noSsException = list(
            df_trycatch[df_trycatch['Screenshot Included'] == False]['Catch Id'])

    numCatch = len(df_trycatch['Screenshot Included'])

    if numCatch == 0:
        screenshotScore = 0
    else:
        screenshotScore = numWSs / numCatch * 100

    return [screenshotScore, noSsException]


def grade_log_message_in_trycatch(df_trycatch):

    # checks if df_trycatch length is zero and returns zeros for all scores
    if len(df_trycatch) == 0:
        return [0, 0]

    # checks if try/catch activities have log messages within them
    if True in df_trycatch.groupby(['Log Message Included']).size().index:
        numWLM = df_trycatch.groupby(['Log Message Included']).size()[True]
    else:
        numWLM = 0

    if False in df_trycatch.groupby(['Log Message Included']).size().index:
        noLMException = list(
            df_trycatch[df_trycatch['Log Message Included'] == False]['Catch Id'])

    numCatch = len(df_trycatch['Log Message Included'])
    logMessageScore = numWLM / numCatch * 100

    return [logMessageScore, noLMException]
