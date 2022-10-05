from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')

def get_client():
    return client

def get_db_todo():
    db = client.db_todo    
    return db
    
def close_mongo_db_connection():
    client.close()