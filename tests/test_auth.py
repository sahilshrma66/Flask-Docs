import unittest
from app import create_app
from app.db import db
from app.models.models import User


class AuthAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test environment."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_success(self):
        """Test successful user registration."""
        response = self.client.post('/register', json={
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertIn("user", data)
        self.assertEqual(data["message"], "User registered successfully")
        self.assertEqual(data["user"]["username"], "testuser")

    def test_register_existing_user(self):
        """Test registration with an existing username."""
        # Register user once
        self.client.post('/register', json={
            "username": "testuser",
            "password": "password123"
        })
        # Try to register the same username
        response = self.client.post('/register', json={
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "User already exists.")

    def test_login_success(self):
        """Test successful login."""
        # Register a user
        self.client.post('/register', json={
            "username": "testuser",
            "password": "password123"
        })
        # Login with the registered user
        response = self.client.post('/login', json={
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("token", data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        # Register a user
        self.client.post('/register', json={
            "username": "testuser",
            "password": "password123"
        })
        # Attempt to login with incorrect password
        response = self.client.post('/login', json={
            "username": "testuser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid credentials.")

    def test_login_nonexistent_user(self):
        """Test login with a username that does not exist."""
        response = self.client.post('/login', json={
            "username": "nonexistent",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid credentials.")

    def test_register_missing_fields(self):
        """Test registration with missing fields."""
        response = self.client.post('/register', json={
            "username": "testuser"
            # Missing "password"
        })
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)

    def test_login_missing_fields(self):
        """Test login with missing fields."""
        response = self.client.post('/login', json={
            "username": "testuser"
            # Missing "password"
        })
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
