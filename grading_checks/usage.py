# package import
import os
from builtins import len, open, list
import pandas as pd
# end package import

# function module for usage
# 1. variable usage
# 2. argument usage
# 3. activity usage

# 1. variable usage
def grade_variable_usage(df_variable):
    numVariables = len(df_variable.variableName)
    if numVariables > 0:
        df_variable_dup = df_variable.copy()
        # df_variable_dup.filePath = df_variable_dup.filePath.str.replace(fileLocationStr, '')
        df_variable_dup['type'] = "Variable Usage"
        df_variable_dup['error'] = "Declared but not used"
        df_variable_dup.rename(columns={'variableName': 'name', 'filePath': 'file', 'projectName': 'project'},
                               inplace=True)
        df_variable_dup['file'] = df_variable_dup.apply(lambda x: x['file'].replace(str(x['mainFolder']), ""), axis=1)
        unusedVariable = df_variable_dup.loc[df_variable_dup['count'] == 1].dropna()\
                             .loc[:, ['name', 'file', 'type', 'error', 'project']]
        variableUsageScore = len(df_variable_dup.loc[df_variable_dup['count'] > 1]['count']) / numVariables * 100
    else:
        [variableUsageScore, unusedVariable] = [0, pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])]

    return [variableUsageScore, unusedVariable]
# end 1. variable usage


# 2. argument usage
def grade_argument_usage(df_argument):
    numArguments = len(df_argument['count'])
    if numArguments > 0:
        df_argument_dup = df_argument.copy()
        # df_argument_dup.filePath = df_argument_dup.filePath.str.replace(fileLocationStr, '')
        df_argument_dup['type'] = "Argument Usage"
        df_argument_dup['error'] = "Declared but not used"
        df_argument_dup.rename(columns={'argumentName': 'name', 'filePath': 'file', 'projectName': 'project'},
                               inplace=True)
        df_argument_dup['file'] = df_argument_dup.apply(lambda x: x['file'].replace(str(x['mainFolder']), ""), axis=1)
        unusedArgument = df_argument_dup.loc[df_argument_dup['count'] == 1].dropna()\
                             .loc[:, ['name', 'file', 'type', 'error', 'project']]
        argumentUsageScore = len(df_argument_dup.loc[df_argument_dup['count'] > 1]['count']) / numArguments * 100
    else:
        [argumentUsageScore, unusedArgument] = [0, pd.DataFrame(columns=['name', 'file', 'type', 'error', 'project'])]
    return [argumentUsageScore, unusedArgument]
# end 2. argument usage