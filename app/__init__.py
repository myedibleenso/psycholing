from flask import Flask
import os
from config import basedir
import sqlite3
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.debug = True

app.config.from_object('config')

bootstrap = Bootstrap(app)

#sqlite3.connect(os.path.abspath("app.db"))
db = SQLAlchemy(app)
#db.create_all()

from app import views, models # avoid circular references
