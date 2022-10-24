from typing import List
from mongoengine import *
from datetime import *
import uuid

connect(host="mongodb://172.17.0.2:27017/db_todo",  w=1) # , j=True

class Todo(EmbeddedDocument):    
    id = UUIDField(required=False, default=uuid.uuid4(), binary=False)
    text = StringField(required=True, max_length=200)
    due_date = DateTimeField(default=datetime.utcnow)
    status = BooleanField(default=False)
    def __init__(self, *args, **kwargs):
        super(Todo, self).__init__(*args, **kwargs)
        self.id = kwargs['id'] if 'id' in kwargs else self.id
        self.text = kwargs['text']
        self.due_date = kwargs['due_date'] if 'due_date' in kwargs else datetime.utcnow()
        self.status = kwargs['status']           
        
class TodoList(Document):
    name = StringField(required=True, max_length=32)
    creation_date = DateTimeField(default=datetime.utcnow)
    todos = EmbeddedDocumentListField(Todo, default=[])
    def __init__(self, *args, **kwargs):
        super(TodoList, self).__init__(*args, **kwargs)
        self.name = kwargs['name']
        self.creation_date
        self.todos