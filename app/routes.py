from app import app, dtos, models, models_ref
from flask import request, json
from bson import ObjectId

@app.route('/')
def index():
  return '<h1>Todo API</h1>'

@app.route('/createTodoList', methods = ['POST'])
def createTodoList():
    json_request = json.loads(request.data)
    dto_todo_list = dtos.TodoList(**json_request)
    
    todo_engine_models: list[models_ref.Todo] = []
    if(len(dto_todo_list.todos) > 0):
      for todo in dto_todo_list.todos:
        todo_engine_model = models_ref.Todo(
          text = todo.text,
          due_date = todo.due_date,
          status = todo.status
        )
        todo_engine_models.append(todo_engine_model)
    
    todo_list_engine_model = models_ref.TodoList(
      name = dto_todo_list.name,
      creation_date = dto_todo_list.creation_date,
      todos = todo_engine_models
    )
    
    todo_list_engine_model.save()

    json_response = dtos.TodoList.to_json(dto_todo_list)
    return json_response
  
  
@app.route('/getAllTodoLists', methods = ['GET'])
def getTodoLists():
    json_arr_response = []
    for todo_list_model in models_ref.TodoList.objects.all():
      todo_list_dto = dtos.listModelToDto(todo_list_model)
      json_arr_response.append(dtos.TodoList.to_json(todo_list_dto))
      
    return json_arr_response
  
@app.route('/getTodoList/<listId>/', methods = ['GET'])
def getTodoList(listId):
    listInstance = ObjectId(str(listId).removeprefix('listId='))  
    dto_todo_list: dtos.TodoList    
    
    for todo_list_model in models_ref.TodoList.objects(pk=listInstance):
      dto_todo_list = dtos.listModelToDto(todo_list_model)      
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