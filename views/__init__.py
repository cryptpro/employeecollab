import os, sys
from flask import Flask
from datetime import timedelta, datetime
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.debug=True

app.config['UPLOAD_FOLDER'] = 'C:/Users/Afroze/Google Drive/employeecollab/views/static/uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg','doc','docx', 'jpeg', 'gif', 'mp4', 'mp3' ])

import browser