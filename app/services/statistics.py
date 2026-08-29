from app.models import Company, Task
from app import db

def get_dashboard_stats():
    """Calculates and returns statistics for the dashboard homepage.
    
    Returns:
        dict: A dictionary containing statistics such as total companies,
              total tasks, completed tasks, pending tasks, task completion rate,
              and company status counts.
    """
    total_companies = Company.query.count()
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    
    completion_rate = 0.0
    if total_tasks > 0:
        completion_rate = round((completed_tasks / total_tasks) * 100, 1)
        
    # Get company status distribution (e.g. Applied, Interviewing, Offered, etc.)
    status_counts = db.session.query(Company.status, db.func.count(Company.id)).group_by(Company.status).all()
    status_dist = {status: count for status, count in status_counts}
    
    return {
        'total_companies': total_companies,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_rate': completion_rate,
        'status_distribution': status_dist
    }
