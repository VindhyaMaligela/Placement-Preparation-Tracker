from datetime import date
from app.models import Company, Task
from app import db

def test_dashboard_empty(client):
    """Test that the dashboard loads correctly when the database is empty."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Placement PrepTracker" in response.data
    
    # Check that stats cards display empty-state values
    assert b"Total Companies" in response.data
    assert b"Total Tasks" in response.data
    assert b"Completed Tasks" in response.data
    assert b"Pending Tasks" in response.data
    assert b"Completion Rate" in response.data
    assert b"0.0%" in response.data
    assert b"No upcoming pending tasks found." in response.data
    assert b"No companies tracked yet." in response.data

def test_dashboard_analytics(client, app):
    """Test that the dashboard displays statistics, upcoming tasks, and recent companies correctly."""
    with app.app_context():
        # Seed 3 companies with different application dates
        c1 = Company(name="Google", role="SWE", status="Interviewing", application_date=date(2026, 8, 20))
        c2 = Company(name="Meta", role="PE", status="Offered", application_date=date(2026, 8, 25))
        c3 = Company(name="Netflix", role="SWE", status="Applied", application_date=date(2026, 8, 22))
        db.session.add_all([c1, c2, c3])
        db.session.commit()

        # Seed tasks with different due dates and completion states
        # 3 Incomplete tasks
        t1 = Task(title="DSA Practice", category="DSA", due_date=date(2026, 9, 5), status="Pending", completed=False, company_id=c1.id)
        t2 = Task(title="System Design", category="Interview", due_date=date(2026, 9, 2), status="In Progress", completed=False, company_id=c2.id)
        t3 = Task(title="Resume Prep", category="Resume", due_date=date(2026, 9, 10), status="Pending", completed=False)
        # 1 Completed task
        t4 = Task(title="Aptitude Practice", category="Aptitude", due_date=date(2026, 8, 28), status="Completed", completed=True)
        db.session.add_all([t1, t2, t3, t4])
        db.session.commit()

    response = client.get('/')
    assert response.status_code == 200

    # 1. Verify statistics counts
    # Companies = 3, Total Tasks = 4, Completed Tasks = 1, Pending Tasks = 3, Completion Rate = 1/4 = 25.0%
    assert b"3" in response.data       # Total Companies count
    assert b"4" in response.data       # Total Tasks count
    assert b"1" in response.data       # Completed Tasks count
    assert b"3" in response.data       # Pending Tasks count
    assert b"25.0%" in response.data   # Completion rate

    # 2. Verify Application Status Distribution
    assert b"Interviewing" in response.data
    assert b"Offered" in response.data
    assert b"Applied" in response.data

    # 3. Verify Upcoming Tasks: only incomplete, ordered by due date: t2 (Sep 2) -> t1 (Sep 5) -> t3 (Sep 10)
    html = response.data.decode('utf-8')
    
    # Isolate the Upcoming Tasks HTML block specifically targeting header tags
    upcoming_start = html.find("Upcoming Tasks</h5>")
    recent_start = html.find("Recent Companies</h5>")
    assert upcoming_start != -1
    assert recent_start != -1
    upcoming_section = html[upcoming_start:recent_start]
    
    t2_idx = upcoming_section.find("System Design")
    t1_idx = upcoming_section.find("DSA Practice")
    t3_idx = upcoming_section.find("Resume Prep")
    t4_idx = upcoming_section.find("Aptitude Practice")

    # Completed task should NOT be in upcoming list
    assert t4_idx == -1
    
    # Assert correct ordering
    assert t2_idx != -1
    assert t1_idx != -1
    assert t3_idx != -1
    assert t2_idx < t1_idx < t3_idx

    # 4. Verify Recent Companies: ordered by application date desc: Meta (Aug 25) -> Netflix (Aug 22) -> Google (Aug 20)
    status_dist_start = html.find("Application Status Distribution</h5>")
    assert status_dist_start != -1
    recent_section = html[recent_start:status_dist_start]

    meta_idx = recent_section.find("Meta")
    netflix_idx = recent_section.find("Netflix")
    google_idx = recent_section.find("Google")

    assert meta_idx != -1
    assert netflix_idx != -1
    assert google_idx != -1
    assert meta_idx < netflix_idx < google_idx
