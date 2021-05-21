# flask_example.py
import os
import flask
import requests
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    BatchSpanProcessor,
)
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from prometheus_client import start_http_server, Counter

service_name = os.environ.get('SERVICE_NAME', 'otel-flask-service')
agent_host = os.environ.get('AGENT_HOST', 'localhost')
agent_port = os.environ.get('AGENT_PORT', '6831')

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: service_name})
    )
)

jaeger_exporter = JaegerExporter(
    agent_host_name = agent_host,
    agent_port = int(agent_port),
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Create a metric to track total number of requests made.
REQUEST_TOTAL = Counter('total_requests', 'Total number of HTTP requests')



app = flask.Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route("/")
def hello():
    tracer = trace.get_tracer(__name__)
    REQUEST_TOTAL.inc()
    with tracer.start_as_current_span("example-request"):
        requests.get("http://www.example.com")
    return "hello"

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(9000)

app.run(host='0.0.0.0', debug=False, port=5000)