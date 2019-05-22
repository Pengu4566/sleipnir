import untangle
import pandas as pd
import re
import sys


def populate_args_dataframe(filePath):

    # init dataframe
    df_argument = pd.DataFrame(columns=['argumentName', 'argumentType', 'filePath'])

    with open(filePath, encoding='utf-8', mode='r') as f:
            printLine = False
            style = 1
            for line in f:
                if 'ui:InvokeWorkflowFile.Arguments>' in line.strip(" "):
                    printLine = not printLine
                    style = 1
                if printLine and \
                        ('ui:InvokeWorkflowFile.Arguments>' not in line.strip(" ")) and \
                        (style == 1):
                    argumentName = untangle.parse(line.strip(" ")) \
                        .children[0]['x:Key']
                    argumentType = untangle.parse(line.strip(" ")) \
                        .children[0]._name
                    df_argument = df_argument.append({'argumentName': argumentName,
                                                      'argumentType':
                                                          argumentType,
                                                      'filePath': filePath},
                                                     ignore_index=True)

                if ('<x:Members>' in line.strip(" ")) or \
                        ('</x:Members>' in line.strip(" ")):
                    printLine = not printLine
                    style = 2
                if printLine and ('<x:Members>' not in line.strip(" ")) and (style == 2):

                    print(untangle.parse(line.strip(" ")).children[0]['Name'], file=sys.stderr)

                    argumentName = untangle.parse(line.strip(" ")).children[0]['Name']
                    argumentType = untangle.parse(line.strip(" ")).children[0]['Type']
                    argumentType = argumentType[:argumentType.index('(')]
                    df_argument = df_argument.append({'argumentName': argumentName,
                                                      'argumentType':argumentType,
                                                      'filePath': filePath},
                                                      ignore_index=True)
                    print(len(df_argument.argumentName), file=sys.stderr)

                return df_argument

    # end argument dataframe

        # # Property Names for arguments in arguments tab (ported from variable_naming.py)
        # with open(filePath, encoding='utf-8', mode='r') as f:
        #     for line in f:
        #         if line.strip(" ").startswith('<x:Property Name'):
        #             variableName = untangle.parse(line.strip(" ")).children[0]['Name']
        #             dataType = untangle.parse(line.strip(" ")).children[0]['Type'].split(":")[1].split(")")[0]
        #
        #             if '[]' in dataType:
        #                 dataType = 'Array'
        #             if (filePath not in list(df_variable[df_variable.variableName == variableName].filePath)):
        #                 df_variable = df_variable.append({'variableType': dataType, 'variableName': variableName,
        #                                                   'count': 1, 'filePath': filePath}, ignore_index=True)
        #                 # print(str(df_variable))


# check argument in/out
def grade_arguments_io(df_argument):
    numArgument = len(df_argument) / 100

    # check if argument name is proper in df_argument
    def proper(df_argument_row):
        if (df_argument_row['argumentType'] == 'InArgument') and \
                (df_argument_row['argumentName'].startswith('in_')):
            return True
        elif (df_argument_row['argumentType'] == 'OutArgument') and \
                (df_argument_row['argumentName'].startswith('out_')):
            return True
        elif (df_argument_row['argumentType'] == 'InOutArgument') and \
                (df_argument_row['argumentName'].startswith('io_')):
            return True
        else:
            return False

    df_argument['properNamed'] = df_argument.apply(proper, axis=1)

    # return lists
    argumentNamingScore = len(
        df_argument[df_argument['properNamed'] == True]) / numArgument
    # improperNamedArguments = list(df_argument[df_argument['properNamed']!= True].argumentName)
    temp_improperNamedArguments = list(
        df_argument[df_argument['properNamed'] != True].argumentName)
    improperNamedArguments = [
        x for x in temp_improperNamedArguments if x is not None]

    return [argumentNamingScore, improperNamedArguments]
# end check argument in/out