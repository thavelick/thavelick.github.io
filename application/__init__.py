"""Flask website for TristanHavelick.com."""

import os
from flask import Flask, render_template
from werkzeug.exceptions import NotFound

from . import db
from .models import Post, Category
from .markdown_utils import render_markdown
import mimetypes
from datetime import datetime


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config["FREEZER_DESTINATION"] = "../public_html"
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
        posts = Post.fetch_by_category("blog", 5)
        return render_template("index.html", title="Tristan Havelick", posts=posts)

    @app.route("/blog/")
    def blog():
        posts = Post.fetch_by_category("blog")
        posts_by_year = {}
        for post in posts:
            year = post["publish_date"][:4]
            posts_by_year.setdefault(year, []).append(post)
        return render_template("blog.html", title="Tristan Havelick", posts_by_year=posts_by_year)

    @app.route("/blogroll/")
    def blogroll():
        return render_template("blogroll.html", title="Tristan Havelick -- Blogroll")

    @app.route("/recipes/")
    def recipes():
        posts = Post.fetch_by_category("recipe")
        return render_template(
            "recipes.html", title="Tristan Havelick - Recipes", posts=posts
        )

    @app.route("/books/")
    def books():
        return render_template("books.html", title="Tristan Havelick -- Books")

    @app.route("/archive/")
    def archive():
        return render_template("archive.html", title="Tristan Havelick -- Archive")

    @app.route("/games/")
    def games():
        return render_template("games.html", title="Tristan Havelick -- Games")

    @app.route("/rss.xml")
    def rss():
        posts = Post.fetch_all()
        posts_list = []
        for post in posts:
            post_dict = dict(post)
            dt = datetime.strptime(post_dict["publish_date"], "%Y-%m-%d %H:%M:%S")
            post_dict["publish_date"] = dt.strftime("%a, %d %b %Y %H:%M:%S")
            if "markdown_content" in post_dict:
                post_dict["article_content"] = render_markdown(
                    post_dict["markdown_content"]
                )
            post_dict["categories"] = Category.fetch_by_post_id(post_dict["id"])
            posts_list.append(post_dict)
        if posts_list:
            feed_pub_date = posts_list[0]["publish_date"]
        else:
            feed_pub_date = ""
        return (
            render_template("rss.xml", posts=posts_list, feed_pub_date=feed_pub_date),
            200,
            {"Content-Type": "text/xml"},
        )

    @app.route("/404.html")
    def page_not_found_static():
        return render_template("404.html")

    @app.route("/<path:path>")
    def catchall(path):
        path_without_trailing_slash = path.rstrip("/")
        post = Post.fetch_by_slug(path_without_trailing_slash)
        if post:
            post = dict(post)
            dt = datetime.strptime(post["publish_date"], "%Y-%m-%d %H:%M:%S")
            post["publish_date"] = dt
            if "markdown_content" in post:
                post["article_content"] = render_markdown(post["markdown_content"])
            return (
                render_template("post.html", post=post),
                200,
                {"Content-Type": "text/html; charset=utf-8"},
            )
        assert app.static_folder
        static_file_path = os.path.join(app.static_folder, path)
        if os.path.exists(static_file_path):
            with open(static_file_path, "rb") as f:
                content = f.read()
            content_type, _ = mimetypes.guess_type(static_file_path)
            if content_type is None:
                content_type = (
                    "text/html; charset=utf-8"
                    if path.endswith(".html") or path.endswith(".htm")
                    else "application/octet-stream"
                )
            return content, 200, {"Content-Type": content_type}
        raise NotFound()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    db.init_app(app)

    return app
