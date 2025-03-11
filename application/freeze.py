from flask_frozen import Freezer
from application import create_app
from application.models import Post

app = create_app()
freezer = Freezer(app)


@freezer.register_generator
def catchall():
    for post in Post.fetch_all():
        yield {"path": post["slug"]}
    
    import os
    archive_dir = os.path.join("application", "static", "archive")
    for root, dirs, files in os.walk(archive_dir):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), "application/static")
            yield {"path": relative_path}

if __name__ == "__main__":
    freezer.freeze()
