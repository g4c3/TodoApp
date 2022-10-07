import datetime, json
from app import models, models_ref

class Todo(object):
    def __init__(self, text, due_date, status):
        self.text: str = text
        self.due_date: datetime = datetime.datetime.now(datetime.timezone.utc) if (due_date == None or due_date == '' or due_date == datetime.MINYEAR) else due_date
        self.status: bool = status
        
def todoModelToDto(dbm = models.Todo):
    return Todo(text = dbm.text, due_date = dbm.due_date, status = dbm.status)
    
class TodoList(object):
    def __init__(self, name, creation_date, todos: list[Todo]):
        self.name: str = name
        self.creation_date: datetime = datetime.datetime.now(datetime.timezone.utc) if (creation_date == None or creation_date == '' or creation_date == datetime.MINYEAR) else creation_date
        self.todos: list[Todo] = []
        
        for todo in todos:
            self.todos.append(Todo(**todo))

    # !read about the serialization configs and options in python
    def to_json(self):
        todos = []
        if(self.todos):
            for todo in self.todos:
                todos.append(json.dumps(todo.__dict__, indent=4, sort_keys=True, default=str))
        self.todos = todos
               
        return json.dumps(self.__dict__, indent=4, sort_keys=True, default=str)
    
def listModelToDto(dbm = models_ref.TodoList):
    todos: list[Todo] = []
    dto_todoList = TodoList(name = dbm.name, creation_date = dbm.creation_date, todos = todos)
    
    for db_todo in dbm.todos:
        todo = todoModelToDto(db_todo)
        todos.append(todo)
    
    dto_todoList.todos = todos;    
    return dto_todoList
