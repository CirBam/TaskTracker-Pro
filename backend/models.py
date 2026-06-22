"""
For the database model for the User and Task classes
"""

from flask_sqlalchemy import SQLAlchemy #For the database
from datetime import date # For the date of the creation of the database

db = SQLAlchemy() # for database in app.py

class User(db.Model):
    """
    The primary user class for students and professors with the password and username for auth.py
    """
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    task = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    """
    The task class as a template for tasks.py
    """
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


