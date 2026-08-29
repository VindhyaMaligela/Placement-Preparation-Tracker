from flask import Blueprint, render_template
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """Renders the tasks list page (placeholder)."""
    tasks = Task.query.all()
    return render_template('tasks/index.html', tasks=tasks)
