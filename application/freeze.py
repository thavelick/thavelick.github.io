from flask_frozen import Freezer
from application import create_app
from application.models import Post

app = create_app()
freezer = Freezer(app)


@freezer.register_generator
def catchall():
    for post in Post.fetch_all():
        yield {"path": post["slug"]}

    # ai! Let's add a loop to iterate over the files in application/static/archive and yeild the relative paths


if __name__ == "__main__":
    freezer.freeze()
