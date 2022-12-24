#!/usr/bin/env python3
import flask
import dotenv
import logging
import os
import sys
from flask import Flask
from datetime import date
from flask_cors import CORS
from sqlalchemy import update
from flask_limiter.util import get_remote_address
import lib.db as db
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
conn = None

# Flask setup
logging.info('Init Flask')
app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def home_get():
    res = dict(app.dbconn.execute(
        'SELECT type, counter FROM access;').fetchall())
    stmt = (
        update(db.accessTable).
        where(db.accessTable.c.type == 'GET').
        values(counter=res['GET'] + 1)
    )
    logging.info('Got GET reqest at: ' + str(date.today()))
    app.dbconn.execute(stmt)
    return {'RequestInfo':
            {
                'host': flask.request.headers.get('Host'),
                'user-agent': flask.request.headers.get('User-Agent'),
                'method': 'GET'
            },
            'ServerInfo': {
                'Node': os.environ.get('NODE_HOST', 'DEFAULT_HOST'),
                'RequestCounter': res['GET']
            }
            }


@app.route("/", methods=["POST"])
def home_post():
    logging.info('Got POST reqest at: ' + str(date.today()))
    res = dict(app.dbconn.execute(
        'SELECT type, counter FROM access;').fetchall())
    stmt = (
        update(db.accessTable).
        where(db.accessTable.c.type == 'POST').
        values(counter=res['POST'] + 1)
    )
    app.dbconn.execute(stmt)
    return {'RequestInfo':
            {
                'host': flask.request.headers.get('Host'),
                'user-agent': flask.request.headers.get('User-Agent'),
                'method': 'POST',
                'payload': str(flask.request.get_json())
            },
            'ServerInfo': {
                'Node': os.environ.get('NODE_HOST', 'DEFAULT_HOST'),
                'RequestCounter': res['POST']
            }
            }


@app.route('/health')
def home_health():
    return 'ok'


def start():
    logging.info('Starting App')
    if os.environ.get('FLASK_ENV', 'development') == 'development':
        dotenv.load_dotenv('.env')
        logging.debug('Using .env file')

    # DB Setup
    app.dbconn = db.initDB()
    return app


start()

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        appenv = os.environ.get('FLASK_ENV', 'development')
        if appenv == 'development':
            dotenv.load_dotenv('.env')
        app = start()
        if appenv == 'development':
            app.testing = True
            app.debug = True
            app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

    except KeyboardInterrupt:
        print('Interrupt received! Closing...')
