from mongoengine import *
import datetime

connect(host="mongodb://localhost:27017/db_todo")

class Todo(EmbeddedDocument):    
    text = StringField(required=True, max_length=200)
    due_date = DateTimeField(default=datetime.datetime.utcnow)
    status = BooleanField(default=False)

class TodoList(Document):
    name = StringField(required=True, max_length=32)
    creation_date = DateTimeField(default=datetime.datetime.utcnow)
    todos = ListField(EmbeddedDocumentField(Todo), default=[])