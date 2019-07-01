import re

from flask import jsonify
from email_validator import validate_email, EmailNotValidError
from webargs import fields, validate
from usernames import is_safe_username


user_args = {
    "email": fields.Str(required=True, validate=validate.Email()),
    "password": fields.Str(required=True, validate=validate.Length(min=8)),
    "name": fields.Str(required=True, validate=validate.Length(min=2)),
}

login_args = {
    "email": fields.Str(required=True, validate=validate.Email()),
    "password": fields.Str(required=True),
}

passport_args = {
    "passport_image": fields.Field(
        required=True,
        validate=lambda f: f.mimetype in ["image/jpeg", "image/jpg",
                                          "image/png"]),
}

airport_args = {
    "name": fields.Str(required=True, validate=validate.Length(min=3)),
    "country": fields.Str(required=True, validate=validate.Length(min=3)),
    "city": fields.Str(required=True, validate=validate.Length(min=3)),
}


airplane_args = {
    "reg_number": fields.Str(required=True, validate=validate.Length(min=3)),
    "economy_seats": fields.Int(required=True, validate=lambda val: val > 0),
    "business_seats": fields.Int(required=True, validate=lambda val: val >= 0),
    "first_class_seats": fields.Int(required=True, validate=lambda val: val >= 0),
}


flight_args = {
    "departure_date": fields.Str(required=True),
    "departure_airport_id": fields.Int(required=True, validate=lambda val: val > 0),
    "arrival_date": fields.Str(required=True),
    "arrival_airport_id": fields.Int(required=True, validate=lambda val: val > 0),
    "airplane_id": fields.Int(required=True, validate=lambda val: val > 0),
}


def check_email(email):
    """Check for a valid email address and
       lowercase the domain part of the email
    """
    try:
        v_email = validate_email(email)
        email = v_email["email"]
        return email
    except EmailNotValidError as error:
        response = {'message': str(error)}
        return jsonify(response), 400


def check_name(name):
    regex = re.compile('^[a-zA-Z]{3,}$')
    res = re.match(regex, str(name))
    if not res:
        response = {'message': "The name should only contain letters."}
        return jsonify(response), 400
    if not is_safe_username(name):
        response = {'message': "The name you provided is not allowed, " +
                               "please try again but with a different name."}
        return jsonify(response), 400


def check_password(password):
    if not re.match(r'[a-zA-Z_]+[A-Za-z0-9@#!$%^&+=]{8,}', str(password)):
        response = {'message': 'Password should contain at least eight ' +
                    'characters with at least one digit, one ' +
                    'uppercase letter and one lowercase letter.'}
        return jsonify(response), 400


def normalize_email(email):
    """Lowercase the domain part of the email"""
    email_part = email.split('@')
    domain = email_part[1].lower()
    email = email_part[0]+'@'+domain
    return email
