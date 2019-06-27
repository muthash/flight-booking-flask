import datetime

from flask_bcrypt import Bcrypt
from app import db
from app.base_model import BaseModel
from app.bookings.models import Booking


class User(BaseModel):
    """This class defines the users table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    passport = db.Column(db.String, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    reservations = db.relationship('Booking', backref='owner', lazy=True)

    def __init__(self, email, name, password, is_admin=False, confirmed=False):
        """Initialize the user with the user details"""
        self.email = email
        self.name = name
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.registered_on = datetime.datetime.now()
        self.is_admin = is_admin
        self.confirmed = confirmed

    def password_is_valid(self, password):
        """Check the password against its hash"""
        return Bcrypt().check_password_hash(self.password, password)

    def __repr__(self):
        return 'user: {}'.format(self.name)
