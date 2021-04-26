FROM python:3.8

#RUN adduser -D flasky
#USER flasky


COPY requirements requirements
#UN python -m venv venv
#RUN venv/bin/pip install -r requirements/common.txt
RUN pip install -r requirements/common.txt

COPY tracing-agent.py boot.sh ./

# run-time configuration
# EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
