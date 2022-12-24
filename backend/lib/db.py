import sqlalchemy as dbconn
import logging
from sqlalchemy import Table, Column, Integer, String, MetaData
import os

meta = MetaData()
accessTable = Table(
   'access', meta,
   Column('id', Integer, primary_key = True),
   Column('type', String(32)),
   Column('counter', Integer),
)

def initDB():
    DB_PORT = os.environ.get('DB_PORT', 3306)
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PASSWD = os.environ.get('DB_PASSWD', 'yes')
    DB_DBNAME = os.environ.get('DB_DBNAME', 'test-db')
    engine = dbconn.create_engine("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(DB_USER, DB_PASSWD, DB_HOST, DB_PORT, DB_DBNAME))
    conn = engine.connect()
    inspector = dbconn.inspect(engine)
    if (len(inspector.get_table_names(schema=DB_DBNAME)) == 0):
        meta.create_all(engine)
        engine.execute('INSERT INTO access (type, counter) VALUES ("GET", 0)')
        engine.execute('INSERT INTO access (type, counter) VALUES ("POST", 0)')

    logging.info('Connected to DB')
    return conn