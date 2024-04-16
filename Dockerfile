FROM python:3.9-alpine

RUN apk update && \
    apk add --no-cache wget && \
    apk add --no-cache python3-dev && \
    apk add --no-cache build-base

RUN pip install --upgrade pip && pip install opentelemetry-distro && opentelemetry-bootstrap -a install && pip install flask
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
COPY repo .

CMD ["python3", "app.py"]
