"""Flask website for TristanHavelick.com."""

import os
from flask import Flask, render_template, request, redirect
from werkzeug.exceptions import NotFound

from . import db
from .models import Post
import markdown
from datetime import datetime


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
        posts = Post.fetch_by_category("blog", 5)
        return render_template("index.html", title="Tristan Havelick", posts=posts)

    @app.route("/blog")
    def blog():
        posts = Post.fetch_by_category("blog")
        return render_template("blog.html", title="Tristan Havelick", posts=posts)

    @app.route("/recipes")
    def recipes():
        posts = Post.fetch_by_category("recipe")
        return render_template(
            "recipes.html", title="Tristan Havelick - Recipes", posts=posts
        )

    @app.route("/rss.xml")
    def rss():
        posts = Post.fetch_by_category("blog")
        posts_list = []
        for post in posts:
            post_dict = dict(post)
            dt = datetime.strptime(post_dict["publish_date"], "%Y-%m-%d %H:%M:%S")
            post_dict["publish_date"] = dt.strftime("%a, %d %b %Y %H:%M:%S")
            if "markdown_content" in post_dict:
                post_dict["article_content"] = markdown.markdown(
                    post_dict["markdown_content"]
                )
            posts_list.append(post_dict)
        return (
            render_template("rss.xml", posts=posts_list),
            200,
            {"Content-Type": "application/xml"},
        )

    @app.route("/<path:path>")
    def catchall(path):
        if not request.path.endswith("/"):
            full_dir = os.path.join(app.static_folder, path)
            if os.path.isdir(full_dir):
                return redirect(request.path + "/", code=302)
        post = Post.fetch_by_slug(path)
        if post:
            post = dict(post)
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

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    db.init_app(app)

    return app
