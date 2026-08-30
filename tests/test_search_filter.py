from app.models import Company, Task
from app import db

def test_companies_search_and_filter(client, app):
    """Test searching and filtering companies."""
    with app.app_context():
        c1 = Company(name="Google", role="Software Engineer", status="Interviewing")
        c2 = Company(name="Meta", role="Production Engineer", status="Offered")
        c3 = Company(name="Netflix", role="SWE", status="Applied")
        db.session.add_all([c1, c2, c3])
        db.session.commit()

    # 1. Loads with HTTP 200
    response = client.get('/companies/')
    assert response.status_code == 200
    assert b"Google" in response.data
    assert b"Meta" in response.data
    assert b"Netflix" in response.data

    # 2. Search by company name (case-insensitive)
    response = client.get('/companies/?search=gOoGlE')
    assert response.status_code == 200
    assert b"Google" in response.data
    assert b"Meta" not in response.data
    assert b"Netflix" not in response.data

    # 3. Search by role (case-insensitive)
    response = client.get('/companies/?search=pRoDuCtIoN')
    assert response.status_code == 200
    assert b"Meta" in response.data
    assert b"Google" not in response.data

    # 4. Filter by status
    response = client.get('/companies/?status=Applied')
    assert response.status_code == 200
    assert b"Netflix" in response.data
    assert b"Google" not in response.data
    assert b"Meta" not in response.data

    # 5. Search + Status combination
    response = client.get('/companies/?search=engineer&status=Offered')
    assert response.status_code == 200
    assert b"Meta" in response.data
    assert b"Google" not in response.data

    # 5b. Search + Status combination for Microsoft/Interviewing
    with app.app_context():
        c4 = Company(name="Microsoft", role="software engineering", status="Interviewing")
        db.session.add(c4)
        db.session.commit()
    response = client.get('/companies/?search=microsoft&status=Interviewing')
    assert response.status_code == 200
    assert b"Microsoft" in response.data

    # Test lowercase status query parameter compatibility
    response = client.get('/companies/?search=microsoft&status=interviewing')
    assert response.status_code == 200
    assert b"Microsoft" in response.data

    # 6. Empty search results
    response = client.get('/companies/?search=NonexistentCompany')
    assert response.status_code == 200
    assert b"No Matches Found" in response.data
    assert b"Clear Filters" in response.data


def test_tasks_search_and_filter(client, app):
    """Test searching and filtering tasks."""
    with app.app_context():
        t1 = Task(title="Solve LeetCode Arrays", category="DSA", status="Pending")
        t2 = Task(title="Resume polishing", category="Resume", status="In Progress")
        t3 = Task(title="Mock interview", category="Interview", status="Completed")
        db.session.add_all([t1, t2, t3])
        db.session.commit()

    # 1. Loads with HTTP 200
    response = client.get('/tasks/')
    assert response.status_code == 200
    assert b"Solve LeetCode Arrays" in response.data
    assert b"Resume polishing" in response.data
    assert b"Mock interview" in response.data

    # 2. Search by title (case-insensitive)
    response = client.get('/tasks/?search=lEeTcOdE')
    assert response.status_code == 200
    assert b"Solve LeetCode Arrays" in response.data
    assert b"Resume polishing" not in response.data

    # 3. Filter by category
    response = client.get('/tasks/?category=Resume')
    assert response.status_code == 200
    assert b"Resume polishing" in response.data
    assert b"Solve LeetCode Arrays" not in response.data

    # 4. Filter by status
    response = client.get('/tasks/?status=Completed')
    assert response.status_code == 200
    assert b"Mock interview" in response.data
    assert b"Solve LeetCode Arrays" not in response.data

    # 5. Search + Category + Status combination
    response = client.get('/tasks/?search=leetcode&category=DSA&status=Pending')
    assert response.status_code == 200
    assert b"Solve LeetCode Arrays" in response.data
    assert b"Resume polishing" not in response.data

    # 6. Empty search results
    response = client.get('/tasks/?search=NonexistentTask')
    assert response.status_code == 200
    assert b"No Matches Found" in response.data
    assert b"Clear Filters" in response.data


def test_companies_all_status_filters(client, app):
    """Test all company status options specifically."""
    with app.app_context():
        # Clear existing data to have a precise testing environment
        db.session.query(Company).delete()
        db.session.commit()
        
        c1 = Company(name="CoApplied", role="RoleA", status="Applied")
        c2 = Company(name="CoInterested", role="RoleB", status="Interested")
        c3 = Company(name="CoInterviewing", role="RoleC", status="Interviewing")
        c4 = Company(name="CoOffered", role="RoleD", status="Offered")
        c5 = Company(name="CoRejected", role="RoleE", status="Rejected")
        db.session.add_all([c1, c2, c3, c4, c5])
        db.session.commit()

    # Test "All Statuses" (empty status query parameter)
    response = client.get('/companies/')
    assert response.status_code == 200
    assert b"CoApplied" in response.data
    assert b"CoInterested" in response.data
    assert b"CoInterviewing" in response.data
    assert b"CoOffered" in response.data
    assert b"CoRejected" in response.data

    # Test "Applied" status filter
    response = client.get('/companies/?status=Applied')
    assert response.status_code == 200
    assert b"CoApplied" in response.data
    assert b"CoInterested" not in response.data
    assert b"CoInterviewing" not in response.data
    assert b"CoOffered" not in response.data
    assert b"CoRejected" not in response.data

    # Test "Interested" status filter
    response = client.get('/companies/?status=Interested')
    assert response.status_code == 200
    assert b"CoInterested" in response.data
    assert b"CoApplied" not in response.data
    assert b"CoInterviewing" not in response.data
    assert b"CoOffered" not in response.data
    assert b"CoRejected" not in response.data

    # Test "Interviewing" status filter
    response = client.get('/companies/?status=Interviewing')
    assert response.status_code == 200
    assert b"CoInterviewing" in response.data
    assert b"CoApplied" not in response.data
    assert b"CoInterested" not in response.data
    assert b"CoOffered" not in response.data
    assert b"CoRejected" not in response.data

    # Test "Offered" status filter
    response = client.get('/companies/?status=Offered')
    assert response.status_code == 200
    assert b"CoOffered" in response.data
    assert b"CoApplied" not in response.data
    assert b"CoInterested" not in response.data
    assert b"CoInterviewing" not in response.data
    assert b"CoRejected" not in response.data

    # Test "Rejected" status filter
    response = client.get('/companies/?status=Rejected')
    assert response.status_code == 200
    assert b"CoRejected" in response.data
    assert b"CoApplied" not in response.data
    assert b"CoInterested" not in response.data
    assert b"CoInterviewing" not in response.data
    assert b"CoOffered" not in response.data


def test_combined_search_status_combinations(client, app):
    """Test various combinations of company name/role search + status filter."""
    with app.app_context():
        # Clear database for clean tests
        db.session.query(Company).delete()
        db.session.commit()

        c1 = Company(name="Amazon", role="SDE intern", status="Applied")
        c2 = Company(name="Microsoft", role="software engineering", status="Interviewing")
        c3 = Company(name="TCS", role="Graduate Engineer Trainee", status="Offered")
        c4 = Company(name="Google", role="Associate Engineer", status="Applied")
        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()

    # 1. Amazon + Interested -> should return No Matches Found (as Amazon is Applied, not Interested)
    response = client.get('/companies/?search=Amazon&status=Interested')
    assert response.status_code == 200
    assert b"No Matches Found" in response.data
    assert b"table-responsive" not in response.data

    # 2. Microsoft + Interviewing -> should return Microsoft
    response = client.get('/companies/?search=Microsoft&status=Interviewing')
    assert response.status_code == 200
    assert b"Microsoft" in response.data
    assert b"Amazon" not in response.data

    # 3. TCS + Offered -> should return TCS
    response = client.get('/companies/?search=TCS&status=Offered')
    assert response.status_code == 200
    assert b"TCS" in response.data
    assert b"Microsoft" not in response.data

    # 4. Google + Applied -> should return Google
    response = client.get('/companies/?search=Google&status=Applied')
    assert response.status_code == 200
    assert b"Google" in response.data
    assert b"TCS" not in response.data
