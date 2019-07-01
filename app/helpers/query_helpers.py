import os
import datetime

from flask import jsonify
from flask_jwt_extended import create_access_token

from app import ROOT_DIR
from app.auth.models import User
from app.flights.models import Airport


def generate_token(message, user, expires=datetime.timedelta(hours=1)):
    """Return access token and response to user"""
    response = {'message': message,
                'access_token': create_access_token(
                        identity=user, expires_delta=expires)}
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


def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


def save_image(image, filename):
    image.save(os.path.join(ROOT_DIR, 'images', filename))


def delete_image(user):
    try:
        os.remove(os.path.join(ROOT_DIR, 'images', user.passport))
    except Exception as e:
        print("Deleting " + user.passport + "failed because of " + str(e))


def save_airport(name, country, city):
    airport = Airport(name, country, city)
    airport.save()
