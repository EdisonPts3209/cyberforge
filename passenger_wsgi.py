import os
import sys

# Путь к virtualenv
INTERP = os.path.expanduser("~/www/cyberforge.red1dark.ru/flaskenv/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from app import app as application