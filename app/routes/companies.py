from flask import Blueprint, render_template
from app.models import Company

companies_bp = Blueprint('companies', __name__)

@companies_bp.route('/')
def index():
    """Renders the companies list page (placeholder)."""
    companies = Company.query.all()
    return render_template('companies/index.html', companies=companies)
