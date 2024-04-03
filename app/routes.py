from flask import Flask, jsonify, request
from . import app, db
from models import Task, User
from datetime import datetime, timedelta 
from flask import abort 
from flask import login_required, current_user 
from functools import wraps
import jwt 
from flask_jwt_extended import create_access_token
from flask_basicauth import BasicAuth
from flask_httpauth import HTTPBasicAuth

basic_auth = HTTPBasicAuth()
#token_auth = HTTPTokenAuth()
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Auth-Token') 
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Create a route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    select_stmt = db.select(Task)
    # Get the tasks from the database
    tasks = db.session.execute(select_stmt).scalars().all()
    return [t.to_dict() for t in tasks]

# Create a route to get a single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Get the task from the database by ID
    task = db.session.get(Task, task_id)
    if task:
        return task.to_dict()
    else:
        return {'error': f"Task with an ID of {task_id} does not exist"}, 404
    
# Create a route to create a new task
@app.route('/tasks', methods=['POST'])
def create_task(): 
    if not request.is_json:
        return jsonify({'error': "Where's the JSON buddy?"}), 400
    if 'title' in request.json:
        title = request.json['title']
    else:
        return jsonify({'error': 'Title is required'}), 400
    if 'description' in request.json:
        description = request.json['description']
    else:
        return jsonify({'error': 'Description is required'}), 400
    if 'dueDate' in request.json:
        dueDate = request.json['dueDate']
    else:
        dueDate = None
    new_task = Task(title=title, description=description, due_date=dueDate)
    return new_task.to_dict(), 201