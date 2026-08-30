from datetime import datetime
from app import db

class Company(db.Model):
    """Placeholder model representing a company being tracked for placements."""
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Interested')  # Interested, Applied, Interviewing, Offered, Rejected
    application_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # One-to-many relationship: One company can have multiple preparation tasks
    tasks = db.relationship('Task', backref='company', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Company {self.name} - {self.role}>'

class Task(db.Model):
    """Model representing preparation tasks (e.g. Resume update, LeetCode, Mock interview)."""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='Other')     # DSA, Aptitude, Resume, Interview, Other
    due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), default='Pending')      # Pending, In Progress, Completed
    completed = db.Column(db.Boolean, default=False)
    
    # Foreign key linking the task to a specific company
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)

    def __repr__(self):
        return f'<Task {self.title} - Status: {self.status}>'
