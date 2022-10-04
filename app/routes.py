from app import app, mongodb
from flask import request, json

@app.route('/')
def index():
  return '<h1>Todo API</h1>'

@app.route('/createTodoList', methods = ['POST'])
def createTodoList():
    todoList = json.loads(request.data)
    
    db = mongodb.get_dbclient()
    tb_todo_list = db.todo_list
    tb_todo_list.insert_one(request.data)

    return todoList