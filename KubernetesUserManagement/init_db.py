from app import app, db, User
from sqlalchemy import text

def init_database():
    with app.app_context():
        # Drop all tables with CASCADE
        db.session.execute(text('DROP TABLE IF EXISTS resource_quota CASCADE'))
        db.session.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
        db.session.commit()
        
        # Create all tables
        db.create_all()
        
        print("Database tables created successfully!")

if __name__ == "__main__":
    init_database() 