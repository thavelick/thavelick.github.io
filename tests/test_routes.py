import unittest
from application import create_app
from application import db


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        import tempfile

        _, db_path = tempfile.mkstemp()
        self.app = create_app(
            {
                "TESTING": True,
                "DATABASE": db_path,
            }
        )
        with self.app.app_context():

            db.init_db()
            con = db.get_db()
            with open("tests/data.sql", "r", encoding="utf-8") as f:
                con.executescript(f.read())
        self.client = self.app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Newest Posts" in response.data)
        self.assertTrue(b"Test Post Title" in response.data)

    def test_blog_route(self):
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Test Post Title" in response.data)

    def test_recipes_route(self):
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Tristan Havelick - Recipes" in response.data)
        self.assertTrue(b"Test Recipe Title" in response.data)

    def test_rss_route(self):
        response = self.client.get("/rss.xml")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "xml")

        # Validate channel information
        channel = soup.find("channel")
        self.assertIsNotNone(channel)
        self.assertEqual(channel.find("title").text, "TristanHavelick.com")
        self.assertEqual(channel.find("description").text, "Tristan Havelick's Blog")
        self.assertEqual(channel.find("link").text, "https://tristanhavelick.com")
        self.assertIsNotNone(channel.find("pubDate"))

        # Validate items in known order (ordered by publish_date descending)
        items = soup.find_all("item")
        self.assertEqual(len(items), 2)

        # First item should be the recipe post (published at 13:00:00)
        item0 = items[0]
        self.assertEqual(item0.find("title").text, "Test Recipe Title")
        self.assertEqual(
            item0.find("link").text, "https://tristanhavelick.com/recipes/test-recipe/"
        )
        self.assertEqual([cat.text for cat in item0.find_all("category")], ["recipe"])

        # Second item should be the blog post (published at 12:00:00)
        item1 = items[1]
        self.assertEqual(item1.find("title").text, "Test Post Title")
        self.assertEqual(
            item1.find("link").text, "https://tristanhavelick.com/test-post/"
        )
        self.assertEqual([cat.text for cat in item1.find_all("category")], ["blog"])

    def test_catchall_route(self):
        response = self.client.get("/test-post")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Test Post Title" in response.data)

    def test_catchall_static(self):
        response = self.client.get("/archive/chaos-of-the-mind/index.htm")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Woohoo!", response.data)

    def test_catchall_static_automatic_index(self):
        response = self.client.get("/games/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Games", response.data)

    def test_catchall_nonexistent(self):
        response = self.client.get("/nonexistentpage")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
