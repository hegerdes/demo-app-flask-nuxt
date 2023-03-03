"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics


def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(8080)


def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)


bind = "0.0.0.0:" + environ.get("PORT", "5000")
max_requests = 1000
workers = cpu_count()
