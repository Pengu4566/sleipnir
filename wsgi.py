"""
This script runs the FlaskWebProject1 application using a development server.
"""

import os
from flask import create_app
from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__, static_folder='./static/dist', template_folder="./static")

if __name__ == '__main__':
    app.run(debug=True)
