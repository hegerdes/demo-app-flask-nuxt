#!/usr/bin/env python3
import flask
import dotenv
import logging
import os
import sys
import requests
from flask import Flask, Response
from datetime import date
from flask_cors import CORS
from sqlalchemy import update
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter.multiprocess import PrometheusMetrics
from flask_session import Session

# import lib.db as db
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
conn = None

# Flask setup
logging.info("Init Flask")
app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Check Configuration section for more details
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
session = Session(app)
coors = CORS(app)
limiter = Limiter(
    get_remote_address, app=app, default_limits=["60 per minute", "5 per second"]
)
get_counter = {}
post_counter = {}

metrics.info(
    "app_info", "Application info", version=os.environ.get("APP_VERSION", "1.0.0")
)


def getIP(request: flask.Request) -> str:
    headers_forward_list = request.headers.getlist("X-Forwarded-For")
    return headers_forward_list[0] if headers_forward_list else request.remote_addr


@app.route("/")
def home_get():
    app.logger.info(
        "Got GET / request at: {} from upstream {}".format(
            date.today(), flask.request.remote_addr
        )
    )

    # Request counter
    # NOTE: This is just in memory and not replication safe
    ip = getIP(flask.request)
    user_agent = flask.request.headers.get("User-Agent")
    counter = flask.session.get("GET_" + ip, 0) + 1
    get_counter["GET_" + ip] = counter
    flask.session["GET_" + ip] = counter

    return {
        "RequestInfo": {
            "host": flask.request.headers.get("Host"),
            "user-agent": user_agent,
            "ip": ip,
            "method": "GET",
            "payload": "NONE",
        },
        "ServerInfo": {
            "Node": os.environ.get("HOSTNAME", "DEFAULT_HOST"),
            "RequestCounter": counter,
        },
    }


@app.route("/", methods=["POST"])
def home_post():
    app.logger.info(
        "Got POST / request at: {} from upstream {}".format(
            date.today(), flask.request.remote_addr
        )
    )

    # Request counter
    # NOTE: This is just in memory and not replication safe
    ip = getIP(flask.request)
    user_agent = flask.request.headers.get("User-Agent")
    counter = flask.session.get("POST_" + ip, 0) + 1
    post_counter["POST_" + ip] = counter
    flask.session["POST_" + ip] = counter

    return {
        "RequestInfo": {
            "host": flask.request.headers.get("Host"),
            "user-agent": user_agent,
            "ip": ip,
            "method": "POST",
            "payload": str(flask.request.get_json()),
        },
        "ServerInfo": {
            "Node": os.environ.get("HOSTNAME", "DEFAULT_HOST"),
            "RequestCounter": counter,
        },
    }


@app.route("/oidc", methods=["POST"])
def oidc():
    app.logger.info(
        "Got POST /oidc request at: {} from upstream {}".format(
            date.today(), flask.request.remote_addr
        )
    )

    payload = flask.request.get_json()
    oidc_access_token = flask.request.headers.get("x-auth-request-access-token", None)
    res = {"status": "error", "msg": "no oidc access token found in headers"}
    print(payload)
    try:
        if oidc_access_token != None:
            url = payload.get("url")
            method = payload.get("method", "GET").upper()
            data = payload.get("data", None)
            headers = payload.get("headers", {})
            headers = {**headers, "Authorization": oidc_access_token}

            response = requests.request(method, url, headers=headers, data=data)
            res = response.json()
    except Exception as e:
        res = {"status": "error", "msg": str(e)}
    finally:
        return res


@app.route("/metrics")
@limiter.exempt
@metrics.do_not_track()
def metrics_get():
    response_data, content_type = metrics.generate_metrics()
    print(response_data)
    return Response(response_data, mimetype=content_type)


@app.route("/healthz")
@limiter.exempt
@metrics.do_not_track()
def home_health():
    return "ok"


def start():
    logging.info("Starting App")
    if os.environ.get("FLASK_ENV", "development") == "development":
        dotenv.load_dotenv(".env")
        logging.debug("Using .env file")

    # DB Setup
    # app.dbconn = db.initDB()
    return app


# Run
start()

if __name__ != "__main__":
    wasgi_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = wasgi_logger.handlers
    app.logger.setLevel(wasgi_logger.level)

# Run in dev mode
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        appenv = os.environ.get("FLASK_ENV", "development")
        if appenv == "development":
            dotenv.load_dotenv(".env")
        app = start()
        if appenv == "development":
            app.testing = True
            app.debug = True
            app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    except KeyboardInterrupt:
        print("Interrupt received! Closing...")
