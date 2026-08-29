from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Company
from app.forms import CompanyForm

companies_bp = Blueprint('companies', __name__)

@companies_bp.route('/')
def index():
    """Renders the companies list page."""
    companies = Company.query.all()
    return render_template('companies/index.html', companies=companies)

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
