#!/bin/bash
#source venv/bin/activate
for i in {1..100}
do
  echo "Welcome $i times"
  python3 tracing-agent.py 
done
#flask deploy
# exec gunicorn -b :5000 --access-logfile - --error-logfile - flasky:app