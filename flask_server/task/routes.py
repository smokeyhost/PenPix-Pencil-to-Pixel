# tasks_endpoint.py
from flask import request, jsonify, session
from model import db, Task, Classes
from task import task_bp
from utils.auth_helpers import login_required
from datetime import datetime
import shutil
import os
import pytz

@login_required
@task_bp.route('/create-task', methods=['POST'])
def create_task():
    user_id = session.get('user_id')  
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    data = request.json
    print(data)

    # if not all(key in data for key in ['title', 'classId', 'dueDate', 'examType', 'answerKeys', 'data', 'status', 'totalSubmissions','reviewedSubmission']):
    #     return jsonify({"error": "Missing required fields"}), 400

    try:
        due_date = datetime.fromisoformat(data['dueDate'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid date format"}), 400

    task = Task(
        title=data['title'],
        user_id=user_id,
        class_id=data['classId'],
        total_submissions=data['totalSubmissions'],  
        reviewed_submissions=data['reviewedSubmissions'], 
        due_date=due_date,
        status=data.get('status', 'Ongoing'),  
        exam_type=data['examType'],
        answer_keys=data['answerKeys'],
    )

    db.session.add(task)
    
    class_obj = Classes.query.get(data['classId'])
    if class_obj:
        class_obj.tasks.append(task) 

    db.session.commit()

    return jsonify(task.to_dict()), 201

@login_required
@task_bp.route('/get-tasks', methods=['GET'])
def list_tasks():
    user_id = session.get('user_id')  
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401
    tasks = Task.query.filter_by(user_id = user_id)
    return jsonify([task.to_dict() for task in tasks])

@login_required
@task_bp.route('/get-task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify(task.to_dict())  

@login_required
@task_bp.route('/edit-task/<int:task_id>', methods=['PATCH'])
def edit_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"message": "Task not found"}), 404

        task_data = request.json
        print(task_data)
        try:
            due_date = datetime.fromisoformat(task_data['dueDate'])
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid date format"}), 400

        task.title = task_data.get('title', task.title)
        task.exam_type = task_data.get('examType', task.exam_type)
        task.status = task_data.get('status', task.status)
        task.answer_keys = task_data.get('answerKeys', task.answer_keys)
        task.class_id = task_data.get('classId', task.class_id)
        task.due_date = due_date
        
        db.session.commit()

        return jsonify({"message": "Task updated", "task_id": task_id})

    except Exception as e:
        print(f"An error occurred: {e}")  # Log the error
        return jsonify({"message": "An error occurred while updating the task"}), 500

@login_required
@task_bp.route('/delete-task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"message": "Task not found"}), 404

        TASK_FOLDER = os.path.join('static', 'images', str(task_id))
        if os.path.exists(TASK_FOLDER):
            shutil.rmtree(TASK_FOLDER) 

        db.session.delete(task)
        db.session.commit()

        return jsonify({"message": "Task deleted", "task_id": task_id})
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
@login_required
@task_bp.route('/delete-expression/<int:task_id>', methods=['POST'])
def delete_expression(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    expression_id = request.json.get('expression_id')
    if expression_id is None:
        return jsonify({"message": "Expression ID is required"}), 400

    try:
        expression_id = int(expression_id)
        if expression_id < 0 or expression_id >= len(task.answer_keys):
            return jsonify({"message": "Invalid expression ID"}), 400
        
        new_answer_keys = task.answer_keys.copy()
        new_answer_keys.pop(expression_id)
        task.answer_keys = new_answer_keys
        db.session.commit()
        return jsonify({"message": "Answer key deleted successfully", "answer_keys": task.answer_keys}), 200
    
    except (ValueError, IndexError):
        return jsonify({"message": "Invalid expression ID"}), 400