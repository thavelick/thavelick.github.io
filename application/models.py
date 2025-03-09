from . import db


class Post:
    @classmethod
    def fetch_by_category(cls, category, limit=None):
        db_instance = db.get_db()
        query = (
            "SELECT p.* "
            "FROM posts p "
            "JOIN post_categories pc ON p.id = pc.post_id "
            "JOIN categories c ON c.id = pc.category_id "
            "WHERE c.name = ? "
            "ORDER BY p.publish_date DESC"
        )
        params = [category]
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)
        return db_instance.execute(query, tuple(params)).fetchall()

    @classmethod
    def fetch_by_slug(cls, slug):
        db_instance = db.get_db()
        return db_instance.execute(
            "SELECT * FROM posts WHERE slug = ?", (slug,)
        ).fetchone()

    @classmethod
    def fetch_all(cls):
        db_instance = db.get_db()
        return db_instance.execute("SELECT * FROM posts ORDER BY publish_date DESC").fetchall()

class Category:
    @classmethod
    def fetch_by_post_id(cls, post_id):
        db_instance = db.get_db()
        rows = db_instance.execute(
            "SELECT c.name FROM post_categories pc JOIN categories c ON c.id = pc.category_id WHERE pc.post_id = ?",
            (post_id,)
        ).fetchall()
        if rows:
            return [row["name"] for row in rows]
        return []
