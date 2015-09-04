#!venv/bin/python
from app import app
import os, sys, logging

logging.basicConfig(stream=sys.stderr)

if __name__ == '__main__':
    app.debug = True
    app.run()
