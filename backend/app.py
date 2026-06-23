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

    @app.route('/')
    def home():
        return {"message": "TaskTracker Pro API is running!"}, 200

    @app.route("/api/register", methods=['POST'])
    def register_user():
        data = request.json
        status, user = auth.authenticate(data['username'], data['password'])

        if status == auth.AUTH_SUCCESS:
            return jsonify({"message": "User registered successfully"}), 201
        return jsonify({"error": status}), 400

    @app.route("/api/login", methods=['POST'])
    def login_user():
        data = request.json
        status, user = auth.authenticate(data['username'], data['password'])
        if status == auth.AUTH_SUCCESS:
            return jsonify({"message": "User logged in"}), 200
        return jsonify({"error": status}), 400

    @app.route("/api/tasks", methods=['POST'])
    def get_tasks():
        user_id = 1
        user_tasks = tasks.get_tasks_for_user(user_id)

        task_list = [tasks.task_to_dict(t) for t in user_tasks]
        return jsonify({"tasks": task_list}), 200

    @app.route("/api/tasks", methods=['POST'])
    def add_tasks():
        data = request.json

        try:
            new_task = tasks.create_task(
                user_id=1,
                title=data.get('title'),
                description=data.get('desc'),
                priority=data.get('priority'),
                date=data.get('date'),
                category=data.get('category'),
            )
            return jsonify(tasks.task_to_dict(new_task)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', debug=True, port=5000)