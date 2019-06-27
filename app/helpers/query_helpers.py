import datetime

from flask import jsonify
from flask_jwt_extended import create_access_token

from app.auth.models import User


def generate_token(message, user, expires=datetime.timedelta(hours=1)):
    """Return access token and response to user"""
    response = {'message': message,
                'access_token': create_access_token(
                        identity=user.id, expires_delta=expires)}
    return jsonify(response), 200


def generate_response(message, status):
    """Return application/json object"""
    response = {'message': message}
    return jsonify(response), status


def search_email(email):
        return User.query.filter_by(email=email).first()


def save_user(email, name, password):
    user = User(email, name, password)
    user.save()

