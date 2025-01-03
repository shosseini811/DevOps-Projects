from locust import HttpUser, task, between, events
from faker import Faker
import json
import logging

fake = Faker()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Initialize test data before load test starts"""
    if not environment.web_ui:
        logger.info("Starting load test...")
    
    # Create initial test user if needed
    with environment.runner.client.post("/api/login", 
        json={
            "username": "test_user",
            "password": "test123"
        },
        catch_response=True) as response:
        if response.status_code != 200:
            logger.warning("Test user doesn't exist, tests might fail")

class UserBehavior(HttpUser):
    wait_time = between(1, 3)
    admin_token = None
    
    def on_start(self):
        """Login as admin to get token for protected routes"""
        try:
            with self.client.post("/api/login", 
                json={
                    "username": "admin",
                    "password": "admin123"
                },
                catch_response=True) as response:
                if response.status_code == 200:
                    self.admin_token = response.json()["access_token"]
                    logger.info("Admin login successful")
                else:
                    logger.error(f"Admin login failed: {response.text}")
        except Exception as e:
            logger.error(f"Error during admin login: {str(e)}")
    
    @task(1)
    def register_user(self):
        """Simulate user registration"""
        if not self.admin_token:
            return
            
        try:
            username = fake.user_name()
            with self.client.post("/api/register", 
                json={
                    "username": username,
                    "email": fake.email(),
                    "password": "test123",
                    "role": "user"
                },
                headers={'Authorization': f'Bearer {self.admin_token}'},
                catch_response=True) as response:
                if response.status_code == 201:
                    response.success()
                elif response.status_code == 400 and b'Username already exists' in response.content:
                    response.success()  # This is also an acceptable outcome
                else:
                    response.failure(f"Registration failed: {response.text}")
        except Exception as e:
            logger.error(f"Error during user registration: {str(e)}")
    
    @task(3)
    def login_user(self):
        """Simulate user login - higher frequency than registration"""
        try:
            with self.client.post("/api/login", 
                json={
                    "username": "test_user",
                    "password": "test123"
                },
                catch_response=True) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Login failed: {response.text}")
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
    
    @task(2)
    def get_users(self):
        """Simulate admin fetching user list"""
        if not self.admin_token:
            return
            
        try:
            with self.client.get("/api/users",
                headers={'Authorization': f'Bearer {self.admin_token}'},
                catch_response=True) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Get users failed: {response.text}")
        except Exception as e:
            logger.error(f"Error during get users: {str(e)}")

class AdminUser(HttpUser):
    wait_time = between(2, 5)
    admin_token = None
    
    def on_start(self):
        """Login as admin"""
        try:
            with self.client.post("/api/login",
                json={
                    "username": "admin",
                    "password": "admin123"
                },
                catch_response=True) as response:
                if response.status_code == 200:
                    self.admin_token = response.json()["access_token"]
                    logger.info("Admin login successful")
                else:
                    logger.error(f"Admin login failed: {response.text}")
        except Exception as e:
            logger.error(f"Error during admin login: {str(e)}")
    
    @task
    def admin_tasks(self):
        """Simulate admin operations"""
        if not self.admin_token:
            return
            
        try:
            # Get users list
            with self.client.get("/api/users",
                headers={'Authorization': f'Bearer {self.admin_token}'},
                catch_response=True) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Get users failed: {response.text}")
            
            # Register new users
            for _ in range(3):
                username = fake.user_name()
                with self.client.post("/api/register",
                    json={
                        "username": username,
                        "email": fake.email(),
                        "password": "test123",
                        "role": "user"
                    },
                    headers={'Authorization': f'Bearer {self.admin_token}'},
                    catch_response=True) as response:
                    if response.status_code == 201:
                        response.success()
                    elif response.status_code == 400 and b'Username already exists' in response.content:
                        response.success()  # This is also an acceptable outcome
                    else:
                        response.failure(f"Registration failed: {response.text}")
        except Exception as e:
            logger.error(f"Error during admin tasks: {str(e)}") 