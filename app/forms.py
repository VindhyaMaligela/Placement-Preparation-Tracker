from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class CompanyForm(FlaskForm):
    """Form for adding and editing tracked companies."""
    name = StringField('Company Name', validators=[
        DataRequired(message="Company name is required."),
        Length(max=100, message="Name must be under 100 characters.")
    ])
    role = StringField('Job Role', validators=[
        DataRequired(message="Job role is required."),
        Length(max=100, message="Role must be under 100 characters.")
    ])
    status = SelectField('Application Status', choices=[
        ('Interested', 'Interested'),
        ('Applied', 'Applied'),
        ('Interviewing', 'Interviewing'),
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected')
    ], default='Interested')
    application_date = DateField('Application Date', validators=[Optional()], format='%Y-%m-%d')
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Company')

class TaskForm(FlaskForm):
    """Form for adding and editing preparation tasks."""
    title = StringField('Task Title', validators=[
        DataRequired(message="Task title is required."),
        Length(max=200, message="Title must be under 200 characters.")
    ])
    description = TextAreaField('Description / Notes', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('DSA', 'DSA (Data Structures & Algorithms)'),
        ('Aptitude', 'Aptitude'),
        ('Resume', 'Resume'),
        ('Interview', 'Interview Prep'),
        ('Other', 'Other')
    ], default='Other')
    due_date = DateField('Due Date', validators=[Optional()], format='%Y-%m-%d')
    status = SelectField('Status', choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ], default='Pending')
    company_id = SelectField('Linked Company (Optional)', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Task')
