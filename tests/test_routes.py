import unittest
from application import create_app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "TESTING": True,
        })
        self.client = self.app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        # Check if the index page contains expected content such as "Newest Posts" or fallback text.
        self.assertTrue(b"Newest Posts" in response.data or b"No posts found." in response.data)

if __name__ == '__main__':
    unittest.main()
