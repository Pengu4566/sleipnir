import inflection
import pandas as pd
# function module for naming
# 1. variable naming
# 2. argument naming
# 3. activity naming

# functions
# check camelcase
def check_cc(stringAfterUs):
    if inflection.camelize(stringAfterUs, uppercase_first_letter=False) != stringAfterUs:
        return "Not Camel Case"
    return ""

# check for abbreviation
def check_abb(variableType, stringBeforeUs):
    errorName = []
    # variable type is in dict above and format matches ['abbreviation''_''anything'] i.e.(int_counter, str_thing)
    dic_type_abbreviation = {'string': 'str', 'int32': 'int', 'datacolumn': 'dclm', 'double': 'dbl',
                             'dateTime': 'date', 'array': 'arr', 'list': 'lst', 'dictionary': 'dic',
                             'exception': 'ept', 'queueItem': 'qitm'}
    if variableType in dic_type_abbreviation.keys():
        if stringBeforeUs != dic_type_abbreviation[variableType]:
            return "No data type abbreviation"
    # variable type is not in above dict but format still matches ['abbreviation''_''anything']
    else:
        subString = stringBeforeUs
        for j in subString:
            if j not in variableType:
                return "No data type abbreviation"
            variableType = variableType[(variableType.find(j) + 1):]
    return ""

# end functions

# 1. variable naming: camelcase, abbreviation ahead of name

def grade_variable_name(df_variable):
    df_variable_dup = df_variable.copy()
    numVariables = len(df_variable_dup.variableName)

    # check if variable name is proper in df_variable ['variableType', 'variableName', 'count', 'filePath', 'projectId']
    def proper_variable_naming(df_variable_row):
        errorName = []
        variableName = df_variable_row['variableName']
        variableType = df_variable_row['variableType']

        # if "_" in the name
        if "_" in df_variable_row['variableName']:
            lst_subString = df_variable_row['variableName'].split("_")
            # if only one "_"
            if len(lst_subString) == 2:
                if check_abb(variableType, lst_subString[0]) == "":
                    errorName.append(check_abb(variableType, lst_subString[0]))
                    errorName.append(check_cc(lst_subString[1]))
                else:
                    errorName.append("No data type abbreviation")
                    errorName.append("Not Camel Case")
            else:
                # more than one "_", not camel case
                errorName.append("Not Camel Case")
                # check for abbreviation
                errorName.append(check_abb(variableType, lst_subString[0]))
        # if "_" not in the name
        else:
            errorName.append("No data type abbreviation")
            errorName.append(check_cc(variableName))
        return ", ".join([i for i in errorName if i != ""])

    if numVariables > 0:
        df_variable_dup['error'] = df_variable_dup.apply(proper_variable_naming, axis=1)
        df_variable_dup['properNamed'] = df_variable_dup.apply(lambda x: True if len(x["error"]) == 0 else False,
                                                               axis=1)
        df_variable_dup['type'] = "Variable Naming"
        df_variable_dup.rename(columns={'variableName': 'name', 'filePath': 'file', 'projectName': 'project'}, inplace=True)
        df_variable_dup['file'] = df_variable_dup.apply(lambda x: x['file'].replace(str(x['mainFolder']), ""), axis=1)
        # return lists
        improperNamedVariable = df_variable_dup.loc[df_variable_dup.properNamed == False].dropna()\
                                    .loc[:, ['name', 'file', 'type', 'error', 'project']]
        variableNamingScore = df_variable_dup.properNamed.sum() / numVariables * 100

    else:
        # improperNamedVariable = ['There is no variable in your project.']
        improperNamedVariable = pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])
        variableNamingScore = 0

    return [variableNamingScore, improperNamedVariable]

# end 1. variable naming


# 2. argument naming: in/out/io, abbreviation, camel case

def grade_argument_name(df_argument):
    numArgument = len(df_argument) / 100

    # check if argument name is proper in df_argument
    def proper(df_argument_row):
        errorName = []
        argumentName = df_argument_row['argumentName']
        argumentType = df_argument_row['argumentType']
        dataType = df_argument_row['dataType']

        if "_" in argumentName:
            lst_substring = argumentName.split("_")
            # check for in/out/io
            def check_io(argumentType, substring):
                if (argumentType == 'InArgument') and (substring[0] == 'in'):
                    return True
                elif (argumentType == 'OutArgument') and (substring[0] == 'out'):
                    return True
                elif (argumentType == 'InOutArgument') and (substring[0] == 'io'):
                    return True
                else:
                    return False

            ioBool = check_io(argumentType, lst_substring[0])

            if not ioBool:
                errorName.append("No argument type abbreviation")
                errorName.append(check_abb(dataType, lst_substring[0]))
                if len(lst_substring) == 2 and check_abb(dataType, lst_substring[0]) == "":
                    errorName.append(check_cc(lst_substring[1]))
                else:
                    errorName.append("Not Camel Case")
            else:
                errorName.append(check_abb(dataType, lst_substring[1]))
                if len(lst_substring) == 3 and check_abb(dataType, lst_substring[1]) == "":
                    errorName.append(check_cc(lst_substring[2]))
                else:
                    errorName.append("Not Camel Case")
        else:
            errorName.append("No argument type abbreviation")
            errorName.append("No data type abbreviation")
            errorName.append(check_cc(argumentName))
        return ", ".join([i for i in errorName if i != ""])

    if numArgument > 0:
        df_argument_dup = df_argument.copy()
        df_argument_dup['error'] = df_argument_dup.apply(proper, axis=1)
        df_argument_dup['properNamed'] = df_argument_dup.apply(lambda x: True if x['error']==[] else False, axis=1)
        # return lists
        argumentNamingScore = df_argument_dup.properNamed.sum() / numArgument
        df_argument_dup['type'] = "Argument Naming"
        df_argument_dup.rename(columns={'argumentName': 'name', 'filePath': 'file', 'projectName': 'project'},
                               inplace=True)
        df_argument_dup['file'] = df_argument_dup.apply(lambda x: x['file'].replace(str(x['mainFolder']), ""), axis=1)
        improperNamedArguments = df_argument_dup[df_argument_dup['properNamed'] == False].dropna()\
                                     .loc[:, ['name', 'file', 'type', 'error', 'project']]
    else:
        [argumentNamingScore, improperNamedArguments] = [0, pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])]

    return [argumentNamingScore, improperNamedArguments]

# 2. argument naming: in/out/io, abbreviation


# 3. activity naming

def grade_activity_name(df_activity):
    if len(df_activity['activityName']) > 0:
        # return lists
        df_activity['customizedName'] = (df_activity['activityName'] != df_activity['activityType'])
        df_activity_dup = df_activity.copy()
        # df_activity_dup.filePath = df_activity_dup.filePath.str.replace(fileLocationStr,'')
        activityNamingScore = df_activity_dup['customizedName'].sum() / len(df_activity_dup.customizedName) * 100
        df_activity_dup.rename(columns={'activityName': 'name', 'filePath': 'file', 'projectName': 'project'},
                               inplace=True)
        df_activity_dup['type'] = "Activity Naming"
        df_activity_dup['error'] = "Used activity default name"
        df_activity_dup['file'] = df_activity_dup.apply(lambda x: x['file'].replace(str(x['mainFolder']), ""), axis=1)
        improperNamedActivities = df_activity_dup[df_activity_dup['customizedName'] != True].dropna()\
                                      .loc[:, ['name', 'file', 'type', 'error', 'project']]
    else:
        [activityNamingScore, improperNamedActivities] = [0, pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])]

    return [activityNamingScore, improperNamedActivities]

# end 3. activity naming
