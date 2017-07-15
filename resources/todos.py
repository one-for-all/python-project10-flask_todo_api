from flask_restful import Resource, marshal, fields, Api, reqparse, \
    marshal_with, url_for
from flask import Blueprint, request, g
from auth import auth
import models


todo_fields = {
    'name': fields.String,
    'id': fields.Integer
}


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            location=['form', 'json'],
            help='name required'
        )
        super().__init__()

    def get(self):
        todos = models.Todo.select()
        return [marshal(todo, todo_fields) for todo in todos]

    @marshal_with(todo_fields)
    @auth.login_required
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(
            created_by=g.user,
            **args
        )
        return todo, 201


class Todo(Resource):
    todo_fields = {
        'name': fields.String,
        'id': fields.Integer
    }

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            location=['form', 'json'],
            help='name required'
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        try:
            todo = models.Todo.get(models.Todo.id == id)
        except models.DoesNotExist:
            return 'Error: todo item does not exist', 404
        else:
            return todo

    @auth.login_required
    def delete(self, id):
        try:
            todo = models.Todo.get(models.Todo.id == id,
                                   models.Todo.created_by == g.user)
            todo.delete_instance()
        except models.DoesNotExist:
            return 'Error: todo item does not exist', 404
        else:
            return '', 200

    @auth.login_required
    def put(self, id):
        args = self.reqparse.parse_args()
        try:
            query = models.Todo.update(**args).where(
                models.Todo.id == id,
                models.Todo.created_by == g.user)
            query.execute()
        except models.DoesNotExist:
            return 'Error: todo item does not exist', 404
        else:
            return marshal(models.Todo.get(models.Todo.id == id),
                           todo_fields), 200, {'Location':
                                               url_for(
                                                   'resources.todos.todo',
                                                   id=id)}


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/todos',
    endpoint='todos'
)
api.add_resource(
    Todo,
    '/todos/<int:id>',
    endpoint='todo'
)