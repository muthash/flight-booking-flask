import os

from flask import Blueprint, request, jsonify
from werkzeug import secure_filename
from flask.views import MethodView
from webargs.flaskparser import use_kwargs
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import ROOT_DIR, db
from app.validators import (
    user_args, login_args, passport_args, check_email, check_name,
    check_password, normalize_email)
from app.helpers.query_helpers import (
    generate_response, generate_token, search_email, save_user, get_user,
    save_image, delete_image)

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
            return generate_response('User already exists, Please login', 409)
        try:
            save_user(valid_email, name, password)
            return generate_response('Account created successfully', 201)
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 401


class LoginUser(MethodView):
    """Class to  login a user"""
    @use_kwargs(login_args, locations=("json",))
    def post(self, email, password):
        """Endpoint to login a user"""
        valid_email = normalize_email(email)
        try:
            user = search_email(valid_email)
            if user and user.password_is_valid(password):
                return generate_token('Login successfull', user)
            return generate_response('Invalid email or password' +
                                     ' Please try again', 401)
        except Exception as e:
            return jsonify({'message': str(e)}), 401


class Passport(MethodView):
    """Class to  upload, change and delete their passport photograph"""
    @jwt_required
    @use_kwargs(passport_args, locations=("files",))
    def put(self, passport_image):
        """Endpoint to upload passport photograph"""
        current_user = get_jwt_identity()
        filename = secure_filename(passport_image.filename)
        data = dict(passport=str(filename))
        try:
            user = get_user(current_user)
            if not user:
                return generate_response('Login to continue', 401)
            if user.passport:
                delete_image(user)
            user.update(user, **data)
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 401
        else:
            save_image(passport_image, filename)
            return generate_response('File uploaded successfully', 201)

    @jwt_required
    def delete(self):
        """Endpoint to delete passport photograph"""
        current_user = get_jwt_identity()
        data = dict(passport=None)
        try:
            user = get_user(current_user)
            if not user.passport:
                return generate_response('Cannot delete blank image file', 401)
            delete_image(user)
            user.update(user, **data)
            return generate_response('File deleted successfully', 200)
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 401


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))
auth.add_url_rule('/login', view_func=LoginUser.as_view('login'))
auth.add_url_rule('/uploads/passport', view_func=Passport.as_view('passport'),
                  methods=['PUT', 'DELETE'])
