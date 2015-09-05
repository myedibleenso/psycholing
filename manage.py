#!venv/bin/python
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db
from app.models import User, Rank

migrate = Migrate(app, db)

manager = Manager(app)


if __name__ == '__main__':
    manager.run()
