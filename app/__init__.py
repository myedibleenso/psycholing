from flask import Flask
import os
from config import basedir
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
app.debug = True

app.config.from_object('config')

bootstrap = Bootstrap(app)

from app import views # avoid circular references
