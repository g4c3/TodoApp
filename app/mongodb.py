from pymongo import MongoClient

def get_dbclient():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.db_todo
    
    return db
    