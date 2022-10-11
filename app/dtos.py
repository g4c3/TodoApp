import datetime, json
from app import models
import uuid

class Todo(object):
    def __init__(self, text, due_date, status, id = uuid.uuid4()):
        self.id: uuid.uuid4() = id 
        self.text: str = text
        self.due_date: datetime = datetime.datetime.now(datetime.timezone.utc) if (due_date == None or due_date == '' or due_date == datetime.MINYEAR) else due_date
        self.status: bool = status
    
class TodoList(object):
    def __init__(self, name, creation_date, todos: list[Todo]):
        self.name: str = name
        self.creation_date: datetime = datetime.datetime.now(datetime.timezone.utc) if (creation_date == None or creation_date == '' or creation_date == datetime.MINYEAR) else creation_date
        self.todos: list[Todo] = []
        for todo in todos:
            if(isinstance(todo, models.Todo)):
                self.todos.append(Todo(id = todo.id, text = todo.text, due_date = todo.due_date, status = todo.status))
            else:
                self.todos.append(Todo(**todo))