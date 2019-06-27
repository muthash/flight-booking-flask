import datetime

from app import db
from app.base_model import BaseModel
from app.flights.models import Flight


class Booking(BaseModel):
    """This class defines the bookings table"""

    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'),
                          nullable=False)
    emails = db.relationship('EmailSchedule', backref='booking', lazy=True)

    def __init__(self, user_id, flight_id):
        """Initialize the booking with the reservation details"""
        self.booking_date = datetime.datetime.now()
        self.user_id = user_id
        self.flight_id = flight_id

    def __repr__(self):
        return 'bookings: {}'.format(self.id)


class EmailSchedule(BaseModel):
    """This class defines the emails to be sent table"""

    __tablename__ = 'email_schedules'

    id = db.Column(db.Integer, primary_key=True)
    send_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(120), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'),
                           nullable=False)

    def __init__(self, send_date, booking_id, status='pending'):
        """Initialize with the emails to be sent details"""
        self.send_date = send_date
        self.booking_id = booking_id
        self.status = status

    def __repr__(self):
        return 'emails: {}'.format(self.id)
