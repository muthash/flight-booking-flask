from datetime import datetime

from flask import Blueprint, request, jsonify
from flask.views import MethodView
from webargs.flaskparser import use_kwargs
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt_claims)

from app import db
from app.helpers.query_helpers import (
    generate_response, save_booking, get_flight, filter_booking_by_flight)
from app.helpers.query_helpers import (
    generate_response)

booking = Blueprint('booking', __name__, url_prefix='/api')


class BookingManipulation(MethodView):
    """Class to manipulate the airport details"""
    @jwt_required
    def post(self, flight_id):
        """POST method to add a new flight booking"""
        data = request.get_json()
        seat = 1
        if data:
            seat = data.get('seat')
        current_user = get_jwt_identity()
        try:
            flight = get_flight(flight_id)
            if not flight:
                return generate_response('Selected flight not available', 400)

            if seat == 1 and flight.booked_economy < flight.airplane.economy_seats:
                data = dict(booked_economy=flight.booked_economy+1)
                save_booking(current_user, flight_id)
                flight.update(flight, **data)
                return generate_response('Economy seat flight reservation successfull', 201)

            if seat == 2 and flight.booked_business < flight.airplane.business_seats:
                data = dict(booked_business=flight.booked_business+1)
                save_booking(current_user, flight_id)
                flight.update(flight, **data)
                return generate_response('Business seat flight reservation successfull', 201)

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 401

    @jwt_required
    def get(self, flight_id):
        """Return a list of all reservations in a given day"""
        booking_date = request.args.get('bdate', datetime.now().strftime('%b %d %Y'), type=str)
        current_user = get_jwt_identity()
        try:
            flight = get_flight(flight_id)
            if not flight:
                return generate_response('Selected flight not available', 400)

            bookings_data = filter_booking_by_flight(flight_id)
            bookings = [booking.serialize() for booking in bookings_data
                        if booking.booking_date.strftime('%b %d %Y') == booking_date]
            response = {'booking_details': bookings,
                        'number_of_booking': len(bookings),
                        'message': "Data retrived successfully"}
            return jsonify(response), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 401


booking.add_url_rule('/booking/<int:flight_id>',
                     view_func=BookingManipulation.as_view('booking'),
                     methods=['GET', 'POST'])
