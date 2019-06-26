""" The create_app function wraps the creation of a new Flask object, and
    returns it after it's loaded up with configuration settingsusing app.config
"""
from flask import Flask, jsonify


from instance.config import app_config

def create_app(config_name):
    """Function wraps the creation of a new Flask object, and returns it after it's
        loaded up with configuration settings
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])


    return app