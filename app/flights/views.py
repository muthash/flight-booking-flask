from flask import Blueprint, request, jsonify
from flask.views import MethodView
from webargs.flaskparser import use_kwargs
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt_claims)

from app import db
from app.flights.models import Airport
from app.validators import (
    airport_args)
from app.helpers.query_helpers import (
    generate_response, save_airport)

flight = Blueprint('flight', __name__, url_prefix='/api')


class AiportManipulation(MethodView):
    """Class to manipulate the airport details"""
    @jwt_required
    @use_kwargs(airport_args, locations=("json",))
    def post(self, name, country, city):
        """POST method to enter a new airport details"""
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
        """return a list of all businesses else a single business"""
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


flight.add_url_rule('/airport', view_func=AiportManipulation.as_view('airport'))
