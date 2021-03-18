from flask import request, Response, jsonify
from werkzeug.exceptions import BadRequest

from app import app, db_connection
from app.resources.forum_resource import ForumResource
from app.resources.thread_resource import ThreadResource


# POST - create forum
@app.route('/forum', methods=['POST'])
def create_forum():
    if request.json:
        with ForumResource(db_connection) as forum:
            forum.create(**request.json)
        return Response('Ok', status=201)
    else:
        raise BadRequest('empty body')


# GET - get forum info
@app.route('/forum/<int:id>', methods=['GET'])
def forum(id):
    with ForumResource(db_connection) as forum:
        return jsonify(forum.details(id))


@app.route('/forum/<int:id>/threads', methods=['GET'])
def get_forum_threads(id):
    with ThreadResource(db_connection) as thread:
        return jsonify(thread.filter(id))