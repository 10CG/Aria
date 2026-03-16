from flask import Blueprint, jsonify
from backend.src.schemas.task import task_list_response

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with new paginated response format"""
    tasks = [
        {"id": 1, "name": "Task 1", "status": "pending"},
        {"id": 2, "name": "Task 2", "status": "completed"}
    ]
    return jsonify(task_list_response(tasks, total=2, page=1, page_size=10))
