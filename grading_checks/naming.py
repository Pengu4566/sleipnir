import inflection
# function module for naming
# 1. variable naming
# 2. argument naming
# 3. activity naming

# functions
# check camelcase
def check_cc(stringAfterUs):
    errorName = []
    if inflection.camelize(stringAfterUs, uppercase_first_letter=False) != stringAfterUs:
        errorName.append("Not Camel Case")
    return errorName

# check for abbreviation
def check_abb(variableType, stringBeforeUs):
    errorName = []
    # variable type is in dict above and format matches ['abbreviation''_''anything'] i.e.(int_counter, str_thing)
    dic_type_abbreviation = {'string': 'str', 'int32': 'int', 'datacolumn': 'dclm', 'double': 'dbl',
                             'dateTime': 'date', 'array': 'arr', 'list': 'lst', 'dictionary': 'dic',
                             'exception': 'ept', 'queueItem': 'qitm'}
    if variableType in dic_type_abbreviation.keys():
        if stringBeforeUs != dic_type_abbreviation[variableType] + '_':
            errorName.append("No data type abbreviation")
    # variable type is not in above dict but format still matches ['abbreviation''_''anything']
    else:
        subString = stringBeforeUs
        for j in subString:
            if j not in variableType:
                errorName.append("No data type abbreviation")
                break
            variableType = variableType[(variableType.find(j) + 1):]
    return errorName

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
                errorName = check_cc(lst_subString[1]) + check_abb(variableType, lst_subString[0])

            else:
                # more than one "_", not camel case
                errorName.append("Not Camel Case")
                # check for abbreviation
                errorName += check_abb(variableType, variableName)
        # if "_" not in the name
        else:
            errorName.append("No data type abbreviation")
            errorName += check_cc(variableName)
        return errorName

    if numVariables > 0:
        df_variable_dup['error'] = df_variable_dup.apply(proper_variable_naming, axis=1)
        df_variable_dup['properNamed'] = df_variable_dup.apply(lambda x: True if len(x["error"]) == 0 else False,
                                                               axis=1)
        df_variable_dup['type'] = "Variable Naming"
        df_variable_dup.rename(columns={'variableName': 'name', 'filePath': 'file', 'projectId': 'project'}, inplace=True)
        # return lists
        if (False in df_variable_dup.properNamed) and (True in df_variable_dup.properNamed):
            improperNamedVariable = list(df_variable_dup.loc[df_variable_dup.properNamed == False]
                                         .loc[:, ['name', 'file', 'type', 'error', 'project']]
                                         .T.to_dict().values())
            variableNamingScore = df_variable_dup.properNamed.sum() / numVariables * 100
        elif True in df_variable_dup.properNamed:
            # improperNamedVariable = ['There is no improperly named variable.']
            improperNamedVariable = []
            variableNamingScore = 100
        else:
            improperNamedVariable = list(df_variable_dup.loc[:, ['name', 'file', 'type', 'error', 'project']]
                                         .T.to_dict().values())
            variableNamingScore = 0
    else:
        # improperNamedVariable = ['There is no variable in your project.']
        improperNamedVariable = []
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
                errorName += check_abb(dataType, lst_substring[0])
                if len(lst_substring) == 2 and check_abb(dataType, lst_substring[0]) == []:
                    errorName += check_cc(lst_substring[1])
                else:
                    errorName.append("Not Camel Case")
            else:
                errorName += check_abb(dataType, lst_substring[1])
                if len(lst_substring) == 3 and check_abb(dataType, lst_substring[1])==[]:
                    errorName += check_cc(lst_substring[2])
                else:
                    errorName.append("Not Camel Case")
        else:
            errorName.append("No argument type abbreviation")
            errorName.append("No data type abbreviation")
            errorName += check_cc(argumentName)
        return errorName



        if pass_io:
            # check for abbreviation
            dic_type_abbreviation = {'string': 'str', 'int32': 'int', 'datacolumn': 'dclm', 'double': 'dbl',
                                     'dateTime': 'date', 'array': 'arr', 'list': 'lst', 'dictionary': 'dic',
                                     'exception': 'ept', 'queueitem': 'qitm'}
            if (len(df_argument_row['argumentName']) -
                len(df_argument_row['argumentName'].replace("_", ""))) >= 2:
                substring = df_argument_row['argumentName'].split("_")[1]
                if (df_argument_row['dataType'] in dic_type_abbreviation.keys()) and \
                        (substring == dic_type_abbreviation[df_argument_row['dataType']]):
                    return True
                # argument type is not in above dict but format still matches ['abbreviation''_''anything']
                elif df_argument_row['dataType'] not in dic_type_abbreviation.keys():
                    dataType = df_argument_row['dataType']
                    for j in substring:
                        if j not in dataType:
                            return False
                        dataType = dataType[(dataType.find(j)+1):]
                    # check camelcase
                    sublist = df_argument_row['argumentName'].split("_")[2:]
                    substring = ''
                    for i in sublist:
                        substring += i

                    # first char must not be upper
                    if substring[0].isupper():
                        return False
                    else:
                        # Any upper case may be not be next to another upper case
                        previousLetterUpper = False
                        for i in substring[1:]:
                            currentLetterUpper = i.isupper()
                            if currentLetterUpper and (not previousLetterUpper):
                                previousLetterUpper = True
                            elif (not currentLetterUpper):
                                previousLetterUpper = False
                            elif currentLetterUpper and previousLetterUpper:
                                return False
                        return True
                    # end check camel case
                else:
                    return False
            else:
                return False
        else:
            return pass_io

    if numArgument > 0:
        df_argument['error'] = df_argument.apply(proper, axis=1)
        df_argument['properNamed'] = df_argument.apply(lambda x: True if x['error']==[] else False, axis=1)
        # return lists
        argumentNamingScore = df_argument.properNamed.sum() / numArgument
        df_argument_dup = df_argument.copy()
        df_argument_dup['type'] = "Argument Naming"
        df_argument_dup.rename(columns={'argumentName': 'name', 'filePath': 'file', 'projectId': 'project'},
                               inplace=True)
        # df_argument_dup.filePath = df_argument_dup.filePath.str.replace(fileLocationStr, '')
        improperNamedArguments = list(df_argument_dup[df_argument_dup['properNamed'] == False].dropna()
                                      .loc[:, ['name', 'file', 'type', 'error', 'project']].T.to_dict().values())
    else:
        [argumentNamingScore, improperNamedArguments] = [0, []]

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
        improperNamedActivities = list(df_activity_dup[df_activity_dup['customizedName'] != True].dropna()
                                       .reset_index(drop=True).reset_index(drop=False)
                                       .loc[:, ['index', 'activityName', 'filePath']].T.to_dict().values())
    else:
        [activityNamingScore, improperNamedActivities] = [0, []]

    return [activityNamingScore, improperNamedActivities]

# end 3. activity naming
