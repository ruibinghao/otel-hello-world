#!/bin/bash
#source venv/bin/activate

python3 tracing-flask.py 

#flask deploy
# exec gunicorn -b :5000 --access-logfile - --error-logfile - flasky:app