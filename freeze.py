from flask_frozen import Freezer
from application import create_app
from apllication.models import Post

app = create_app()
freezer = Freezer(app)


@freezer.register_generator
def catchall():
    for post in Post.fetch_all():
        yield {"path": post.slug}


if __name__ == "__main__":
    freezer.freeze()
