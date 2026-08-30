from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Task, Company
from app.forms import TaskForm

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """Renders the tasks list page."""
    tasks = Task.query.all()
    return render_template('tasks/index.html', tasks=tasks)

@tasks_bp.route('/new', methods=['GET', 'POST'])
def new_task():
    """Route to add a new preparation task."""
    form = TaskForm()
    # Dynamically populate company choices
    form.company_id.choices = [(-1, 'None / General Prep')] + [
        (c.id, f"{c.name} ({c.role})") for c in Company.query.order_by(Company.name).all()
    ]
    
    if request.method == 'GET' and request.args.get('company_id'):
        try:
            form.company_id.data = int(request.args.get('company_id'))
        except ValueError:
            pass
    
    if form.validate_on_submit():
        company_id = form.company_id.data if form.company_id.data != -1 else None
        completed = (form.status.data == 'Completed')
        
        task = Task(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            due_date=form.due_date.data,
            status=form.status.data,
            completed=completed,
            company_id=company_id
        )
        db.session.add(task)
        db.session.commit()
        flash(f'Task "{task.title}" has been successfully added!', 'success')
        return redirect(url_for('tasks.index'))
        
    return render_template('tasks/form.html', form=form, title='Add Task')

@tasks_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_task(id):
    """Route to edit an existing task."""
    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    
    # Dynamically populate company choices
    form.company_id.choices = [(-1, 'None / General Prep')] + [
        (c.id, f"{c.name} ({c.role})") for c in Company.query.order_by(Company.name).all()
    ]
    
    if request.method == 'GET':
        form.company_id.data = task.company_id if task.company_id is not None else -1
        
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.category = form.category.data
        task.due_date = form.due_date.data
        task.status = form.status.data
        task.completed = (form.status.data == 'Completed')
        task.company_id = form.company_id.data if form.company_id.data != -1 else None
        
        db.session.commit()
        flash(f'Task "{task.title}" has been updated!', 'success')
        return redirect(url_for('tasks.index'))
        
    return render_template('tasks/form.html', form=form, title='Edit Task', task=task)

@tasks_bp.route('/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """Route to delete a task."""
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash(f'Task "{task.title}" has been deleted.', 'danger')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/<int:id>/complete', methods=['POST'])
def complete_task(id):
    """Route shortcut to quickly mark a task as completed."""
    task = Task.query.get_or_404(id)
    task.status = 'Completed'
    task.completed = True
    db.session.commit()
    flash(f'Task "{task.title}" has been marked as Completed!', 'success')
    return redirect(url_for('tasks.index'))
