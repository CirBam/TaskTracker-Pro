"""
Entry point for configuration of the server, connecting to the database, and create the tables
"""

from flask import Flask
from models import db # From models.py
import os

def create_app():
    """
    Will create a flask app instance
    """
    app = Flask(__name__)

    app.config['KEY'] = 'floridapoly' # Session management key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasktracker.db' # Will create a file in the instance folder for database configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context(): # To create tables if they dont exist
        db.create_all()
        print("Database tables successfully created")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=5000, debug=True) # Runs the server on http://localhost:5000/