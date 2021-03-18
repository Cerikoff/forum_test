from flask import request, Response, jsonify
from werkzeug.exceptions import BadRequest

from app import app, db_connection
from app.resources.user_resource import UserResource
from app.resources.post_resource import PostResource


# POST - create user
@app.route('/user', methods=['POST'])
def create_user():
    if request.json:
        with UserResource(db_connection) as user:
            user.create(**request.json)
        return Response('Ok', status=201)
    else:
        raise BadRequest('empty body')


# GET - get user info
# PUT - update user info
@app.route('/user/<int:id>', methods=['GET', 'PUT'])
def user(id):
    if request.method == 'GET':
        with UserResource(db_connection) as user:
            return jsonify(user.details(id))
    else:
        with UserResource(db_connection) as user:
            user.update(id, **request.json)
        return Response('Ok', status=200)


# get all user's posts
@app.route('/user/<int:id>/posts', methods=['GET'])
def get_user_posts(id):
    with PostResource(db_connection) as post:
            kwargs = {
                'post.creator_user_id': id
            }
            return jsonify(post.filter(**kwargs))
