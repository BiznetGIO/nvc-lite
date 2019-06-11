from . import configs
from flask import Flask, g, request
from flask_cors import CORS
from flask_redis import FlaskRedis
from celery import Celery
import os
import cx_Oracle, pymysql


celery = Celery(__name__,
                broker=os.environ.get("CELERY_BROKER_URL",
                                        "amqp://admin:qazwsx@127.0.0.1:5672//"),
                backend=os.environ.get("CELERY_RESULT_BACKEND",
                                        "amqp://admin:qazwsx@127.0.0.1:5672//"))

# ORACLE BIZNET DB
db = "(DESCRIPTION=(ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = 202.169.33.34)(PORT = 1522)))(CONNECT_DATA=(SERVER=DEDICATED)(SID=BIZODS2)))"
connection = cx_Oracle.connect("crestelodsread","crestelodsread",db)
cursor = connection.cursor()

# HOSTBILL BGN DB
conn_mysql = pymysql.connect(host=os.environ.get("MYSQL_HOST",os.getenv('FLASK_MYSQL_HOST')),
                        user=os.environ.get("MYSQL_USER",os.getenv('FLASK_MYSQL_USER')),
                        password=os.environ.get("MYSQL_PASSWORD",os.getenv('FLASK_MYSQL_PASSWORD')),
                        db=os.environ.get("MYSQL_DB",os.getenv('FLASK_MYSQL_DB')),
                        cursorclass=pymysql.cursors.DictCursor,
                        autocommit=True)
db_mysql = conn_mysql.cursor()

redis_store = FlaskRedis()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def create_app():
    app = Flask(__name__)
    app.config.from_object(configs.Config)
    app.config['REDIS_URL'] = os.environ.get(
        "APP_REDIS_URL","redis://:@127.0.0.1:6379/0")
    redis_store.init_app(app)
    celery.conf.update(app.config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .controllers import api_blueprint
    from .controllers import swaggerui_blueprint

    app.register_blueprint(swaggerui_blueprint,url_prefix=os.environ.get("/api/docs","/api/docs"))

    app.register_blueprint(api_blueprint)

    return app
