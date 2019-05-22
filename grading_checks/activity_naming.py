import untangle
import pandas as pd
import re
import sys


def activity_naming_check(df_activity):
    # return lists
    df_activity['customizedName'] = (
        df_activity['activityName'] != df_activity['activityType'])
    activityNamingScore = len(df_activity[df_activity['customizedName'] == True].customizedName) / len(
        df_activity.customizedName) * 100
    improperNamedActivities = list(
        df_activity[df_activity['customizedName'] != True].activityName)

    return [activityNamingScore, improperNamedActivities]

def populate_activity_dataframe():
    with open(filePath, encoding='utf-8', mode='r') as f:
        for line in f:
            if 'DisplayName=' in line:
                name = re.search('DisplayName=\"[^\"]*\"',
                                 line.strip(' ')) \
                           .group(0)[len("DisplayName=\""):-1]
                activity = line.strip(' ').split(' ')[0].strip('<')
                activity = activity if 'ui:' not in activity else activity[3:]
                df_activity = df_activity.append({'activityName': name,
                                                  'activityType': activity,
                                                  'filePath': filePath},
                                                 ignore_index=True)