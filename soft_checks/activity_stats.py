import pandas as pd

# activity stats
def get_activity_stats(df_activity, fileLocationStr, df_json, df_annotation):
    if len(df_activity['activityName']) > 0:
        df_activity_dup = df_activity.loc[:, ['activityType', 'filePath']]
        df_activity_dup = df_activity_dup.groupby(['activityType', 'filePath']).size().reset_index(drop=False)
        df_activity_dup.columns = ['activityType', 'filePath', 'count']
        df_json_dup = pd.DataFrame(df_json.subfiles.tolist(), index=df_json['index']).stack().reset_index()
        df_json_dup.columns = ['projectId', 'fileIndex', 'filePath']
        df_json_dup.drop(columns=['fileIndex'], inplace=True)
        df_activity_dup = df_activity_dup.merge(df_json_dup, on='filePath', how='left')
        df_activity_dup.fillna("Unknown", inplace=True)
        df_activity_dup.filePath = df_activity_dup.filePath.str.replace(fileLocationStr, "").replace(".xaml", '')
        lst_activity_dup_byProject = list(df_activity_dup.groupby(['activityType', 'projectId'])['count'].sum()
                                          .reset_index(drop=False).reset_index().T.to_dict().values())
        return {"byFile": list(df_activity_dup.reset_index().T.to_dict().values()),
                "byProject": lst_activity_dup_byProject}
    else:
        return ["There is no activity in files you uploaded."]

# end activity stats