from flask_restful import Resource, reqparse, marshal, fields, Api
from flask import Blueprint

import models

user_fields = {
    'username': fields.String,
    'email': fields.String
}


class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        user = models.User.create_user(**args)
        return marshal(user, user_fields)

    def get(self):
        users = models.User.select()
        return [marshal(user, user_fields) for user in users]


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    User,
    '/users',
    endpoint='user'
)