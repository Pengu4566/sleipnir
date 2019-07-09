import pandas as pd
import re
import xml.etree.ElementTree as ET

def populate_dataframe(filePath):

    tree = ET.parse(filePath)
    root = tree.getroot()

    lst_vars = root.findall('.//{http://schemas.microsoft.com/netfx/2009/xaml/activities}Variable')
    lst_args = root.findall('.//{http://schemas.microsoft.com/winfx/2006/xaml}Members//')
    lst_catches = root.findall('.//{http://schemas.microsoft.com/netfx/2009/xaml/activities}Catch')
    lst_acts = root.findall('.//')
    lst_invokes = root.findall('.//{http://schemas.uipath.com/workflow/activities}InvokeWorkflowFile')
    invokedBy = filePath.replace(".xaml", "")

    # variables
    def extract_var_info(var):
        variableName = var.attrib['Name']
        dataType = var.attrib['{http://schemas.microsoft.com/winfx/2006/xaml}TypeArguments'].split(":")[1].lower()
        if '[]' in dataType:
            dataType = 'array'
        return pd.DataFrame.from_dict({'variableType': [dataType],
                                       'variableName': [variableName],
                                       'count': [1],
                                       'filePath': [filePath]})

    lst_var_processed = list(map(extract_var_info, lst_vars.copy()))

    if len(lst_var_processed) > 0:
        temp_df_variable = pd.concat(lst_var_processed, ignore_index=True)
        temp_df_variable.drop_duplicates(inplace=True)
    else:
        temp_df_variable = pd.DataFrame(columns=['variableType', 'variableName', 'count', 'filePath'])

    if len(temp_df_variable.variableName) > 0:
        with open(filePath, encoding='utf-8', mode='r') as f:
            lst_lines = f.readlines()
            f.close()

        def var_count_file(df_row):
            def var_count_line(variableName, line):
                if re.search(('\[.*' + variableName + '.*\]'), line) is not None:
                    return 1
                else:
                    return 0
            lst_count = list(map(var_count_line, [df_row['variableName']]*len(lst_lines), lst_lines))
            return sum(lst_count) + 1
        temp_df_variable['count'] = temp_df_variable.apply(var_count_file, axis=1)

    # arguments
    if len(lst_args) > 0:
        def extract_arg_info(arg):
            argumentName = arg.attrib['Name']
            dataType = arg.attrib['Type'].split(":")[1].split(")")[0].split("(")[0].lower()
            if '[]' in dataType:
                dataType = 'array'
            argumentType = arg.attrib['Type'].split("(")[0]
            return pd.DataFrame.from_dict({'argumentName': [argumentName],
                                           'argumentType': [argumentType],
                                           'filePath': [filePath],
                                           'dataType': [dataType],
                                           'count': [1]})
        lst_arg_processed = list(map(extract_arg_info, lst_args.copy()))
        if len(lst_arg_processed) > 0:
            temp_df_argument = pd.concat(lst_arg_processed, ignore_index=True)
            temp_df_argument.drop_duplicates(inplace=True)
            lst_text = list(filter(lambda x: x.startswith("["),
                                   list(filter(lambda x: x is not None, [ele.text for ele in root.findall('.//')]))))
            lst_attrib = list(filter(lambda x: len(x.keys()) > 0, [ele.attrib for ele in root.findall('.//')]))
            lst_search = sum([list(x.values()) for x in lst_attrib], []) + lst_text

            def arg_count_file(df_row):
                argName = df_row.argumentName

                def arg_match(argName, ele_search):
                    if argName in ele_search:
                        return 1
                    else:
                        return 0

                lst_count = list(map(arg_match, [argName] * len(lst_search), lst_search))
                return sum(lst_count)

            temp_df_argument['count'] = temp_df_argument.apply(arg_count_file, axis=1)
    else:
        temp_df_argument = pd.DataFrame(columns=['argumentName', 'argumentType', 'filePath', 'dataType', 'count'])


    # catches
    def extract_catch_content(catch):
        try:
            catchId = catch.attrib['{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}WorkflowViewState.IdRef']
        except Exception:
            catchId = catch.find('./{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}WorkflowViewState.IdRef').text
        screenshotIncluded = True if len(
                catch.findall('.//{http://schemas.uipath.com/workflow/activities}TakeScreenshot')) > 0 else False
        logMessageIncluded = True if len(
                catch.findall('.//{http://schemas.uipath.com/workflow/activities}LogMessage')) > 0 else False

        return pd.DataFrame.from_dict({'Catch Id': [catchId],
                                       'Screenshot Included': [screenshotIncluded],
                                       'filePath': [filePath],
                                       'Log Message Included': [logMessageIncluded]})

    lst_df_catch_rows = list(map(extract_catch_content, lst_catches))
    if len(lst_df_catch_rows) > 0:
        temp_df_catches = pd.concat(lst_df_catch_rows, ignore_index=True)
    else:
        temp_df_catches = pd.DataFrame(columns=['Catch Id', 'Screenshot Included', 'filePath', 'Log Message Included'])


    # activities
    def extract_act_info(act):
        if '{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}WorkflowViewState.IdRef' in act.attrib.keys():
            try:
                name = act.attrib['DisplayName']
                activity = act.attrib[
                    '{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}WorkflowViewState.IdRef'].split(
                    "_")[0]
            except Exception:
                name = activity = act.attrib['{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}WorkflowViewState.IdRef'].split("_")[0]

            return pd.DataFrame.from_dict({'activityName': [name],
                                           'activityType': [activity],
                                           'filePath': [filePath]})
        else:
            return None

    lst_df_act_rows = list(filter(lambda x: x is not None, list(map(extract_act_info, lst_acts))))

    # for df_row in lst_df_act_rows:
    #     temp_df_activity = temp_df_activity.append(df_row, ignore_index=True)
    if len(lst_df_act_rows) > 0:
        temp_df_activity = pd.concat(lst_df_act_rows, ignore_index=True)
    else:
        temp_df_activity = pd.DataFrame(columns=['activityName', 'activityType', 'filePath'])


    # annotations
    if len(lst_invokes) > 0:

        def extract_invoke_info(invoke):
            workflowName = invoke.attrib['WorkflowFileName'].replace("\\", "/").replace(".xaml","")
            return pd.DataFrame.from_dict({'workflowName': [workflowName],
                                           'invokedBy': [invokedBy],
                                           'annotated': [False],
                                           'annotation': ['']})

        lst_df_annot_rows = list(map(extract_invoke_info, lst_invokes))

        temp_df_annotation = pd.concat(lst_df_annot_rows, ignore_index=True)
    else:
        temp_df_annotation = pd.DataFrame(columns=['workflowName', 'invokedBy', 'annotated', 'annotation'])

    return [temp_df_variable, temp_df_argument, temp_df_catches, temp_df_activity, temp_df_annotation]
