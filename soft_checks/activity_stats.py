import pandas as pd

# activity stats
def get_activity_stats(df_activity):
    if len(df_activity['activityName']) > 0:
        df_activity_dup = df_activity.copy()
        df_activity_dup['filePath'] = df_activity_dup.apply(lambda x: x['filePath'].replace(str(x['mainFolder']), ''), axis=1)
        df_activity_dup = df_activity_dup.loc[:, ['activityType', 'filePath', 'projectName']]
        df_activity_dup = df_activity_dup.groupby(['activityType', 'filePath', 'projectName']).size().reset_index(drop=False)
        df_activity_dup.columns = ['activityType', 'file', 'project', 'count']
        df_activity_dup.fillna("Unknown", inplace=True)
        return df_activity_dup
    else:
        return pd.DataFrame(columns=['activityType', 'file', 'project', 'count'])

# end activity stats