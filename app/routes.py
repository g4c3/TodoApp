from app import app
from app.decorators import *
from app.models import *
from flask import request, json
import uuid
from flasgger.utils import swag_from

@app.route('/')
def index():
    response = '<h1>Todo API! Your IP Address {ip}</h1>'.format(ip = request.remote_addr)
    return response


@app.route('/createTodoList', methods=['POST'])
@track_time_spent
def createTodoList():
    json_request = json.loads(request.data)
    todo_list_model = TodoList(**json_request)
    todo_list_model.save()
    return todo_list_model.to_json()


@app.route('/getAllTodoLists', methods=['GET'])
@swag_from('api_doc/TodoList.yml')
@track_time_spent
def getTodoLists():
    return TodoList.objects.all().to_json()


@app.route('/getTodoList/<string:listId>/', methods=['GET'])
@track_time_spent
@remove_prefix
def getTodoList(listId):
    return TodoList.objects(pk=listId).to_json()


@app.route('/updateTodoList/<listId>/', methods=['PUT'])
@track_time_spent
@remove_prefix
def updateTodoList(listId):
    json_request = json.loads(request.data)

    TodoList.objects(pk=listId).update_one(
        set__name=json_request['name'])

    return TodoList.objects(pk=listId).to_json()


@app.route('/createTodo/<listId>/', methods=['POST'])
@track_time_spent
@remove_prefix
def createTodo(listId):
    json_request = json.loads(request.data)
    dto_todo = Todo(**json_request)

    TodoList.objects(pk=listId).update_one(push__todos=dto_todo)

    return TodoList.objects(pk=listId).to_json()


@app.route('/deleteTodo/<listId>', methods=['DELETE'])
@track_time_spent
@remove_prefix
def deleteTodo(listId):
    json_request = json.loads(request.data)
    todo_uuid = uuid.UUID(json_request['id'])

    TodoList.objects(pk=listId).update_one(
        pull__todos__id=todo_uuid)

    return TodoList.objects(pk=listId).to_json()


@app.route('/updateTodo/<listId>', methods=['PUT'])
@track_time_spent
@remove_prefix
def updateTodo(listId):
    json_request = json.loads(request.data)

    dto_todo = Todo(**json_request)
    TodoList.objects(todos__id=uuid.UUID(
        dto_todo.id)).update_one(set__todos__S=dto_todo)

    return TodoList.objects(pk=listId).to_json()
