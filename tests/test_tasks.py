from datetime import date
from app.models import Task, Company
from app import db

def test_tasks_index_empty(client):
    """Test the tasks listing page when no data exists."""
    response = client.get('/tasks/')
    assert response.status_code == 200
    assert b"No Preparation Tasks Yet" in response.data

def test_create_task(client, app):
    """Test creating a task with valid inputs."""
    response = client.get('/tasks/new')
    assert response.status_code == 200
    assert b"Add Task" in response.data

    # POST valid task details
    response = client.post('/tasks/new', data={
        'title': 'Solve 10 Leetcode Problems',
        'description': 'Solve easy and medium array questions.',
        'category': 'DSA',
        'due_date': '2026-08-30',
        'status': 'Pending',
        'company_id': -1
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Task &#34;Solve 10 Leetcode Problems&#34; has been successfully added!' in response.data
    assert b'Solve 10 Leetcode Problems' in response.data

    with app.app_context():
        task = Task.query.filter_by(title='Solve 10 Leetcode Problems').first()
        assert task is not None
        assert task.description == 'Solve easy and medium array questions.'
        assert task.category == 'DSA'
        assert task.due_date == date(2026, 8, 30)
        assert task.status == 'Pending'
        assert task.completed is False
        assert task.company_id is None

def test_create_task_linked_to_company(client, app):
    """Test creating a task linked to an existing company."""
    with app.app_context():
        company = Company(name='Microsoft', role='Software Engineer')
        db.session.add(company)
        db.session.commit()
        company_id = company.id

    response = client.post('/tasks/new', data={
        'title': 'Resume Tailoring',
        'description': 'Add cloud experience.',
        'category': 'Resume',
        'due_date': '2026-08-30',
        'status': 'In Progress',
        'company_id': company_id
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Resume Tailoring' in response.data
    assert b'Microsoft' in response.data

    with app.app_context():
        task = Task.query.filter_by(title='Resume Tailoring').first()
        assert task is not None
        assert task.company_id == company_id
        assert task.completed is False

def test_create_task_invalid(client):
    """Test form validation when fields are empty."""
    # Post empty title
    response = client.post('/tasks/new', data={
        'title': '',
        'category': 'Other',
        'status': 'Pending'
    })
    assert response.status_code == 200
    assert b"Task title is required." in response.data

def test_edit_task(client, app):
    """Test editing an existing task."""
    with app.app_context():
        task = Task(title='Mock Interview 1', category='Interview', status='Pending')
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.get(f'/tasks/{task_id}/edit')
    assert response.status_code == 200
    assert b"Edit Task" in response.data

    response = client.post(f'/tasks/{task_id}/edit', data={
        'title': 'Mock Interview 1 - Feedback Fixes',
        'description': 'Fix OOP weaknesses.',
        'category': 'Interview',
        'due_date': '2026-08-31',
        'status': 'Completed',
        'company_id': -1
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Task &#34;Mock Interview 1 - Feedback Fixes&#34; has been updated!' in response.data

    with app.app_context():
        task = Task.query.get(task_id)
        assert task.title == 'Mock Interview 1 - Feedback Fixes'
        assert task.status == 'Completed'
        assert task.completed is True

def test_complete_task(client, app):
    """Test marking a task completed through the complete shortcut route."""
    with app.app_context():
        task = Task(title='Aptitude Quant practice', category='Aptitude', status='Pending', completed=False)
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.post(f'/tasks/{task_id}/complete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Task &#34;Aptitude Quant practice&#34; has been marked as Completed!' in response.data

    with app.app_context():
        task = Task.query.get(task_id)
        assert task.status == 'Completed'
        assert task.completed is True

def test_delete_task(client, app):
    """Test deleting a task."""
    with app.app_context():
        task = Task(title='Leetcode Hard problem', category='DSA', status='Pending')
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.post(f'/tasks/{task_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Task &#34;Leetcode Hard problem&#34; has been deleted.' in response.data

    with app.app_context():
        task = Task.query.get(task_id)
        assert task is None
