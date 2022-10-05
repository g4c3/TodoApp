import datetime
from typing import List

class Todo:
    text: str
    due_date: datetime
    status: bool
    
class TodoList(object):
    def __init__(self, name, creation_date, todos):
        self.name: str = name
        self.creation_date: datetime = datetime.datetime.now(datetime.timezone.utc) if (creation_date == None or creation_date == '' or creation_date == datetime.MINYEAR) else creation_date
        self.todos: List[Todo] = todos
