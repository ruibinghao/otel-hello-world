FROM python:3.8-slim

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

COPY requirements requirements

RUN pip install -r requirements/common.txt

COPY tracing-agent.py tracing-flask.py boot.sh boot-flask.sh boot-flask-slim.sh ./

# run-time configuration
ENV FLASK_DEBUG=False
EXPOSE 5000
EXPOSE 9000
ENTRYPOINT ["./boot-flask.sh"]
