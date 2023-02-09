ARG VARIANT="3.9-alpine"
FROM python:${VARIANT}

WORKDIR /app
COPY requirements.txt /app
RUN apk add gcc musl-dev libffi libffi-dev \
    && python3 -m pip install -r requirements.txt \
    && apk del git gcc musl-dev libffi-dev

COPY . /app
ARG APP_PORT=5000
ARG APP_VERSION=1.0.0
ARG COMMIT_HASH="none"
ENV PORT=${APP_PORT}
ENV PROMETHEUS_MULTIPROC_DIR=/tmp
ENV APP_VERSION=${APP_VERSION}
ENV COMMIT_HASH=$COMMIT_HASH

LABEL app-version=$APP_VERSION
LABEL commit-hash=$COMMIT_HASH

ENTRYPOINT [ "gunicorn", "-c", "gunicorn.py", "app:app" ]
