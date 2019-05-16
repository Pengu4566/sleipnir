"""
This script runs the FlaskWebProject1 application using a development server.
"""

import os
from application import create_app
app = Flask(__name__, static_folder='./static/dist', template_folder="./static")

if __name__ == '__main__':
    app.run(debug=True)
