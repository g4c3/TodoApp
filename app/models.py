from mongoengine import *
import datetime
import uuid

connect(host="mongodb://localhost:27017/db_todo",  w=1, j=True)

class Todo(EmbeddedDocument):
    id = UUIDField(required=False, default=uuid.uuid4(), binary=False)
    text = StringField(required=True, max_length=200)
    due_date = DateTimeField(default=datetime.datetime.utcnow)
    status = BooleanField(default=False)

class TodoList(Document):
    name = StringField(required=True, max_length=32)
    creation_date = DateTimeField(default=datetime.datetime.utcnow)
    todos = EmbeddedDocumentListField(Todo, default=[])