from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_by_name

# Initialize SQLAlchemy without binding it to a specific app instance yet
db = SQLAlchemy()

def create_app(config_name='development'):
    """Application factory function to configure and initialize the Flask app."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the configuration settings
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))
    
    # Initialize SQLAlchemy with the Flask application
    db.init_app(app)
    
    # Import routes within factory to avoid circular dependencies
    from app.routes.dashboard import dashboard_bp
    from app.routes.companies import companies_bp
    from app.routes.tasks import tasks_bp
    
    # Register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(companies_bp, url_prefix='/companies')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    
    return app
