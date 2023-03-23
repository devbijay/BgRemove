from flask import Flask
from routes.main import landing


def create_app():
    app = Flask(__name__)
    app.register_blueprint(landing)

    return app
