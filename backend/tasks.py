from models import db,Task
from datetime import datetime

def create_task(
    user_id,
    title,
    description,
    date,
    priority,
    category
):
    task_date = datetime.strptime(date, "%Y-%m-%d")
    task = Task(
        title=title,
        description=description,
        date=task_date,
        priority=priority,
        category=category,
        completed=False,
        user_id=user_id
)

    db.session.add(task)
    db.session.commit()

    return task

def get_task(task_id):
    return Task.query.get(task_id)

def get_tasks_for_user(user_id):
    return Task.query.filter_by(
        user_id=user_id
    ).all()

def update_task(
        task_id,
        title,
        description,
        date,
        priority,
        category
):
    task = Task.query.get(task_id)

    if task is None:
        return None
    
    task.title = title
    task.description = description
    task.date = datetime.strptime(date,"%Y-%m-%d")
    task.priority = priority
    task.category = category

    db.session.commit()

    return task

def complete_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return False
    
    task.completed = True

    db.session.commit()

    return True

def delete_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return False
    
    db.session.delete(task)
    db.session.commit()

    return True

def task_to_dict(task):
    return{
        "task_id": task.task_id,
        "user_id": task.user_id,
        "title": task.title,
        "description": task.description,
        "date": task.date.strftime("%Y-%m-%d"),
        "priority": task.priority,
        "category": task.category,
        "completed": task.completed
    }
    
