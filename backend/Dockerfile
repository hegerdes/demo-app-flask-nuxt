ARG VARIANT="3.9-alpine"
FROM python:${VARIANT}

WORKDIR /app
COPY requirements.txt /app
RUN apk add gcc musl-dev libffi libffi-dev \
    && python3 -m pip install -r requirements.txt \
    && apk del git gcc musl-dev libffi-dev

COPY . /app
ARG APP_PORT=5000
ENV PORT=${APP_PORT}
ENV PROMETHEUS_MULTIPROC_DIR=/tmp

ENTRYPOINT [ "gunicorn", "-c", "gunicorn.py", "app:app" ]
