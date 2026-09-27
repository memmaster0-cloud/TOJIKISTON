"""Application factory for the ToDo API."""

from flask import Flask

from app.main import api


def create_app() -> Flask:
    """Create and configure a Flask application instance.

    Using the factory pattern makes the app easy to test: each test
    can build a fresh app/state instead of relying on module-level
    globals.
    """
    app = Flask(__name__)
    app.register_blueprint(api)
    return app
