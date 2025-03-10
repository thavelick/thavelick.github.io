from flask_frozen import Freezer
from application import create_app

app = create_app()
freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
