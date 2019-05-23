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
def grade_variable_usage(df_variable):
    numVariables = len(df_variable.variableName)
    if numVariables > 0:
        unusedVariable = list(df_variable.loc[df_variable['count'] == 1].variableName)
        variableUsageScore = len(df_variable.loc[df_variable['count'] > 1]['count']) / numVariables * 100
    else:
        [variableUsageScore, unusedVariable] = [0, ["There is no variable in your project."]]

    return [variableUsageScore, unusedVariable]
# end 1. variable usage


# 2. argument usage
def grade_argument_usage(df_argument):
    numArguments = len(df_argument['count'])
    if numArguments > 0:
        unusedArgument = list(df_argument.loc[df_argument['count'] == 1].argumentName)
        argumentUsageScore = len(df_argument.loc[df_argument['count'] > 1]['count']) / numArguments * 100
    else:
        [argumentUsageScore, unusedArgument] = [0, ["There is no argument in your project."]]
    return [argumentUsageScore, unusedArgument]
# end 2. argument usage