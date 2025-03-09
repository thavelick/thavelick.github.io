import unittest
from application import create_app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "TESTING": True,
        })
        with self.app.app_context():
            from application import db
            con = db.get_db()
            # Clean up tables in case they exist
            con.execute("DELETE FROM post_categories")
            con.execute("DELETE FROM posts")
            con.execute("DELETE FROM categories")
            # Insert a test category 'blog'
            con.execute("INSERT INTO categories (name) VALUES (?)", ("blog",))
            category_row = con.execute("SELECT id FROM categories WHERE name = ?", ("blog",)).fetchone()
            category_id = category_row["id"]
            # Insert a test post with category 'blog'
            con.execute(
                "INSERT INTO posts (slug, title, markdown_content, publish_date) VALUES (?, ?, ?, ?)",
                ("test-post", "Test Post Title", "This is **test** content", "2025-03-09 12:00:00")
            )
            post_row = con.execute("SELECT id FROM posts WHERE slug = ?", ("test-post",)).fetchone()
            post_id = post_row["id"]
            con.execute("INSERT INTO post_categories (post_id, category_id) VALUES (?, ?)", (post_id, category_id))
            # Insert a test category 'recipe'
            con.execute("INSERT INTO categories (name) VALUES (?)", ("recipe",))
            recipe_category_row = con.execute("SELECT id FROM categories WHERE name = ?", ("recipe",)).fetchone()
            recipe_category_id = recipe_category_row["id"]
            # Insert a test post with category 'recipe'
            con.execute(
                "INSERT INTO posts (slug, title, markdown_content, publish_date) VALUES (?, ?, ?, ?)",
                ("test-recipe", "Test Recipe Title", "Recipe **content**", "2025-03-09 13:00:00")
            )
            recipe_post_row = con.execute("SELECT id FROM posts WHERE slug = ?", ("test-recipe",)).fetchone()
            recipe_post_id = recipe_post_row["id"]
            con.execute("INSERT INTO post_categories (post_id, category_id) VALUES (?, ?)", (recipe_post_id, recipe_category_id))
            con.commit()
        self.client = self.app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        # Check if the index page contains expected content such as "Newest Posts" or fallback text.
        self.assertTrue(b"Newest Posts" in response.data)
        self.assertTrue(b"Test Post Title" in response.data)

    def test_blog_route(self):
        response = self.client.get("/blog")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Test Post Title" in response.data)

    def test_recipes_route(self):
        response = self.client.get("/recipes")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Tristan Havelick - Recipes" in response.data)

if __name__ == '__main__':
    unittest.main()
