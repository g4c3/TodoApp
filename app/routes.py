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
    
    db_todos = []
    for todo in dto_todo_list.todos:
      todo_model = models.Todo(
        text = todo.text,
        due_date = todo.due_date,
        status = todo.status
      )
      db_todos.append(todo_model)
      
    db_todo_list_model = models.TodoList(
        name = dto_todo_list.name,
        creation_date = dto_todo_list.creation_date,
        todos = db_todos        
    )    
    db_todo_list_model.save()

    json_response = dtos.TodoList.to_json(dto_todo_list)
    return json_response
  
  
@app.route('/getAllTodoLists', methods = ['GET'])
def getTodoLists():
    results = []
    for todo_list_model in models.TodoList.objects.all():
      todoListDto = dtos.listModelToDto(todo_list_model)
      results.append(dtos.TodoList.to_json(todoListDto))
      
    return results
  
# ?not working route with params
# @app.route('/getTodoList/<uuid>', methods = ['POST','GET'])
@app.route('/getTodoList', methods = ['GET'])
def getTodoList():
    json_request = json.loads(request.data)
    todo_list_id = json_request['id']
    objInstance = ObjectId(todo_list_id)   
    dto_todo_list: dtos.TodoList    
    for todo_list in models.TodoList.objects.raw({'_id': objInstance}):
      dto_todo_list = dtos.listModelToDto(todo_list)
      
    json_response = dtos.TodoList.to_json(dto_todo_list)
    return json_response
  
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
    
    dto_todo_list: dtos.TodoList    
    for todoList in models.TodoList.objects.raw({'_id': objInstance}):
      dto_todo_list = dtos.listModelToDto(todoList)
    
    return json.dumps(dto_todo_list.__dict__)
