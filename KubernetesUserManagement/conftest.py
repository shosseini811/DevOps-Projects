import os
import sys
import pytest
from datetime import datetime, timezone

# Add the parent directory to PYTHONPATH so that app can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app import app, db, User

@pytest.fixture(scope="session")
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/k8s_users_test'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    return app

@pytest.fixture(scope="session")
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture(scope="function")
def init_database(test_app):
    with test_app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        try:
            # Create test admin user with unique timestamp
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
            admin = User(
                username=f'admin_{timestamp}',
                email=f'admin_{timestamp}@test.com',
                password='admin123',
                role='admin'
            )
            db.session.add(admin)
            
            # Create test regular user with unique timestamp
            user = User(
                username=f'test_user_{timestamp}',
                email=f'test_{timestamp}@test.com',
                password='test123',
                role='user'
            )
            db.session.add(user)
            
            db.session.commit()
            
            # Refresh the instances to ensure they are bound to the session
            db.session.refresh(admin)
            db.session.refresh(user)
            
            # Store the instances in a dict
            users = {'admin': admin, 'user': user}
            
            # Yield instead of return to keep the session alive
            yield users
            
            # Clean up after the test
            db.session.remove()
            
        except Exception as e:
            db.session.rollback()
            raise e

@pytest.fixture(scope="function")
def admin_token(test_client, init_database):
    """Get admin token for protected routes"""
    response = test_client.post('/api/login',
        json={
            'username': init_database['admin'].username,
            'password': 'admin123'
        }
    )
    return response.json['access_token']

@pytest.fixture(scope="function")
def user_token(test_client, init_database):
    """Get user token for protected routes"""
    response = test_client.post('/api/login',
        json={
            'username': init_database['user'].username,
            'password': 'test123'
        }
    )
    return response.json['access_token'] 