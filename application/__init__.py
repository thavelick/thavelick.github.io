"""Flask website for TristanHavelick.com."""

import os
from flask import Flask, render_template
from werkzeug.exceptions import NotFound
import click

from . import db
import markdown


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "blog.db"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route("/")
    def index():
        db_instance = db.get_db()
        articles = db_instance.execute(
            "SELECT p.id, p.slug, p.title "
            "FROM posts p "
            "JOIN post_categories pc ON p.id = pc.post_id "
            "JOIN categories c ON c.id = pc.category_id "
            "WHERE c.name = ? "
            "ORDER BY p.publish_date DESC LIMIT 5",
            ("blog",)
        ).fetchall()
        return render_template("index.html", title="Tristan Havelick", articles=articles)

    @app.route("/blog")
    def blog():
        db_instance = db.get_db()
        articles = db_instance.execute(
            "SELECT p.id, p.slug, p.title "
            "FROM posts p "
            "JOIN post_categories pc ON p.id = pc.post_id "
            "JOIN categories c ON c.id = pc.category_id "
            "WHERE c.name = ? "
            "ORDER BY p.publish_date DESC",
            ("blog",)
        ).fetchall()
        return render_template("blog.html", title="Tristan Havelick", articles=articles)

    @app.route("/<path:path>")
    def static_proxy(path):
        db_instance = db.get_db()
        post = db_instance.execute("SELECT * FROM posts WHERE slug = ?", (path,)).fetchone()
        if post:
            post = dict(post)
            from datetime import datetime
            try:
                dt = datetime.strptime(post["publish_date"], "%Y-%m-%d %H:%M:%S")
                post["publish_date"] = dt
            except Exception:
                pass
            if "markdown_content" in post:
                post["article_content"] = markdown.markdown(post["markdown_content"])
            return render_template("post.html", post=post)
        try:
            return app.send_static_file(path)
        except NotFound as e:
            new_path = os.path.join(path, "index.html")
            assert app.static_folder is not None
            full_path = os.path.join(app.static_folder, new_path)
            if os.path.exists(full_path):
                return app.send_static_file(new_path)
            raise NotFound() from e

    db.init_app(app)

    return app
