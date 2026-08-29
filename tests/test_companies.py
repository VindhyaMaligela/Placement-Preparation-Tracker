from datetime import date
from app.models import Company
from app import db

def test_companies_index_empty(client):
    """Test the companies listing page when no data exists."""
    response = client.get('/companies/')
    assert response.status_code == 200
    assert b"No Companies Tracked Yet" in response.data

def test_create_company(client, app):
    """Test creating a company with valid inputs."""
    # Verify add company page loads
    response = client.get('/companies/new')
    assert response.status_code == 200
    assert b"Add Company" in response.data
    
    # POST valid company details
    response = client.post('/companies/new', data={
        'name': 'Netflix',
        'role': 'SWE Intern',
        'status': 'Applied',
        'application_date': '2026-08-29',
        'notes': 'Referred by alumni.'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Company &#34;Netflix&#34; has been successfully added!' in response.data
    assert b'Netflix' in response.data
    assert b'SWE Intern' in response.data

    # Check database record
    with app.app_context():
        company = Company.query.filter_by(name='Netflix').first()
        assert company is not None
        assert company.role == 'SWE Intern'
        assert company.status == 'Applied'
        assert company.application_date == date(2026, 8, 29)
        assert company.notes == 'Referred by alumni.'

def test_create_company_invalid(client):
    """Test form validation errors when fields are empty."""
    # Post empty name
    response = client.post('/companies/new', data={
        'name': '',
        'role': 'SWE Intern',
        'status': 'Applied'
    })
    assert response.status_code == 200
    assert b"Company name is required." in response.data

    # Post empty role
    response = client.post('/companies/new', data={
        'name': 'Netflix',
        'role': '',
        'status': 'Applied'
    })
    assert response.status_code == 200
    assert b"Job role is required." in response.data

def test_edit_company(client, app):
    """Test editing an existing company's details."""
    with app.app_context():
        # Seed a company
        company = Company(name='Amazon', role='SDE I', status='Interested')
        db.session.add(company)
        db.session.commit()
        company_id = company.id

    # Verify form loads with values
    response = client.get(f'/companies/{company_id}/edit')
    assert response.status_code == 200
    assert b"Edit Company" in response.data
    assert b"Amazon" in response.data

    # Save changes
    response = client.post(f'/companies/{company_id}/edit', data={
        'name': 'Amazon Inc.',
        'role': 'SDE II',
        'status': 'Interviewing',
        'notes': 'System Design round scheduled.'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Company &#34;Amazon Inc.&#34; has been updated!' in response.data
    assert b'Amazon Inc.' in response.data
    assert b'SDE II' in response.data

    # Verify database updates
    with app.app_context():
        company = Company.query.get(company_id)
        assert company.name == 'Amazon Inc.'
        assert company.role == 'SDE II'
        assert company.status == 'Interviewing'

def test_delete_company(client, app):
    """Test deleting a company record."""
    with app.app_context():
        # Seed a company
        company = Company(name='Meta', role='SWE', status='Rejected')
        db.session.add(company)
        db.session.commit()
        company_id = company.id

    # Post delete request
    response = client.post(f'/companies/{company_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Company &#34;Meta&#34; has been deleted.' in response.data

    # Check database
    with app.app_context():
        company = Company.query.get(company_id)
        assert company is None
