from pymodm import MongoModel, EmbeddedMongoModel, fields, connection
from pymongo.write_concern import WriteConcern

connection.connect("mongodb://localhost:27017/db_todo", alias="todo_app_connection")

class Todo(EmbeddedMongoModel):
    text = fields.CharField(required=True)
    due_date = fields.DateTimeField(required=True)
    status = fields.BooleanField(required=True, default=False)
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'todo_app_connection'
    
class TodoList(MongoModel):
    name = fields.CharField(required=True)
    creation_date = fields.DateTimeField(required=True)
    todos = fields.ListField(fields.EmbeddedDocumentField(Todo, default = list, blank=True))
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'todo_app_connection'
