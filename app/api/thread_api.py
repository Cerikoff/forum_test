from flask import request, Response, jsonify
from werkzeug.exceptions import BadRequest

from app import app, db_connection
from app.resources.thread_resource import ThreadResource
from app.resources.post_resource import PostResource


# POST - create thread
@app.route('/thread', methods=['POST', 'GET'])
def create_thread():
    if request.method == 'POST':
        if request.json:
            with ThreadResource(db_connection) as thread:
                thread.create(**request.json)
            return Response('Ok', status=201)
        else:
            raise BadRequest('empty body')
    else:
        forum_id = None
        if 'forum_id' in request.values:
            forum_id = request.values['forum_id']
        with ThreadResource(db_connection) as thread:
            return jsonify(thread.filter(forum_id))


# GET - get thread info
# DELETE - delete thread
# POST - restore thread
@app.route('/thread/<int:id>', methods=['GET', 'DELETE', 'POST'])
def thread(id):
    with ThreadResource(db_connection) as thread:
        if request.method == 'GET':
            return jsonify(thread.details(id))
        elif request.method == 'DELETE':
            thread.delete(id)
            return Response('deleted', status=200)
        else:
            thread.restore(id)
            return Response('restored', status=200)


@app.route('/thread/<int:id>/posts', methods=['GET'])
def get_thread_posts(id):
    with PostResource(db_connection) as post:
        kwargs = {
            'post.thread_id': id
        }
        return jsonify(post.filter(**kwargs))