import os

basedir = os.path.abspath(os.path.dirname(__file__))

#APPLICATION_ROOT = 'app'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'png', 'jpg', 'jpeg', 'json'])

WTF_CSRF_ENABLED = True
SECRET_KEY = 'poop'
