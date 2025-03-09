"""Application package."""
import os
from flask import Flask
from werkzeug.exceptions import NotFound

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'blog.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/', defaults={'path': 'index.html'})
    @app.route('/<path:path>')
    def static_proxy(path):
        try:
            return app.send_static_file(path)
        except NotFound as e:
            new_path = os.path.join(path, 'index.html')
            full_path = os.path.join(app.static_folder, new_path)
            if os.path.exists(full_path):
                return app.send_static_file(new_path)
            raise NotFound() from e

    # pylint: disable=import-outside-toplevel
    from . import db
    db.init_app(app)

    return app
