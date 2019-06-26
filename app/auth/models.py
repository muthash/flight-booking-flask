import datetime

from flask_bcrypt import Bcrypt
from app import db
from app.base_model import BaseModel


class User(BaseModel):
    """This class defines the users table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    name = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    passport = db.Column(db.String(256), default="1")
    registered_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    bookings = db.relationship('Booking', backref='user',
                               order_by='Booking.id',
                               cascade="all, delete-orphan", lazy=True)

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
