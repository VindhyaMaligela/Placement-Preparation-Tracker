from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Company
from app.forms import CompanyForm

companies_bp = Blueprint('companies', __name__)

@companies_bp.route('/')
def index():
    """Renders the companies list page with search and status filters."""
    query = Company.query
    search_query = request.args.get('search', '').strip()
    status_query = request.args.get('status', '').strip()
    
    if search_query:
        query = query.filter(Company.name.ilike(f'%{search_query}%') | Company.role.ilike(f'%{search_query}%'))
    if status_query:
        query = query.filter(Company.status.ilike(status_query))
        
    companies = query.all()
    return render_template('companies/index.html', companies=companies, search=search_query, status=status_query)

@companies_bp.route('/new', methods=['GET', 'POST'])
def new_company():
    """Route to add a new company."""
    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(
            name=form.name.data,
            role=form.role.data,
            status=form.status.data,
            application_date=form.application_date.data,
            notes=form.notes.data
        )
        db.session.add(company)
        db.session.commit()
        flash(f'Company "{company.name}" has been successfully added!', 'success')
        return redirect(url_for('companies.index'))
    return render_template('companies/form.html', form=form, title='Add Company')

@companies_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_company(id):
    """Route to edit an existing company."""
    company = Company.query.get_or_404(id)
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        company.name = form.name.data
        company.role = form.role.data
        company.status = form.status.data
        company.application_date = form.application_date.data
        company.notes = form.notes.data
        db.session.commit()
        flash(f'Company "{company.name}" has been updated!', 'success')
        return redirect(url_for('companies.index'))
    return render_template('companies/form.html', form=form, title='Edit Company', company=company)

@companies_bp.route('/<int:id>/delete', methods=['POST'])
def delete_company(id):
    """Route to delete an existing company."""
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    flash(f'Company "{company.name}" has been deleted.', 'danger')
    return redirect(url_for('companies.index'))

@companies_bp.route('/<int:id>', methods=['GET'])
def company_detail(id):
    """Route to view details of a specific company and its linked tasks."""
    company = Company.query.get_or_404(id)
    return render_template('companies/detail.html', company=company)
