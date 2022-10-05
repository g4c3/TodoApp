from pymodm import MongoModel, EmbeddedMongoModel, fields, connection
from pymongo.write_concern import WriteConcern
from flask import json
from bson import json_util

connection.connect("mongodb://localhost:27017/db_todo", alias="todo_app_connection")


class Todo(EmbeddedMongoModel):
    text = fields.CharField(required=True)
    due_date = fields.DateTimeField(required=True)
    status = fields.BooleanField(required=True, default=False)
    
class TodoList(MongoModel):
    name = fields.CharField(required=True)
    creation_date = fields.DateTimeField(required=True)
    todos = fields.EmbeddedDocumentListField(Todo, default=[], blank=True)
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'todo_app_connection'
        
    # !there is something missing with the serialization process
    def parse_json(data):
        return json.loads(json_util.dumps(data, default=json_util.default))
