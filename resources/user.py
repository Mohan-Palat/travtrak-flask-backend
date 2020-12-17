import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required, logout_user
from flask_httpauth import HTTPTokenAuth



# first argument is blueprints name
# second argument is it's import_name
user = Blueprint('users', 'user')
auth = HTTPTokenAuth(scheme='Bearer')

@user.route('/register', methods=["POST"])
def register():
    ## see request payload anagolous to req.body in express
    ## This is how you get the image you sent over
    ## This has all the data like username, email, password
    payload = request.get_json()

    payload['email'].lower()
    try:
        # Find if the user already exists?
        models.User.get(models.User.email == payload['email']) # model query finding by email
        return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password']) # bcrypt line for generating the hash
        user = models.User.create(**payload) # put the user in the database
        # **payload, is spreading like js (...) the properties of the payload object out

        #login_user
        login_user(user) # starts session

        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        # delete the password
        del user_dict['password'] # delete the password before we return it, because we don't need the client to be aware of it

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload, '< --- this is playload')
    try:
        user = models.User.get(models.User.email== payload['email']) ### Try find the user by thier email
        user_dict = model_to_dict(user) # if you find the User model convert in to a dictionary so you can access it
        if(check_password_hash(user_dict['password'], payload['password'])): # use bcyrpts check password to see if passwords match
            token = user.generate_auth_token().decode('utf-8')
            del user_dict['password'] # delete the password
            login_user(user) # setup the session
            print(user, ' this is user')
            return jsonify(data={"user": user_dict, "token": token}, status={"code": 200, "message": "Success"}) # respond to the client
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

@user.route("/logout")
# @login_required
def logout():
    logout_user()
    return 'you are logged out'

   # teaching tool -- route to show which user is logged in
# demonstrating how to use current_user
# this requires user_loader to be set up in app.py
@user.route('/logged_in', methods=['GET'])
def get_logged_in_user():
  # READ THIS https://flask-login.readthedocs.io/en/latest/#flask_login.current_user
  # because we called login_user and set up user_loader
  # print(current_user) # this is the logged in user
  # print(type(current_user)) # <class 'werkzeug.local.LocalProxy'> -- Google it if you're interested
  # user_dict = model_to_dict(current_user)
  # print(user_dict)
  # return jsonify(data=user_dict), 200 # should have been jsonify all along 
  # you can TELL WHETHER A USER IS LOGGED IN with current_user.is_authenticated 
  # (search current_user.is_authenticated in docs)
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