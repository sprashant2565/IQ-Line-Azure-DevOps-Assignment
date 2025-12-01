import unittest
from app import app # Import the Flask app instance

class UserServiceTestCase(unittest.TestCase):
    """Unit tests for the User Service endpoints."""

    def setUp(self):
        """Set up test environment."""
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check_success(self):
        """Test the /health endpoint returns 200 OK."""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Service', response.data)

    def test_get_user_details_content(self):
        """Test the /users/<id> endpoint returns expected data for a dummy ID."""
        user_id = '123'
        response = self.app.get(f'/users/{user_id}')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], user_id)
        self.assertIn('Alice Johnson', data['name'])

# To run this test locally: python -m unittest test_app.py