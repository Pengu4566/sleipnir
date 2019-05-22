import untangle
import pandas as pd
import re
import sys


def populate_activity_dataframe(filePath):

    # init dataframe
    df_activity = pd.DataFrame(columns=['activityName', 'activityType', 'filePath'])

    with open(filePath, encoding='utf-8', mode='r') as f:
        for line in f:
            if 'sap2010:WorkflowViewState.IdRef=' in line:
                if 'DisplayName=' in line:
                    name = re.search('DisplayName=\"[^\"]*\"',
                                     line.strip(' ')) \
                               .group(0)[len("DisplayName=\""):-1]
                    activity = line.strip(' ').split(' ')[0].strip('<')
                    activity = activity if 'ui:' not in activity else activity[3:]
                else:
                    activity = line.strip(' ').split(' ')[0].strip('<')
                    activity = activity if 'ui:' not in activity else activity[3:]
                    name = activity
                df_activity = df_activity.append({'activityName': name,
                                                  'activityType': activity,
                                                  'filePath': filePath},
                                                 ignore_index=True)
    return df_activity


def grade_activity_naming(df_activity):

    # checks if df_activity length is zero and returns zeros for all scores
    if len(df_activity) == 0:
        return [0, 0]

    # return lists
    df_activity['customizedName'] = (
        df_activity['activityName'] != df_activity['activityType'])
    activityNamingScore = len(df_activity[df_activity['customizedName'] == True].customizedName) / len(
        df_activity.customizedName) * 100
    improperNamedActivities = list(
        df_activity[df_activity['customizedName'] != True].activityName)

    return [activityNamingScore, improperNamedActivities]




