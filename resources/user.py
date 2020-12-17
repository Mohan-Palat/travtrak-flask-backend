import models
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required, logout_user
from flask_httpauth import HTTPTokenAuth


user = Blueprint('users', 'user')
auth = HTTPTokenAuth(scheme='Bearer')

@user.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email']) 
        return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)
        login_user(user) 
        user_dict = model_to_dict(user)
        del user_dict['password']

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    try:
        user = models.User.get(models.User.email== payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            token = user.generate_auth_token().decode('utf-8')
            del user_dict['password']
            login_user(user) 
            return jsonify(data={"user": user_dict, "token": token}, status={"code": 200, "message": "Success"}) 
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

@user.route("/logout")
def logout():
    logout_user()
    return 'you are logged out'


@user.route('/logged_in', methods=['GET'])
def get_logged_in_user():
  if not current_user.is_authenticated:
    return jsonify(
        data={},
        message="No user is currently logged in",
        status=401
      ), 401
  else: # current user is logged in
    user_dict = model_to_dict(current_user)
    user_dict.pop('password')
    return jsonify(
        data=user_dict,
        message=f"Current user is {user_dict['email']}",
        status=200
      ), 200