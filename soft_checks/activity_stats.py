# activity stats
def get_activity_stats(df_activity):
    if len(df_activity['activityName']) > 0:
        html_string = "<h3 id='act_stat_header'>Activity Statistics</h3>"
        html_string += "<div id='stats_buttons'> <p id='stat_notes'>(Click on the file name to see details)</p>"
        for f in df_activity.filePath.unique():
            df_activity_gbPathType = df_activity[df_activity['filePath'] == f].loc[:, ['activityType']]\
                                                .groupby(['activityType']).size()
            df_activity_gbPathType = df_activity_gbPathType.reset_index()
            df_activity_gbPathType.columns = ['Activity Type', 'Count']
            df_activity_gbPathType = df_activity_gbPathType.loc[:].sort_values(by=['Count'], ascending= False)
            df_activity_gbPathType.reset_index(drop=True, inplace=True)
            df_activity_gbPathType = df_activity_gbPathType.to_html(justify="center")
            html_string += "<div class='act_stat'> <button>" + f + "</button>" + "<div class='stats_table'>" + df_activity_gbPathType + "</div></div>"
        html_string += "</div>"
        return html_string
    else:
        html_string = "<div class='act_stat'> <h3 id='act_stat_header'>Activity Statistics</h3> <p>There is no activity in your project.</p> </div>"
        return html_string
# end activity stats