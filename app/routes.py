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
  
@app.route('/updateTodoList/<listId>/', methods = ['PUT'])
def updateTodoList(listId):
    json_request = json.loads(request.data)
    listInstance = ObjectId(str(listId).removeprefix('listId='))
    
    models.TodoList.objects.raw({
      "_id" : listInstance
    }).update(
      {'$set': {
        "name": json_request['name'],
        "todos": json_request['todos']       
      }}
    )
    
    dto_todo_list: dtos.TodoList    
    for todoList in models.TodoList.objects.raw({'_id': listInstance}):
      dto_todo_list = dtos.listModelToDto(todoList)      

    json_response = dtos.TodoList.to_json(dto_todo_list)
    return json_response
  
@app.route('/createTodo/<listId>/', methods = ['POST'])
def createTodo(listId):
  json_request = json.loads(request.data)
  dto_todo = dtos.Todo(**json_request)
  # maybe some cast or mapping would be better
  listInstance = ObjectId(str(listId).removeprefix('listId='))  
  
  new_todo_model =  models.Todo(
    text = dto_todo.text,
    due_date = dto_todo.due_date,
    status = dto_todo.status
  )
    
  todo_list_model: models.TodoList
  for todo_list in models.TodoList.objects.raw({'_id': listInstance}):
    todo_list_model = todo_list
    
  todo_list_model.todos.append(new_todo_model)
  todo_list_model.save()

  dto_todo_list = dtos.listModelToDto(todo_list_model)
  json_response = dtos.TodoList.to_json(dto_todo_list)
  
  return json_response


app.run(debug=True, port=5000)