import datetime
from os import stat
from typing import List
from app import models
from bson import ObjectId

class Todo:
    def __init__(self, listId, text, due_date, status):
        self.listId: ObjectId = listId
        self.text: str = text
        self.due_date: datetime = datetime.datetime.now(datetime.timezone.utc) if (due_date == None or due_date == '' or due_date == datetime.MINYEAR) else due_date
        self.status: bool = status
        
def todoModelToDto(dbm = models.Todo):
    return Todo(text = dbm.text, due_date = dbm.due_date, status = dbm.status)
    
class TodoList(object):
    def __init__(self, name, creation_date, todos):
        self.name: str = name
        self.creation_date: datetime = datetime.datetime.now(datetime.timezone.utc) if (creation_date == None or creation_date == '' or creation_date == datetime.MINYEAR) else creation_date
        self.todos: List[Todo] = todos

def listModelToDto(dbm = models.TodoList):
    return TodoList(name = dbm.name, creation_date = dbm.creation_date, todos = dbm.todos)