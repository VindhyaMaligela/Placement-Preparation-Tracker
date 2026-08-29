from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import config_by_name

# Initialize SQLAlchemy and CSRFProtect without binding to app yet
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_name='development'):
    """Application factory function to configure and initialize the Flask app."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the configuration settings
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    
    # Import routes within factory to avoid circular dependencies
    from app.routes.dashboard import dashboard_bp
    from app.routes.companies import companies_bp
    from app.routes.tasks import tasks_bp
    
    # Register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(companies_bp, url_prefix='/companies')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    
    return app
