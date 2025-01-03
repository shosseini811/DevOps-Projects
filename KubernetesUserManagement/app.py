from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from kubernetes import client, config
from datetime import datetime, timedelta, timezone
from functools import wraps
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enhanced Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:123456@localhost:5432/k8s_users')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Enhanced Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)

    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

# Role-based access control decorator
def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = User.query.filter_by(username=get_jwt_identity()).first()
            if not current_user:
                return jsonify({"error": "User not found"}), 404
            if not current_user.is_active:
                return jsonify({"error": "User account is deactivated"}), 403
            if current_user.role not in roles:
                return jsonify({"error": "Insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Initialize database with default users
def init_db():
    with app.app_context():
        try:
            logger.info("Starting database initialization...")
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Check if admin user exists
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(
                    username='admin',
                    email='admin@example.com',
                    password=os.getenv('ADMIN_PASSWORD', 'admin123'),  # Change in production
                    role='admin'
                )
                db.session.add(admin_user)
                
                # Add a test user
                test_user = User(
                    username='test_user',
                    email='test@example.com',
                    password='test123',  # Change in production
                    role='user'
                )
                db.session.add(test_user)
                
                db.session.commit()
                logger.info("Database initialized with default users")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error initializing database: {str(e)}")
            raise  # Re-raise the exception to see the full error

# Enhanced Routes
@app.route('/api/register', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def register():
    try:
        data = request.get_json()
        required_fields = ['username', 'email', 'password']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
            
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=data.get('role', 'user')
        )
        
        db.session.add(user)
        db.session.commit()
        logger.info(f"New user registered: {user.username}")
        
        return jsonify({'message': 'User created successfully'}), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error in user registration: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
            
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
            
        # Update last login time
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()
        
        access_token = create_access_token(identity=user.username)
        logger.info(f"User logged in: {user.username}")
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/')
def home():
    return render_template('home.html')

# Admin routes
@app.route('/api/users', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None
        } for user in users]), 200
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def create_k8s_namespace(username):
    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()

    v1 = client.CoreV1Api()
    
    namespace = client.V1Namespace(
        metadata=client.V1ObjectMeta(
            name=f"user-{username}"
        )
    )
    
    try:
        v1.create_namespace(namespace)
        logger.info(f"Created Kubernetes namespace for user: {username}")
    except Exception as e:
        logger.error(f"Error creating namespace: {str(e)}")
        raise

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Initialize database with default users
    app.run(host='0.0.0.0', port=5001)
