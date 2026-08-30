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
        # Run self-healing schema migration to add new columns if they don't exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if inspector.has_table('tasks'):
            columns = [col['name'] for col in inspector.get_columns('tasks')]
            alter_needed = False
            if 'category' not in columns:
                db.session.execute(db.text("ALTER TABLE tasks ADD COLUMN category VARCHAR(50) DEFAULT 'Other'"))
                alter_needed = True
            if 'status' not in columns:
                db.session.execute(db.text("ALTER TABLE tasks ADD COLUMN status VARCHAR(50) DEFAULT 'Pending'"))
                alter_needed = True
            if alter_needed:
                db.session.commit()
        
    print("Starting Placement Preparation Tracker on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
