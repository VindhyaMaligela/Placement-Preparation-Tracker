import os
from app import create_app, db

# Determine the environment config, defaulting to development
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Ensure the instance directory exists for SQLite database storage
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Create the database tables on startup if they don't exist
    with app.app_context():
        db.create_all()
        
    print("Starting Placement Preparation Tracker on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)
