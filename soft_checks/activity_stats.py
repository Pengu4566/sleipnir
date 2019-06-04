# activity stats
def get_activity_stats(df_activity):
    if len(df_activity['activityName']) > 0:
        html_string = "<p>Below is the activity statistics for each file of your project:</p>"
        for f in df_activity.filePath.unique():
            df_activity_gbPathType = df_activity[df_activity['filePath'] == f].loc[:, [ 'activityType']]\
                                                .groupby(['activityType']).size()
            df_activity_gbPathType = df_activity_gbPathType.reset_index()
            df_activity_gbPathType.columns = ['Activity Type', 'Count']
            df_activity_gbPathType = df_activity_gbPathType.loc[:].sort_values(by=['Count'], ascending= False)
            df_activity_gbPathType.reset_index(drop=True, inplace=True)
            df_activity_gbPathType = df_activity_gbPathType.to_html(justify="center")
            html_string += "<p>" + f + "</p>" + df_activity_gbPathType
        html_string += ("<p>" + "-" * 110 + "</p>")
        return html_string
    else:
        html_string = "<p>There is no activity in your project.</p>" + ("<p>" + "-" * 110 + "</p>")
        return html_string
# end activity stats