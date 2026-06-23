"""
Entry point for configuration of the server, connecting to the database, and create the tables
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db # From models.py
import os, tasks, auth

def create_app():
    """
    Will create a flask app instance
    """
    app = Flask(__name__)

    CORS(app)  # allows frontend to make requests to the backend

    app.config['KEY'] = 'floridapoly' # Session management key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasktracker.db' # Will create a file in the instance folder for database configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context(): # To create tables if they dont exist
        db.create_all()
        print("Database tables successfully created")

    @app.route('/') # If nothing is called just testing
    def home():
        return {"message": "TaskTracker Pro API is running!"}, 200

    @app.route("/api/register", methods=['POST']) # This is an endpoint so that the frontend can fetch from here
    def register_user():
        """
        For registering a new user
        """
        data = request.json
        status, user = auth.register(data.get('username'), data.get('password')) # For better safe handling of data

        if status == auth.REGISTER_SUCCESS: # Actually testing if it registers
            return jsonify({"message": "User registered successfully"}), 201 # 201 is for the HTML status code, 201 = Created
        return jsonify({"error": status}), 400 # For basic troubleshooting, 400 = Bad Request

    @app.route("/api/login", methods=['POST'])
    def login_user():
        """
        For loging in a user
        """
        data = request.json
        status, user = auth.authenticate(data.get('username'), data.get('password'))
        if status == auth.AUTH_SUCCESS:
            # From Justin's file:
            # We return the user_id so the frontend can save it in localStorage
            return jsonify({"message": "Login successful", "user_id": user.user_id, "username": user.username}), 200
        return jsonify({"error": status}), 401 # 401 = Unauthorized user

    @app.route("/api/tasks", methods=['GET'])
    def get_tasks():
        """
        For getting a list of tasks of the user
        """
        user_id = request.args.get('user_id') # From Justin's file
        user_tasks = tasks.get_tasks_for_user(user_id)

        task_list = [tasks.task_to_dict(t) for t in user_tasks]
        return jsonify({"tasks": task_list}), 200

    @app.route("/api/tasks", methods=['POST'])
    def add_tasks():
        """
        For adding a task
        """
        data = request.json

        user_id = data.get('user_id')  # From Justin's file

        try:
            new_task = tasks.create_task(
                title=data.get('title'),
                description=data.get('description'),
                date=data.get('date'),
                priority=data.get('priority'),
                category=data.get('category'),
                user_id=user_id,
            )
            return jsonify(tasks.task_to_dict(new_task)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/tasks/<task_id>', methods=['GET'])
    def get_single_task(task_id):
        """
        For getting a single task
        """
        task = tasks.get_task(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404 # 404 = Not Found
        return jsonify(tasks.task_to_dict(task)), 200

    @app.route('/api/tasks/<task_id>/complete', methods=['PUT'])
    def complete_task(task_id):
        """
        For completing a task
        """
        success = tasks.complete_task(task_id)
        if success:
            return jsonify({"message": "Task marked complete"}), 200
        return jsonify({'error': 'Task not found'}), 404

    @app.route('/api/tasks/<task_id>/', methods=['DELETE'])
    def delete_task(task_id):
        """
        For deleting a task
        """
        deleted = tasks.delete_task(task_id)
        if deleted:
            return jsonify({"message": "Task deleted"}), 200
        return jsonify({'error': 'Task not found'}), 404

    @app.route('/api/tasks/<task_id>/', methods=['PUT'])
    def update_task(task_id):
        """
        For updating a task
        """
        data = request.json

        try:
            updated_task = tasks.update_task(
                task_id=task_id,
                title=data.get('title'),
                description=data.get('description'),
                date=data.get('date'),
                priority=data.get('priority'),
                category=data.get('category')
            )

            if updated_task is None:
                return jsonify({'error': 'Task not found'}), 404
            return jsonify(updated_task), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', debug=True, port=5000) # Runs the server on http://localhost:5000/