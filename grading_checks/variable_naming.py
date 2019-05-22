import untangle
import pandas as pd
import re
import sys


def populate_variables_dataframe(filePath):

    # init dataframe
    df_variable = pd.DataFrame(columns=['variableType', 'variableName', 'count', 'filePath'])

    # capture variables bound by tags
    with open(filePath, encoding='utf-8', mode='r') as f:
        for line in f:
            if line.strip(" ").startswith('<Variable x:'):
                variableName = untangle.parse(line.strip(" ")) \
                    .children[0]['Name']
                dataType = untangle.parse(line.strip(" ")) \
                    .children[0]['x:TypeArguments'] \
                    .split(":")[1].split("(")[0]
                if '[]' in dataType:
                    dataType = 'Array'
                if filePath not in list(df_variable[df_variable.variableName == variableName].filePath):
                    df_variable = df_variable.append({'variableType': dataType, 'variableName': variableName,
                                                      'count': 1, 'filePath': filePath}, ignore_index=True)

    with open(filePath, encoding='utf-8', mode='r') as f:
        for line in f:
            for index, row in df_variable.iterrows():
                if (re.search(('\[.*' + row['variableName'] + '.*\]'), line) is not None) and \
                        (filePath == row['filePath']):
                    row['count'] += 1

    return df_variable


def grade_variable_name(df_variable):
    numVariables = len(df_variable.variableName)

    print("[DEBUG MESSAGE] - length of df_variable: " + str(numVariables), file=sys.stderr)

    # check if variable name is proper in df_variable ['variableType', 'variableName', 'count', 'filePath']
    def ProperVariableNaming(df_variable_row):
        dic_type_abbreviation = {'String': 'str',
                                 'Int32': 'int',
                                 'DataColumn': 'dclm',
                                 'Double': 'dbl',
                                 'DateTime': 'date',
                                 'Array': 'arr',
                                 'List': 'lst',
                                 'Dictionary': 'dic',
                                 'Exception': 'ept',
                                 'QueueItem': 'qi'}

        # checks if df_variable length is zero and returns zeros for all scores
        if len(df_variable) == 0:
            return [0, 0, 0, 0]

        # check camel case naming for everything right of the '_'
        # For everything right of "_" apply:
        # 	First character may not be upper
        # 	If > 2 upper case character
        #     Any upper case may be not be next to another upper case
        for j in df_variable['variableName']:
            #print(j, file=sys.stderr)

            # if it contains a "_", split on it and extract everything after
            if "_" in j:
                afterUnderscoreString = j.split('_')[1]
                #print(afterUnderscoreString, file=sys.stderr)

                # first char must not be upper
                if afterUnderscoreString[0].isupper():
                    return False

                # uppercase letters must not be next to each other
                counter = 0
                previousLetterUpper = False
                while counter < len(afterUnderscoreString):
                    currentLetterUpper = afterUnderscoreString[counter].isupper()

                    if previousLetterUpper & currentLetterUpper:
                        return False
                    else:
                        previousLetterUpper = currentLetterUpper
                        currentLetterUpper = False

                    #print(afterUnderscoreString[counter] + " " + afterUnderscoreString[counter - 1], file=sys.stderr)
                    counter = counter + 1
            return True

        # variable type is in dict above and format matches ['abbreviation''_''anything'] i.e.(int_counter, str_thing)
        if (df_variable_row['variableType'] in dic_type_abbreviation.keys()) and \
                (df_variable_row['variableName'].startswith(dic_type_abbreviation[df_variable_row['variableType']]
                                                            + '_')):
            return True
        # variable type is not in above dict but format still matches ['abbreviation''_''anything']
        elif (not df_variable_row['variableType'] in dic_type_abbreviation.keys()) and \
                ('_' in df_variable_row['variableName']):
            ind = 0
            abb = True
            for j in df_variable_row['variableName'].split('_')[0]:
                if (j in df_variable_row[df_variable_row['variableName']]) and \
                        (df_variable_row[df_variable_row['variableName']].find(j) <= ind):
                    abb = (abb and True)
                else:
                    abb = (abb and False)

                ind = df_variable_row[df_variable_row['variableName']].find(j)
                return abb
        else:
            return False

    df_variable['properNamed'] = df_variable.apply(ProperVariableNaming, axis=1)

    # return lists
    improperNamedVariable = list(df_variable.loc[df_variable.properNamed == False].variableName)
    unusedVariable = list(df_variable.loc[df_variable['count'] == 1].variableName)
    variableUsageScore = len(df_variable.loc[df_variable['count'] > 1]['count']) / numVariables * 100
    variableNamingScore = len(df_variable.loc[df_variable.properNamed == True].variableName) / numVariables * 100

    return [variableNamingScore, variableUsageScore, improperNamedVariable, unusedVariable]