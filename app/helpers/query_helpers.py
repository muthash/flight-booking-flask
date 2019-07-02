import os
import datetime

from flask import jsonify
from flask_jwt_extended import create_access_token

from app import ROOT_DIR, db
from app.auth.models import User
from app.flights.models import Airport, Airplane, Flight
from app.bookings.models import Booking


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


def save_airplane(reg_number, economy, business, first_class):
    airplane = Airplane(reg_number, economy, business, first_class)
    airplane.save()


def save_flight(reg_number, economy_seats, business_seats,
                first_class_seats, airplane_id):
    flight = Flight(reg_number, economy_seats, business_seats,
                    first_class_seats, airplane_id)
    flight.save()


def save_booking(user_id, flight_id):
    booking = Booking(user_id, flight_id)
    booking.save()


def get_flight(flight_id):
    return Flight.query.filter_by(id=flight_id).first()


def filter_booking_by_flight(flight_id):
    return Booking.query.filter_by(flight_id=flight_id).all()


def get_tomorrow_flights():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    with db.app.app_context():
        return Flight.query.filter_by(departure_date=tomorrow).all()
