from datetime import datetime
from bson import ObjectId


def log_datetime(func):
    '''Log the date and time of a function'''

    def wrapper():
        print(
            f'Function: {func.__name__}\nRun on: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'{"-"*30}')
        return func()

    return wrapper


def track_time_spent(name):
    def decorator(f):
        def wrapped(*args, **kwargs):
            start = datetime.now()
            ret = f(*args, **kwargs)
            delta = datetime.now() - start
            print(name, "took", delta.total_seconds(), "seconds")
            return ret
        return wrapped
    return decorator


def remove_prefix(func):
    def decorated_function(listId, *args, **kwargs):
        id = ObjectId(str(listId).removeprefix('listId='))
        return func(id)
    decorated_function.__name__ = func.__name__
    return decorated_function
