from flask import Blueprint, request, jsonify
from flask.views import MethodView
from webargs.flaskparser import use_kwargs
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt_claims)

from app import db
from app.flights.models import Airport, Airplane, Flight
from app.validators import (
    airport_args, airplane_args, flight_args)
from app.helpers.query_helpers import (
    generate_response, save_airport, save_airplane, save_flight)

flight = Blueprint('flight', __name__, url_prefix='/api')


class AirportManipulation(MethodView):
    """Class to manipulate the airport details"""
    @jwt_required
    @use_kwargs(airport_args, locations=("json",))
    def post(self, name, country, city):
        """POST method to add a new airport details"""
        current_roles = get_jwt_claims()['roles']
        if not current_roles:
            return generate_response("Forbidden, Admins only!", 403)
        try:
            save_airport(name.upper(), country.upper(), city.upper())
            return generate_response('Airport registered successfully', 201)
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 401

    @jwt_required
    def get(self):
        """return a list of all airports"""
        try:
            airports_data = Airport.get_all()
            if not airports_data:
                return generate_response('No data to display', 200)

            airports = [airport.serialize() for airport in airports_data]
            response = {'airports': airports,
                        'number_of_airports': len(airports),
                        'message': "Data retrived successfully"}
            return jsonify(response), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 401


class AirplaneManipulation(MethodView):
    """Class to manipulate the airport details"""
    @jwt_required
    @use_kwargs(airplane_args, locations=("json",))
    def post(self, reg_number, economy_seats, business_seats,
             first_class_seats):
        """POST method to add a new airplane details"""
        current_roles = get_jwt_claims()['roles']
        if not current_roles:
            return generate_response("Forbidden, Admins only!", 403)
        try:
            save_airplane(reg_number.upper(), economy_seats, business_seats,
                          first_class_seats)
            return generate_response('Airplane registered successfully', 201)
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 401

    @jwt_required
    def get(self):
        """return a list of all airplanes"""
        try:
            airplanes_data = Airplane.get_all()
            if not airplanes_data:
                return generate_response('No data to display', 200)

            airplanes = [airplane.serialize() for airplane in airplanes_data]
            response = {'airplanes': airplanes,
                        'number_of_airplanes': len(airplanes),
                        'message': "Data retrived successfully"}
            return jsonify(response), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 401


class FlightManipulation(MethodView):
    """Class to manipulate the flight details"""
    @jwt_required
    @use_kwargs(flight_args, locations=("json",))
    def post(self, departure_date, departure_airport_id, arrival_date,
             arrival_airport_id, airplane_id):
        """POST method to add a new flight schedule"""
        current_roles = get_jwt_claims()['roles']
        if not current_roles:
            return generate_response("Forbidden, Admins only!", 403)
        try:
            save_flight(departure_date, departure_airport_id, arrival_date,
                        arrival_airport_id, airplane_id)
            return generate_response('Flight schedule added successfully', 201)
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 401

    @jwt_required
    def get(self):
        """Return a list of all flights"""
        try:
            flights_data = Flight.get_all()
            if not flights_data:
                return generate_response('No data to display', 200)

            flights = [flight.serialize() for flight in flights_data]
            response = {'flights': flights,
                        'message': "Data retrived successfully"}
            return jsonify(response), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 401


flight.add_url_rule('/airport', view_func=AirportManipulation.as_view('airport'))
flight.add_url_rule('/airplane', view_func=AirplaneManipulation.as_view('airplane'))
flight.add_url_rule('/flight', view_func=FlightManipulation.as_view('flight'))
