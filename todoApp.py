from flask import Flask, jsonify, request, abort
from http import HTTPStatus
import json
import sqlOperations
from typing import Dict, Any

app = Flask('todoapp')
sqlOp = sqlOperations.SqlOperation()
sqlOp.create_table()

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """Get all tasks from the database."""
    try:
        tasks = sqlOp.select_all_tasks()
        return jsonify(tasks), HTTPStatus.OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    try:
        data = request.get_json()
        if not data or 'id' not in data or 'content' not in data:
            return jsonify({'error': 'Missing required fields'}), HTTPStatus.BAD_REQUEST
        
        task = (data['id'], data['content'], False)
        sqlOp.add_task(task)
        return jsonify({'message': 'Task created successfully'}), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id: str):
    """Get a specific task by ID."""
    try:
        task = sqlOp.get_task(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), HTTPStatus.NOT_FOUND
        return jsonify(task), HTTPStatus.OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id: str):
    """Update a task's status."""
    try:
        if not sqlOp.get_task(task_id):
            return jsonify({'error': 'Task not found'}), HTTPStatus.NOT_FOUND
        
        sqlOp.update_task(task_id)
        return jsonify({'message': f'Task {task_id} updated successfully'}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id: str):
    """Delete a task."""
    try:
        if not sqlOp.get_task(task_id):
            return jsonify({'error': 'Task not found'}), HTTPStatus.NOT_FOUND
            
        sqlOp.delete_task(task_id)
        return jsonify({'message': f'Task {task_id} deleted successfully'}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), HTTPStatus.NOT_FOUND

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)