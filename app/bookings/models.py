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
    email_status = db.Column(db.String(120), nullable=False, default='pending')

    def __init__(self, user_id, flight_id, status='pending'):
        """Initialize the booking with the reservation details"""
        self.booking_date = datetime.datetime.now()
        self.user_id = user_id
        self.flight_id = flight_id
        self.email_status = status

    def serialize(self):
        """Return a dictionary"""
        return {
            "booking_date": self.booking_date,
            "booked_by": self.owner.name,
            "email_status": self.email_status
        }

    def __repr__(self):
        return 'bookings: {}'.format(self.id)
