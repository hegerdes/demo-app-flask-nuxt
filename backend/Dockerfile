ARG VARIANT="3.11-alpine"
FROM python:${VARIANT}

WORKDIR /app
COPY requirements.txt /app
ENV GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
ENV GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1

RUN apk add curl gcc g++ musl-dev libffi libffi-dev \
    && python3 -m pip --no-cache-dir install --upgrade wheel \
    && python3 -m pip --no-cache-dir install --upgrade setuptools \
    && python3 -m pip --no-cache-dir install -r requirements.txt \
    && opentelemetry-bootstrap -a install \
    && apk del git gcc g++ musl-dev libffi-dev

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

HEALTHCHECK --interval=30s --timeout=30s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

ENTRYPOINT [ "gunicorn", "-c", "gunicorn.py", "app:app" ]
# ENTRYPOINT [ "opentelemetry-instrument", "gunicorn", "-c", "gunicorn.py", "app:app" ]
