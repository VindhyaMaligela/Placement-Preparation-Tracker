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
