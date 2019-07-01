""" The create_app function wraps the creation of a new Flask object, and
    returns it after it's loaded up with configuration settingsusing app.config
"""
import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


from instance.config import app_config

db = SQLAlchemy()
jwt = JWTManager()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app(config_name):
    """Function wraps the creation of a new Flask object, and returns it after it's
        loaded up with configuration settings
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    jwt.init_app(app)

    from app.auth.views import auth
    from app.flights.views import flight
    from app.bookings.views import booking

    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code

    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {'roles': user.is_admin}

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    app.register_blueprint(auth)
    app.register_blueprint(flight)
    app.register_blueprint(booking)

    return app
