import models

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
trek = Blueprint('treks', 'trek')

@trek.route('/', methods=["GET"])
# @login_required
def get_all_treks():
    ## find the treks and change each one to a dictionary into a new array
    try:
        treks = [model_to_dict(trek) for trek in models.Trek.select()]
        return jsonify(data=treks, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@trek.route('/<id>', methods=["GET"])
def get_trek_detail(id):
    ## find the treks and change each one to a dictionary into a new array
    try:
        trek = [model_to_dict(trek) for trek in models.Trek.select().where(models.Trek.id==id)]
        return jsonify(data=trek, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@trek.route('/', methods=["POST"])
def create_treks():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    trek = models.Trek.create(**payload)
    ## see the object
    ## Look at all the methods
    # Change the model to a dict
    song_dict = model_to_dict(trek)
    return jsonify(data=song_dict, status={"code": 201, "message": "Success"})

@trek.route('/<id>', methods=["Delete"])
def delete_trek(id):
    query = models.Trek.delete().where(models.Trek.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

@trek.route('/<id>', methods=["PUT"])
def update_trek(id):
    payload = request.get_json()
    print(payload)
    query = models.Trek.update(**payload).where(models.Trek.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.Trek.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})
