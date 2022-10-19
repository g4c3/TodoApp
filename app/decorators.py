from datetime import datetime
from bson import ObjectId

def track_time_spent(func):
    def decorated_function(*args, **kwargs):
        start = datetime.now()
        ret = func(*args, **kwargs)
        delta = datetime.now() - start
        print(func.__name__, "took", delta.total_seconds(), "seconds")
        return ret
      
    decorated_function.__name__ = func.__name__          
    return decorated_function

def remove_prefix(func):
    def decorated_function(listId):
        id = ObjectId(str(listId).removeprefix('listId='))
        return func(id)
    decorated_function.__name__ = func.__name__
    return decorated_function
