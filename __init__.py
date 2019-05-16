"""
The flask application package.
"""

from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__, static_folder='./static/dist', template_folder="./static")