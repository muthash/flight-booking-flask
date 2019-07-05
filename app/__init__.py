""" The create_app function wraps the creation of a new Flask object, and
    returns it after it's loaded up with configuration settingsusing app.config
"""
import os
import atexit
import logging

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from instance.config import app_config

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app(config_name):
    """Function wraps the creation of a new Flask object, and returns it after it's
        loaded up with configuration settings
    """
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    db.app = app
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from app.auth.views import auth
    from app.flights.views import flight
    from app.bookings.views import booking
    from app.helpers.send_email import background_scheduler

    background_scheduler()

    @app.route('/')
    def index():
        return jsonify({"message":
                        ("Welcome to Flight Booking API, "
                         "This is a flask API that provides User Authentication, "
                         "Flight Search, Flight Booking and Email Notifications.")}), 200

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
