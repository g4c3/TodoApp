from flask import Flask, make_response, request, redirect, url_for, abort, session, jsonify, json
from pymongo import MongoClient
from pprint import pprint


app = Flask(__name__)

@app.route('/')
def index():
  return '<h1>Todo API</h1>'

@app.route('/createTodoList', methods = ['POST'])
def createTodoList():
    todoList = json.loads(request.data)
        
    # client = MongoClient()
    client = MongoClient('mongodb://localhost:27017/')
    
    # just create a test db
    db = client.test
    employee = {"id": "101",  
    "name": "Peter",  
    "profession": "Software Engineer",  
    }  
    employees = db.employees
    # and save some info
    employees.insert_one(employee)  
    # one_employee = employees.find_one()
    pprint(employees.find_one())  
    
    # test db server
    # db = client.admin
    # server = db.command("buildinfo")
    # print("serverStatus")
    # pprint(db.command("buildinfo"))
    
    return todoList