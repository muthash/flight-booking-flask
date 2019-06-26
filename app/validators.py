import re

from flask import jsonify
from email_validator import validate_email, EmailNotValidError
from webargs import fields, validate


user_args = {
    "email": fields.Str(required=True, validate=validate.Email()),
    "password": fields.Str(required=True, validate=validate.Length(min=8)),
    "firstname": fields.Str(required=True, validate=validate.Length(min=2)),
    "othernames": fields.Str(required=True, validate=validate.Length(min=2)),
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
