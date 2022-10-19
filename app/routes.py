from app import app, models
from app.decorators import *
from flask import request, json
import uuid


@app.route('/')
def index():
    return '<h1>Todo API</h1>'


@app.route('/createTodoList', methods=['POST'])
def createTodoList():
    json_request = json.loads(request.data)
    todo_list_model = models.TodoList(**json_request)
    todo_list_model.save()
    return todo_list_model.to_json()


@app.route('/getAllTodoLists', methods=['GET'])
def getTodoLists():
    return models.TodoList.objects.all().to_json()


@app.route('/getTodoList/<string:listId>/', methods=['GET'])
@remove_prefix
def getTodoList(listId):
    return models.TodoList.objects(pk=listId).to_json()


@app.route('/updateTodoList/<listId>/', methods=['PUT'])
@remove_prefix
def updateTodoList(listId):

    json_request = json.loads(request.data)

    models.TodoList.objects(pk=listId).update_one(
        set__name=json_request['name'])

    return models.TodoList.objects(pk=listId).to_json()


@app.route('/createTodo/<listId>/', methods=['POST'])
@remove_prefix
def createTodo(listId):
    json_request = json.loads(request.data)
    dto_todo = models.Todo(**json_request)

    models.TodoList.objects(pk=listId).update_one(push__todos=dto_todo)

    return models.TodoList.objects(pk=listId).to_json()


@app.route('/deleteTodo/<listId>', methods=['DELETE'])
@remove_prefix
def deleteTodo(listId):
    json_request = json.loads(request.data)
    todo_uuid = uuid.UUID(json_request['id'])

    models.TodoList.objects(pk=listId).update_one(
        pull__todos__id=todo_uuid)

    return models.TodoList.objects(pk=listId).to_json()


@app.route('/updateTodo/<listId>', methods=['PUT'])
@remove_prefix
def updateTodo(listId):
    json_request = json.loads(request.data)

    dto_todo = models.Todo(**json_request)
    models.TodoList.objects(todos__id=uuid.UUID(
        dto_todo.id)).update_one(set__todos__S=dto_todo)

    return models.TodoList.objects(pk=listId).to_json()
