from app.models import Company, Task
from app import db

def get_dashboard_stats():
    """Calculates and returns statistics for the dashboard homepage.
    
    Returns:
        dict: A dictionary containing statistics such as total companies,
              total tasks, completed tasks, pending tasks, task completion rate,
              company status counts, upcoming incomplete tasks, and recent companies.
    """
    total_companies = Company.query.count()
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter((Task.completed == True) | (Task.status == 'Completed')).count()
    pending_tasks = total_tasks - completed_tasks
    
    completion_rate = 0.0
    if total_tasks > 0:
        completion_rate = round((completed_tasks / total_tasks) * 100, 1)
        
    # Get company status distribution (e.g. Applied, Interviewing, Offered, etc.)
    status_counts = db.session.query(Company.status, db.func.count(Company.id)).group_by(Company.status).all()
    status_dist = {status: count for status, count in status_counts}
    
    # Query upcoming incomplete tasks (Pending or In Progress), sorting due dates ascending (nulls last)
    upcoming_tasks = Task.query.filter(
        (Task.completed == False) & (Task.status != 'Completed')
    ).order_by(
        Task.due_date.is_(None).asc(),
        Task.due_date.asc()
    ).limit(5).all()
    
    # Query recently added companies, sorting by application date descending (nulls last)
    recent_companies = Company.query.order_by(
        Company.application_date.is_(None).asc(),
        Company.application_date.desc(),
        Company.id.desc()
    ).limit(5).all()
    
    return {
        'total_companies': total_companies,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_rate': completion_rate,
        'status_distribution': status_dist,
        'upcoming_tasks': upcoming_tasks,
        'recent_companies': recent_companies
    }
