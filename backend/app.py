"""Application factory that sets up Flask and Dash."""

from flask import Flask

from frontend.dash_app import create_dash

from .database import init_db
from .routes import api_bp
from . import models
from . import sample_data


def create_app():
    """Create Flask app with Dash attached."""
    init_db()  # Ensure tables exist
    sample_data.seed()  # WHY: provide sample records for testing auth
    server = Flask(__name__)
    server.register_blueprint(api_bp, url_prefix="/api")

    # Attach Dash frontend to this server
    create_dash(server)

    return server

