import datetime

from app import db
from app.base_model import BaseModel


class Airport(BaseModel):
    """This class defines the airports table"""

    __tablename__ = 'airports'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    country = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(256), nullable=False)
    flights = db.relationship('Flight', backref='airport', lazy=True)

    def __init__(self, name, country, city):
        """Initialize the airport with the airport details"""
        self.name = name
        self.country = country
        self.city = city

    def serialize(self):
        """Return a dictionary"""
        return {
            'airport_id': self.id,
            'airport_name': self.name,
            'country': self.country,
            'city': self.city
        }

    @staticmethod
    def get_all():
        return Airport.query.all()

    def __repr__(self):
        return 'airports: {}'.format(self.name)


class Airplane(BaseModel):
    """This class defines the airplanes table"""

    __tablename__ = 'airplanes'

    id = db.Column(db.Integer, primary_key=True)
    reg_number = db.Column(db.String, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    economy_seats = db.Column(db.Integer, nullable=False)
    business_seats = db.Column(db.Integer, nullable=False)
    flights = db.relationship('Flight', backref='airplane', lazy=True)

    def __init__(self, reg_number, economy_seats, business_seats,
                 first_class_seats):
        """Initialize the airplane details"""
        self.reg_number = reg_number
        self.total_seats = economy_seats + business_seats
        self.economy_seats = economy_seats
        self.business_seats = business_seats
        self.first_class_seats = first_class_seats

    def serialize(self):
        """Return a dictionary"""
        return {
            'airplane_id': self.id,
            'reg_number': self.reg_number,
            'business_seats': self.business_seats,
            'economy_seats': self.economy_seats,
            'total_seats': self.total_seats
        }

    @staticmethod
    def get_all():
        return Airplane.query.all()

    def __repr__(self):
        return 'Airplane: {}'.format(self.reg_number)


class Flight(BaseModel):
    """This class defines the flight schedules table"""

    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    departure_date = db.Column(db.DateTime, nullable=False)
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'),
                                     nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=False)
    arrival_airport_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(256), default='upcoming')
    airplane_id = db.Column(db.Integer, db.ForeignKey('airplanes.id'),
                            nullable=False)
    booked_business = db.Column(db.Integer, default=0)
    booked_economy = db.Column(db.Integer, default=0)
    bookings = db.relationship('Booking', backref='flight', lazy=True)

    def __init__(self, departure_date, departure_airport_id, arrival_date,
                 arrival_airport_id, airplane_id):
        """Initialize the flight details"""
        self.departure_date = departure_date
        self.departure_airport_id = departure_airport_id
        self.arrival_date = arrival_date
        self.arrival_airport_id = arrival_airport_id
        self.airplane_id = airplane_id

    def get_arrival_airport(self):
        return Airport.query.filter_by(id=self.arrival_airport_id).first()

    def serialize(self):
        """Return a dictionary"""
        self.arrival_airport = self.get_arrival_airport()
        return {
            'flight_id': self.id,
            'departure_date': self.departure_date,
            'departure_airport': self.airport.name,
            'departure_city': self.airport.city,
            'arrival_date': self.arrival_date,
            'arrival_airport': self.arrival_airport.name,
            'arrival_city': self.arrival_airport.city,
            'flight_status': self.status
        }

    @staticmethod
    def get_all():
        return Flight.query.all()

    def __repr__(self):
        return 'Flight: {}'.format(self.id)
