# function module for naming
# 1. variable naming
# 2. argument naming
# 3. activity naming

# 1. variable naming: camelcase, abbreviation ahead of name

def grade_variable_name(df_variable):
    numVariables = len(df_variable.variableName)

    # check if variable name is proper in df_variable ['variableType', 'variableName', 'count', 'filePath']
    def proper_variable_naming(df_variable_row):

        # if there is a "_" in the name
        if "_" in df_variable_row['variableName']:
            # check camelcase
            # For right of "_" apply:
            try:
                afterUnderscoreString = df_variable_row['variableName'].split('_')[1]
            except IndexError:
                return False
            # first char must not be upper
            if len(afterUnderscoreString) == 0:
                return False
            elif afterUnderscoreString[0].isupper():
                return False
            else:
                # Any upper case may be not be next to another upper case
                previousLetterUpper = False
                for i in afterUnderscoreString[1:]:
                    currentLetterUpper = i.isupper()
                    if currentLetterUpper and (not previousLetterUpper):
                        previousLetterUpper = True
                    elif (not currentLetterUpper):
                        previousLetterUpper = False
                    elif currentLetterUpper and previousLetterUpper:
                        return False
            # if passed camelcase checking, check for abbreviation
            # variable type is in dict above and format matches ['abbreviation''_''anything'] i.e.(int_counter, str_thing)
            dic_type_abbreviation = {'string': 'str',
                                     'int32': 'int',
                                     'datacolumn': 'dclm',
                                     'double': 'dbl',
                                     'dateTime': 'date',
                                     'array': 'arr',
                                     'list': 'lst',
                                     'dictionary': 'dic',
                                     'exception': 'ept',
                                     'queueItem': 'qi'}
            if df_variable_row['variableType'] in dic_type_abbreviation.keys():
                if df_variable_row['variableName'].startswith(dic_type_abbreviation
                                                              [df_variable_row['variableType']] + '_'):
                    return True
                return False
            # variable type is not in above dict but format still matches ['abbreviation''_''anything']
            else:
                variableType = df_variable_row['variableType']
                for j in df_variable_row['variableName'].split('_')[0]:
                    if j not in variableType:
                        return False
                    variableType = variableType[(variableType.find(j)+1):]
                return True
        # if there is no "_" in the name
        else:
            return False


    if numVariables > 0:
        df_variable['properNamed'] = df_variable.apply(proper_variable_naming, axis=1)
        # return lists
        if (False in df_variable.properNamed) and (True in df_variable.properNamed):
            improperNamedVariable = list(df_variable.loc[df_variable.properNamed == False].variableName)
            variableNamingScore = len(
                df_variable.loc[df_variable.properNamed == True].variableName) / numVariables * 100
        elif True in df_variable.properNamed :
            improperNamedVariable = ['There is no improperly named variable.']
            variableNamingScore = 100
        else:
            improperNamedVariable = list(df_variable.variableName)
            variableNamingScore = 0
    else:
        improperNamedVariable = ['There is no variable in your project.']
        variableNamingScore = 0

    return [variableNamingScore, improperNamedVariable]

# end 1. variable naming


# 2. argument naming: in/out/io, abbreviation, camel case

def grade_argument_name(df_argument):
    numArgument = len(df_argument) / 100

    # check if argument name is proper in df_argument
    def proper(df_argument_row):
        # check for in/out/io
        pass_io = False
        if (df_argument_row['argumentType'] == 'InArgument') and (df_argument_row['argumentName'].startswith('in_')):
            pass_io = True
        elif (df_argument_row['argumentType'] == 'OutArgument') and (df_argument_row['argumentName'].startswith('out_')):
            pass_io = True
        elif (df_argument_row['argumentType'] == 'InOutArgument') and (df_argument_row['argumentName'].startswith('io_')):
            pass_io = True
        if pass_io:
            # check for abbreviation
            dic_type_abbreviation = {'string': 'str',
                                     'int32': 'int',
                                     'datacolumn': 'dclm',
                                     'double': 'dbl',
                                     'dateTime': 'date',
                                     'array': 'arr',
                                     'list': 'lst',
                                     'dictionary': 'dic',
                                     'exception': 'ept',
                                     'queueitem': 'qi'}
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
        df_argument['properNamed'] = df_argument.apply(proper, axis=1)
        # return lists
        argumentNamingScore = len(df_argument[df_argument['properNamed'] == True]) / numArgument
        # improperNamedArguments = list(df_argument[df_argument['properNamed']!= True].argumentName)
        temp_improperNamedArguments = list(df_argument[df_argument['properNamed'] != True].argumentName)
        improperNamedArguments = [x for x in temp_improperNamedArguments if x is not None]
    else:
        [argumentNamingScore, improperNamedArguments] = [0, ["There is no argument in your project."]]

    return [argumentNamingScore, improperNamedArguments]

# 2. argument naming: in/out/io, abbreviation


# 3. activity naming

def grade_activity_name(df_activity):
    if len(df_activity['activityName']) > 0:
        # return lists
        df_activity['customizedName'] = (df_activity['activityName'] != df_activity['activityType'])
        activityNamingScore = len(df_activity[df_activity['customizedName'] == True].customizedName) / len(
            df_activity.customizedName) * 100
        improperNamedActivities = list(df_activity[df_activity['customizedName'] != True].activityName)
    else:
        [activityNamingScore, improperNamedActivities] = [0, ["There is no activity in your project."]]

    return [activityNamingScore, improperNamedActivities]

# end 3. activity naming
