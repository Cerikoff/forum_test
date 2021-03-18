from flask import request, Response, jsonify
from werkzeug.exceptions import BadRequest

from app import app, db_connection
from app.resources.post_resource import PostResource


# POST - create post
# GET - get posts list
@app.route('/post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        if request.json:
            with PostResource(db_connection) as post:
                post.create(**request.json)
            return Response('Ok', status=201)
        else:
            raise BadRequest('empty body')
    else:
        with PostResource(db_connection) as post:
            return jsonify(post.filter(**request.values))


# GET - get post info
# DELETE - delete post
# POST - restore post
# PUT - update post
@app.route('/post/<int:id>', methods=['GET', 'DELETE', 'POST', 'PUT'])
def post(id):
    with PostResource(db_connection) as post:
        if request.method == 'GET':
            return jsonify(post.details(id))
        elif request.method == 'DELETE':
            post.delete(id)
            return Response('deleted', status=200)
        elif request.method == 'POST':
            post.restore(id)
            return Response('restored', status=200)
        else:
            post.update(id, **request.json)
            return Response('Ok', status=200)
