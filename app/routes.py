from app import app, models
from flask import request, json
from bson import ObjectId
import uuid

@app.route('/')
def index():
  return '<h1>Todo API</h1>'

@app.route('/createTodoList', methods = ['POST'])
def createTodoList():
    json_request = json.loads(request.data)
    todo_list_model = models.TodoList(**json_request)
    todo_list_model.save()
    return todo_list_model.to_json()
  
@app.route('/getAllTodoLists', methods = ['GET'])
def getTodoLists():     
    return models.TodoList.objects.all().to_json()
  
@app.route('/getTodoList/<listId>/', methods = ['GET'])
def getTodoList(listId):
    listIdInstance = ObjectId(str(listId).removeprefix('listId='))  
    return models.TodoList.objects(pk=listIdInstance).to_json()  
  
@app.route('/updateTodoList/<listId>/', methods = ['PUT'])
def updateTodoList(listId):

  json_request = json.loads(request.data)
  listIdInstance = ObjectId(str(listId).removeprefix('listId='))

  models.TodoList.objects(pk=listIdInstance).update_one(set__name=json_request['name'])
  
  return models.TodoList.objects(pk=listIdInstance).to_json()
  
@app.route('/createTodo/<listId>/', methods = ['POST'])
def createTodo(listId):
  json_request = json.loads(request.data)
  listIdInstance = ObjectId(str(listId).removeprefix('listId='))  
  dto_todo = models.Todo(**json_request)  
    
  models.TodoList.objects(pk=listIdInstance).update_one(push__todos=dto_todo)
  
  return models.TodoList.objects(pk=listIdInstance).to_json()

@app.route('/deleteTodo/<listId>', methods = ['DELETE'])
def deleteTodo(listId):
  json_request = json.loads(request.data)
  listIdInstance = ObjectId(str(listId).removeprefix('listId='))  
  todo_uuid = uuid.UUID(json_request['id'])
  
  models.TodoList.objects(pk=listIdInstance).update_one(pull__todos__id = todo_uuid)
  
  return models.TodoList.objects(pk=listIdInstance).to_json()

@app.route('/updateTodo/<listId>', methods = ['PUT'])
def updateTodo(listId):
  json_request = json.loads(request.data)
  listIdInstance = ObjectId(str(listId).removeprefix('listId='))
  
  dto_todo = models.Todo(**json_request)  
  models.TodoList.objects(todos__id=uuid.UUID(dto_todo.id)).update_one(set__todos__S=dto_todo)
  
  return models.TodoList.objects(pk=listIdInstance).to_json()
