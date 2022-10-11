import datetime
from app import app, dtos, models
from flask import request, json
from bson import ObjectId
import uuid

@app.route('/')
def index():
  return '<h1>Todo API</h1>'

@app.route('/createTodoList', methods = ['POST'])
def createTodoList():
    json_request = json.loads(request.data)
    dto_todo_list = dtos.TodoList(**json_request)
    
    todo_models: list[models.Todo] = []
    if(len(dto_todo_list.todos) > 0):
      for todo in dto_todo_list.todos:
        todo_model = models.Todo(
          text = todo.text,
          due_date = todo.due_date,
          status = todo.status
        )
        todo_models.append(todo_model)
    
    todo_list_model = models.TodoList(
      name = dto_todo_list.name,
      creation_date = dto_todo_list.creation_date,
      todos = todo_models
    ).save()
 
    return todo_list_model.to_json()
  
@app.route('/getAllTodoLists', methods = ['GET'])
def getTodoLists():
    return models.TodoList.objects.all().to_json()
  
@app.route('/getTodoList/<listId>/', methods = ['GET'])
def getTodoList(listId):
    listInstance = ObjectId(str(listId).removeprefix('listId='))  
    
    return models.TodoList.objects(pk=listInstance).to_json()
  
@app.route('/updateTodoList/<listId>/', methods = ['PUT'])
def updateTodoList(listId):
  json_request = json.loads(request.data)
  listInstance = ObjectId(str(listId).removeprefix('listId='))

  models.TodoList.objects(pk=listInstance).update_one(set__name=json_request['name'])
  
  return models.TodoList.objects(pk=listInstance).to_json()
  
@app.route('/createTodo/<listId>/', methods = ['POST'])
def createTodo(listId):
  json_request = json.loads(request.data)
  dto_todo = dtos.Todo(**json_request)
  listInstance = ObjectId(str(listId).removeprefix('listId='))  
  
  new_todo_model =  models.Todo(
    text = dto_todo.text,
    due_date = dto_todo.due_date,
    status = dto_todo.status
  )    
  models.TodoList.objects(pk=listInstance).update_one(push__todos=new_todo_model)
  
  return models.TodoList.objects(pk=listInstance).to_json()

@app.route('/deleteTodo/<listId>', methods = ['DELETE'])
def deleteTodo(listId):
  json_request = json.loads(request.data)
  listInstance = ObjectId(str(listId).removeprefix('listId='))  
  todo_uuid = uuid.UUID(json_request['id'])
  
  models.TodoList.objects(pk=listInstance).update_one(pull__todos__id = todo_uuid)
  
  return models.TodoList.objects(pk=listInstance).to_json()

@app.route('/updateTodo/<listId>', methods = ['PUT'])
def updateTodo(listId):
  json_request = json.loads(request.data)
  dto_todo = dtos.Todo(**json_request)  
  listInstance = ObjectId(str(listId).removeprefix('listId='))
  todo_uuid = uuid.UUID(dto_todo.id)

  updated_todo_model = models.Todo(
    id = dto_todo.id, 
    text = dto_todo.text, 
    due_date =  datetime.datetime.strptime(dto_todo.due_date, '%Y-%m-%dT%H:%M:%S.%f%z'), 
    status = dto_todo.status)
  
  models.TodoList.objects(todos__id=todo_uuid).update_one(set__todos__S=updated_todo_model)
  
  return models.TodoList.objects(pk=listInstance).to_json()
