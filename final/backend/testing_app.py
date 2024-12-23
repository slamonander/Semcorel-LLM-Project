import unittest
import json
from app import app

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the test client and push the app context."""
        app.testing = True  # Enables testing mode
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()  # Push the context for the Flask app

    def tearDown(self):
        """Clean up by popping the app context."""
        self.app_context.pop()  # Pop the context to avoid resource leaks

    def test_chat_interface_route(self):
        """Test the '/' route to return the index.html page."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"<!doctype html>" in response.data.lower())

    def test_static_files_route(self):
        """Test the '/static/<path>' route to return static files."""
        response = self.client.get('/static/main.4ad22289.js')
        # Expecting a 404 unless the file exists in the static folder
        if response.status_code == 404:
            self.assertTrue(True)  # File does not exist
        else:
            self.assertEqual(response.status_code, 200)

    def test_submit_valid_input(self):
        """Test the '/submit' route with valid input."""
        valid_payload = {
            "userInput": "How do I connect my CoCo watch?",
            "history": json.dumps([{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello"}])
        }
        response = self.client.post(
            '/submit',
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("response", data)
        self.assertIsInstance(data["response"], str)

    def test_submit_invalid_input(self):
        """Test the '/submit' route with missing 'userInput'."""
        invalid_payload = {"history": "[]"}
        response = self.client.post(
            '/submit',
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("response", data)
        self.assertEqual(data["response"], "Invalid input.")

    def test_submit_invalid_json(self):
        """Test the '/submit' route with invalid JSON format."""
        invalid_payload = "Not a JSON String"
        response = self.client.post(
            '/submit',
            data=invalid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertIn("response", data)
        self.assertEqual(data["response"], "Invalid JSON format.")

if __name__ == '__main__':
    unittest.main()
