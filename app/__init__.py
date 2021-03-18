from flask import Flask
import psycopg2
from werkzeug.exceptions import BadRequest, NotFound


app = Flask(__name__)

app.config['DB_USER'] = 'postgres'
app.config['DB_NAME'] = 'forum'
app.config['DB_PASS'] = '123qweasd'
app.config['DB_HOST'] = 'localhost'

db_connection = psycopg2.connect(dbname=app.config['DB_NAME'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASS'], host=app.config['DB_HOST'])

from app.api import user_api, forum_api, post_api, thread_api

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return e, 400

@app.errorhandler(NotFound)
def handle_not_found(e):
    return e, 404
