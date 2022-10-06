from asyncio.windows_events import NULL
from app import app, dtos, models
from flask import request, json
from bson import ObjectId

@app.route('/')
def index():
  return '<h1>Todo API</h1>'

@app.route('/createTodoList', methods = ['POST'])
def createTodoList():
    json_request = json.loads(request.data)
    dto_todo_list = dtos.TodoList(**json_request)
    db_model = models.TodoList(
        name = dto_todo_list.name,
        creation_date = dto_todo_list.creation_date,
        todos = dto_todo_list.todos
    )    
    db_model.save()
    
    return json.dumps(dto_todo_list.__dict__)
  
  
@app.route('/getAllTodoLists', methods = ['GET'])
def getTodoLists():
    db_model = []
    for todoList in models.TodoList.objects.all():
      modelDto = dtos.listModelToDto(todoList)
      db_model.append(json.dumps(modelDto.__dict__))
      
    return db_model
  
# ?not working route with params
# @app.route('/getTodoList/<uuid>', methods = ['POST','GET'])
@app.route('/getTodoList', methods = ['GET'])
def getTodoList():
    json_request = json.loads(request.data)
    id = json_request['id']
    objInstance = ObjectId(id)   
    todoListDto: dtos.TodoList    
    for todoList in models.TodoList.objects.raw({'_id': objInstance}):
      todoListDto = dtos.listModelToDto(todoList)
      
    return json.dumps(todoListDto.__dict__)
  
@app.route('/updateTodoList', methods = ['PUT'])
def updateTodoList():
    json_request = json.loads(request.data)
    objInstance = ObjectId(json_request['_id'])
    
    models.TodoList.objects.raw({
      "_id" : objInstance
    }).update(
      {'$set': {
        "name": json_request['name'],
        "todos": json_request['todos']       
      }}
    )
    
    todoListDto: dtos.TodoList    
    for todoList in models.TodoList.objects.raw({'_id': objInstance}):
      todoListDto = dtos.listModelToDto(todoList)
    
    return json.dumps(todoListDto.__dict__)