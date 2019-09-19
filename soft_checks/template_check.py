import pandas as pd

def check_template(df_json, df_annotation, df_activity, df_json_exp):
    # omit '_Test.xaml', 'Test_Framework/RunAllTests.xaml'
    df_json_dup = df_json.loc[:, ['index', 'mainFolder', 'subfiles', 'mainFile']]
    df_json_dup.subfiles = df_json_dup.apply(lambda x: [subfile.replace(x['mainFolder']+'/', '') for subfile in x['subfiles']], axis=1)
    df_annotation_dup = df_annotation.loc[:, ['mainFolder', 'workflowName', 'invokedBy']]

    qTempInvokingData = {'workflowName': ['Framework/InitAllSettings.xaml', 'Framework/Gen_KillProcessesOfUser.xaml',
                                                 'Framework/InitAllApplications.xaml', 'Framework/GetTransactionItem.xaml',
                                                  'Process.xaml', 'Framework/GetPerformanceMetrics.xaml',
                                                  'Framework/TakeScreenshot.xaml', 'Framework/CloseAllApplications.xaml',
                                                  'Framework/CreateStandardReport.xaml', 'Framework/TakeScreenshot.xaml',
                                                  'Framework/CloseAllApplications.xaml', 'Framework/KillAllProcesses.xaml'],
                                 'invokedBy': ['Main.xaml', 'Main.xaml', 'Main.xaml', 'Main.xaml', 'Main.xaml',
                                               'Main.xaml', 'Main.xaml', 'Main.xaml', 'Main.xaml', 'Framework/SetTransactionStatus.xaml',
                                               'Framework/SetTransactionStatus.xaml', 'Framework/SetTransactionStatus.xaml']}

    nqTempInvokingData = {'workflowName': ['Framework/InitAllSettings.xaml', 'Framework/Gen_KillProcessesOfUser.xaml',
                                           'Framework/InitAllApplications.xaml', 'Framework/GetTransactionData.xaml',
                                           'Framework/GetTransactionItem.xaml', 'Process.xaml',
                                           'Framework/GetPerformanceMetrics.xaml', 'Framework/TakeScreenshot.xaml',
                                           'Framework/CloseAllApplications.xaml', 'Framework/CreateStandardReport.xaml',
                                           'Framework/TakeScreenshot.xaml', 'Framework/CloseAllApplications.xaml',
                                           'Framework/KillAllProcesses.xaml'],
                          'invokedBy': ['Main.xaml', 'Main.xaml', 'Main.xaml', 'Main.xaml', 'Main.xaml', 'Main.xaml',
                                        'Main.xaml', 'Main.xaml', 'Main.xaml', 'Main.xaml',
                                        'Framework/SetTransactionStatus.xaml', 'Framework/SetTransactionStatus.xaml',
                                        'Framework/SetTransactionStatus.xaml']}

    nrTempInvokingData = {'workflowName': ['Framework/InitAllSettings.xaml', 'Framework/Gen_KillProcessesOfUser.xaml',
                                           'Framework/InitAllApplications.xaml', 'Process.xaml',
                                           'Framework/TakeScreenshot.xaml', 'Framework/CreateStandardReport.xaml',
                                           'Framework/CloseAllApplications.xaml'],
                          'invokedBy': ['Main.xaml', 'Main.xaml', 'Main.xaml', 'Main.xaml', 'Main.xaml',
                                        'Main.xaml', 'Main.xaml']}

    df_qTempInvoking = pd.DataFrame(data=qTempInvokingData)
    # df_qTempInvoking.to_csv('./qTempInvoke.csv')
    df_nqTempInvoking = pd.DataFrame(data=nqTempInvokingData)
    # df_nqTempInvoking.to_csv('./nqTempInvoke.csv')
    df_nrTempInvoking = pd.DataFrame(data=nrTempInvokingData)
    # df_nrTempInvoking.to_csv('./nrTempInvoke.csv')

    if len(df_annotation_dup) > 0:

        df_annotation_dup.workflowName = df_annotation_dup.apply(lambda x: x['workflowName']
                                                                 .replace(x['mainFolder']+'/', ''), axis=1)
        df_annotation_dup.invokedBy = df_annotation_dup.apply(lambda x: x['invokedBy']
                                                              .replace(x['mainFolder']+'/', ''), axis=1)
        df_temp_invoking_check = pd.merge(df_annotation_dup, df_qTempInvoking, on=['workflowName', 'invokedBy'],
                                          how='left', indicator='qTempInvoke')

        df_temp_invoking_check = pd.merge(df_temp_invoking_check, df_nqTempInvoking, on=['workflowName', 'invokedBy'],
                                          how='left', indicator='nqTempInvoke')

        df_temp_invoking_check = pd.merge(df_temp_invoking_check, df_nrTempInvoking, on=['workflowName', 'invokedBy'],
                                          how='left', indicator='nrTempInvoke')

        df_temp_invoking_check['qTempInvoke'] = df_temp_invoking_check.apply(
            lambda x: True if x['qTempInvoke'] == 'both' else False,
            axis=1)
        df_temp_invoking_check['nqTempInvoke'] = df_temp_invoking_check.apply(
            lambda x: True if x['nqTempInvoke'] == 'both' else False,
            axis=1)
        df_temp_invoking_check['nrTempInvoke'] = df_temp_invoking_check.apply(
            lambda x: True if x['nrTempInvoke'] == 'both' else False,
            axis=1)

        # df = df_temp_invoking_check.loc[:, ['workflowName', 'invokedBy', 'qTempInvoke', 'nqTempInvoke', 'nrTempInvoke']]
        # df.to_csv('./test.csv')
        df_match_invoke_byProject = df_temp_invoking_check.groupby('mainFolder')[
            'qTempInvoke', 'nqTempInvoke', 'nrTempInvoke'].sum().reset_index(drop=False)
        df_match_invoke_byProject.qTempInvoke = df_match_invoke_byProject.qTempInvoke == len(df_qTempInvoking)
        df_match_invoke_byProject.nqTempInvoke = df_match_invoke_byProject.nqTempInvoke == len(df_nqTempInvoking)
        df_match_invoke_byProject.nrTempInvoke = df_match_invoke_byProject.nrTempInvoke == len(df_nrTempInvoking)
        df_json_dup = pd.merge(df_json_dup, df_match_invoke_byProject, on=['mainFolder'], how='left')
        # df_json_dup.to_csv("./test2.csv")
    else:
        df_match_invoke_byProject = df_annotation_dup.copy().loc[:,["mainFolder"]]
        df_match_invoke_byProject["qTempInvoke"] = False
        df_match_invoke_byProject["nqTempInvoke"] = False
        df_match_invoke_byProject["nrTempInvoke"] = False
        df_json_dup = pd.merge(df_json_dup, df_match_invoke_byProject, on=['mainFolder'], how='left')

    df_activity_dup = df_activity.loc[:, ['activityType', 'filePath']]
    df_json_dup['StateMachine'] = df_json_dup.apply(lambda x: 'StateMachine' in list(df_activity_dup[df_activity_dup['filePath']==x['mainFile']].activityType), axis=1)

    df_json_exp_dup = df_json_exp.copy()
    df_activity_dup = pd.merge(df_activity_dup, df_json_exp_dup, on=['filePath'], how='left')
    df_json_dup['AddQItem'] = df_json_dup.apply(lambda x: 'AddQueueItem' in list(df_activity_dup[df_activity_dup['projectId']==x['index']]['activityType']), axis=1)
    df_json_dup['AddTItem'] = df_json_dup.apply(lambda x: 'AddTransactionItem' in list(df_activity_dup[df_activity_dup['projectId']==x['index']]['activityType']), axis=1)
    df_json_dup['BulkAddQItems'] = df_json_dup.apply(lambda x: 'BulkAddQueueItems' in list(df_activity_dup[df_activity_dup['projectId']==x['index']]['activityType']), axis=1)
    df_json_dup['GetQItems'] = df_json_dup.apply(lambda x: 'GetQueueItems' in list(df_activity_dup[df_activity_dup['projectId']==x['index']]['activityType']), axis=1)
    df_json_dup['GetTItem'] = df_json_dup.apply(lambda x: 'GetQueueItem' in list(df_activity_dup[df_activity_dup['projectId']==x['index']]['activityType']), axis=1)
    df_json_dup['Dispatcher'] = df_json_dup.apply(lambda x: x['AddQItem'] or x['AddTItem'] or x['BulkAddQItems'], axis=1)
    df_json_dup['Performer'] = df_json_dup.apply(lambda x: x['GetQItems'] or x['GetTItem'], axis=1)

    def template_comment(df_row):
        if all([df_row['Dispatcher'], not df_row['Performer']]):
            if any([df_row['qTempInvoke'], df_row['nqTempInvoke'], df_row['nrTempInvoke']]):
                return "Dispatcher using AKOA template."
            elif df_row['StateMachine']:
                return "Dispatcher not using AKOA template, but using State Machine."
            else:
                return "Dispatcher using neither AKOA template nor State Machine."
        elif all([df_row['Performer'], not df_row['Dispatcher']]):
            if any([df_row['qTempInvoke'], df_row['nqTempInvoke'], df_row['nrTempInvoke']]):
                return "Performer using AKOA template."
            elif df_row['StateMachine']:
                return "Performer not using AKOA template, but using State Machine."
            else:
                return "Performer using neither AKOA template nor State Machine."
        elif all([df_row['Performer'], df_row['Dispatcher']]):
            if any([df_row['qTempInvoke'], df_row['nqTempInvoke'], df_row['nrTempInvoke']]):
                return "Bridge performer using AKOA template."
            elif df_row['StateMachine']:
                return "Bridge performer not using AKOA template, but using State Machine."
            else:
                return "Bridge performer using neither AKOA template nor State Machine."
        else:
            return "Neither dispatcher nor performer."

    df_json_dup['template_comment'] = df_json_dup.apply(template_comment, axis=1)

    # df_json_dup.to_csv('./test3.csv')
    return df_json_dup.loc[:, ['index', 'template_comment']]

