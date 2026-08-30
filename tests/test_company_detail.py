from app.models import Company, Task
from app import db

def test_company_detail_loads(client, app):
    """Test that the company details page loads correctly."""
    with app.app_context():
        company = Company(name='Apple', role='iOS Developer', status='Applied', notes='Applied through career site.')
        db.session.add(company)
        db.session.commit()
        company_id = company.id

    response = client.get(f'/companies/{company_id}')
    assert response.status_code == 200
    assert b"Apple" in response.data
    assert b"iOS Developer" in response.data
    assert b"Applied" in response.data
    assert b"Applied through career site." in response.data

def test_company_detail_tasks_linkage(client, app):
    """Test that only tasks linked to this company show on detail page."""
    with app.app_context():
        company1 = Company(name='Apple', role='iOS Developer')
        company2 = Company(name='Google', role='Android Developer')
        db.session.add_all([company1, company2])
        db.session.commit()
        
        # Link task 1 to Apple
        task1 = Task(title='Swift syntax review', category='DSA', company_id=company1.id)
        # Link task 2 to Google
        task2 = Task(title='Kotlin coroutines review', category='DSA', company_id=company2.id)
        # Create unlinked task
        task3 = Task(title='General Resume update', category='Resume')
        db.session.add_all([task1, task2, task3])
        db.session.commit()
        
        c1_id = company1.id

    # Get details for Apple (company1)
    response = client.get(f'/companies/{c1_id}')
    assert response.status_code == 200
    assert b"Swift syntax review" in response.data
    assert b"Kotlin coroutines review" not in response.data
    assert b"General Resume update" not in response.data

def test_company_detail_prepopulates_new_task(client, app):
    """Test that company_id query param pre-populates task creation select option."""
    with app.app_context():
        company = Company(name='Apple', role='iOS Developer')
        db.session.add(company)
        db.session.commit()
        company_id = company.id

    response = client.get(f'/tasks/new?company_id={company_id}')
    assert response.status_code == 200
    # Check that option is selected in select dropdown
    # WTForms renders: <option selected value="X">
    expected_selected = f'selected value="{company_id}"'
    assert expected_selected.encode() in response.data
