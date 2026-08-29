from flask import Blueprint, render_template
from app.services.statistics import get_dashboard_stats

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Renders the dashboard/homepage showing placement statistics and placeholders."""
    stats = get_dashboard_stats()
    return render_template('dashboard/index.html', stats=stats)
