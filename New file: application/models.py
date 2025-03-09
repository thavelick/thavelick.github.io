from . import db

class Post:
    @classmethod
    def fetch_by_category(cls, category, limit=None):
        db_instance = db.get_db()
        query = (
            "SELECT p.id, p.slug, p.title "
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
