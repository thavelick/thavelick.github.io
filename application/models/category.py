from .. import db

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
