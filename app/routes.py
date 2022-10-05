from asyncio.windows_events import NULL
from app import app, dtos, models, mongodb
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
      db_model.append(models.TodoList.parse_json(todoList))
    return db_model
  
# ?not working route with params
# @app.route('/getTodoList/<id>', methods = ['POST','GET'])
@app.route('/getTodoList', methods = ['GET'])
def getTodoList():
    id = json.loads(request.data)['id']
    objInstance = ObjectId(id)   
    
    # todoList_json = ''
    # problem with finding an object with id through the pymodm framework
    # for todoList in models.TodoList.objects.raw({'legacy_id': objInstance}):
    # for todoList in models.TodoList.objects.values().get({'_id': id}):
    #   todoList_json = models.TodoList.parse_json(todoList)
    
    # alternative: use MongoClient
    collection = mongodb.get_db_todo().todo_list
    result = collection.find_one({"_id": objInstance})
    
    return models.TodoList.parse_json(result)
  
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
    
    collection = mongodb.get_db_todo().todo_list
    result = collection.find_one({"_id": objInstance})
    
    return models.TodoList.parse_json(result)