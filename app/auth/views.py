from flask import Blueprint, request, jsonify
from flask.views import MethodView
from webargs.flaskparser import use_kwargs
from email_validator import validate_email, EmailNotValidError

from app.validators import user_args, check_email, check_name, check_password
from app.helpers.query_helpers import search_email, save_user

auth = Blueprint('auth', __name__, url_prefix='/api')


class RegisterUser(MethodView):
    """Class to Register a new user"""
    @use_kwargs(user_args, locations=("json",))
    def post(self, email, password, name):
        """POST method to register a user"""
        if not isinstance(check_email(email), str):
            return check_email(email)
        if check_name(name):
            return check_name(name)
        if check_password(password):
            return check_password(password)

        valid_email = check_email(email)
        if search_email(valid_email):
            response = {'message': 'User already exists, Please login'}
            return jsonify(response), 409
        try:
            save_user(valid_email, name, password)
            return jsonify({'message': 'Account created successfully, ' +
                            'A confirmation email has been sent.'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 401


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))
