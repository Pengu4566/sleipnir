import pandas as pd
import re


def populate_activity_dataframe(df_activity, filePath):
    temp_df_activity = pd.DataFrame(columns=['activityName', 'activityType', 'filePath'])
    with open(filePath, encoding='utf-8', mode='r') as f:
        for line in f:
            if ('sap2010:WorkflowViewState.IdRef=' in line) and ('<Activity' not in line):
                if 'DisplayName=' in line:
                    name = re.search('DisplayName=\"[^\"]*\"', line.strip(' ')).group(0)[len("DisplayName=\""):-1]
                    activity = line.strip(' ').split(' ')[0].strip('<')
                    activity = activity if 'ui:' not in activity else activity[3:]
                else:
                    activity = line.strip(' ').split(' ')[0].strip('<')
                    activity = activity if 'ui:' not in activity else activity[3:]
                    name = activity
                temp_df_activity = temp_df_activity.append({'activityName': name,
                                                            'activityType': activity,
                                                            'filePath': filePath},
                                                           ignore_index=True)

    return pd.concat([df_activity, temp_df_activity], ignore_index=True, sort=False)