from flask import Flask
app = Flask(__name__)
import os
from builtins import len, open, list
import pandas as pd
import untangle
import re

@app.route("/")
def __main__():

    message = "Hello New Innovation!"

    print(message)

    return message

__main__()