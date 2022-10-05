from asyncio.windows_events import NULL
from app import app, dtos, models
from flask import request, json

@app.route('/')
def index():
  return '<h1>Todo API</h1>'

@app.route('/createTodoList', methods = ['POST'])
def createTodoList():
    json_request = json.loads(request.data)
    dto_todo_list = dtos.TodoList(**json_request)
    print(dto_todo_list.creation_date)
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
      db_model.append(models.TodoList.parse_json(todoList))
    return db_model