from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

#APPLICATION_ROOT = 'app'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'png', 'jpg', 'jpeg', 'json'])

WTF_CSRF_ENABLED = True
SECRET_KEY = 'poop'

