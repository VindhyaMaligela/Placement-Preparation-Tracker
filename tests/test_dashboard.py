from app.models import Company, Task
from app import db

def test_dashboard_empty(client):
    """Test that the dashboard loads correctly when the database is empty."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Placement PrepTracker" in response.data
    # Default values of 0 and 0.0%
    assert b"0" in response.data
    assert b"0.0%" in response.data

def test_dashboard_with_data(client, app):
    """Test that the dashboard displays database statistics correctly."""
    with app.app_context():
        # Seed a test company
        company = Company(name="TechCorp", role="Developer", status="Interviewing")
        db.session.add(company)
        db.session.commit()

        # Seed test tasks (1 completed, 1 pending = 50% completion rate)
        task1 = Task(title="Prepare System Design", completed=True, company_id=company.id)
        task2 = Task(title="Practice DSA Problems", completed=False, company_id=company.id)
        db.session.add_all([task1, task2])
        db.session.commit()

    response = client.get('/')
    assert response.status_code == 200
    
    # Check that seeded company statistics show up
    assert b"1" in response.data  # 1 Company, 1 completed task
    assert b"50.0%" in response.data  # 50.0% completion rate
    assert b"Interviewing" in response.data  # Distribution status
