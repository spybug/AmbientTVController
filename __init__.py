from flask import *
import os


def create_app():
    app = Flask(__name__)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/setup')
    def setup():
        return '<p>Hello World</p>'

    return app
