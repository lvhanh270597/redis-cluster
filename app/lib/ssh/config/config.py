import os

config = dict()

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__).replace(".","/")))
SHEPATH = os.path.join(BASEDIR, "shell")
