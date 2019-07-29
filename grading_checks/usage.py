# package import
import os
from builtins import len, open, list
import pandas as pd
import untangle
import re
import matplotlib.pyplot as plt
import zipfile
from math import pi
from werkzeug.utils import secure_filename
# end package import

# function module for usage
# 1. variable usage
# 2. argument usage
# 3. activity usage

# 1. variable usage
def grade_variable_usage(df_variable, fileLocationStr):
    numVariables = len(df_variable.variableName)
    if numVariables > 0:
        df_variable_dup = df_variable.copy()
        df_variable_dup.filePath = df_variable_dup.filePath.str.replace(fileLocationStr, '')
        unusedVariable = list(df_variable_dup.loc[df_variable_dup['count'] == 1].dropna()
                              .reset_index(drop=True).reset_index()
                              .loc[:, ['index', 'variableName', 'filePath']].T.to_dict().values())
        variableUsageScore = len(df_variable_dup.loc[df_variable_dup['count'] > 1]['count']) / numVariables * 100
    else:
        [variableUsageScore, unusedVariable] = [0, ["There is no variable in your project."]]

    return [variableUsageScore, unusedVariable]
# end 1. variable usage


# 2. argument usage
def grade_argument_usage(df_argument, fileLocationStr):
    numArguments = len(df_argument['count'])
    if numArguments > 0:
        df_argument_dup = df_argument.copy()
        df_argument_dup.filePath = df_argument_dup.filePath.str.replace(fileLocationStr, '')
        unusedArgument = list(df_argument_dup.loc[df_argument_dup['count'] == 1].dropna()
                              .reset_index(drop=True).reset_index()
                              .loc[:, ['index', 'argumentName', 'filePath']].T.to_dict().values())
        argumentUsageScore = len(df_argument_dup.loc[df_argument_dup['count'] > 1]['count']) / numArguments * 100
    else:
        [argumentUsageScore, unusedArgument] = [0, ["There is no argument in your project."]]
    return [argumentUsageScore, unusedArgument]
# end 2. argument usage