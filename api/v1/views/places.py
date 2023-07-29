#!/usr/bin/python3
"""Places blueprint page """
from . import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.city import City


@app_views.route("/cities/<city_id>/places",
                 methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """returns list of all places for each city"""
    d_places = storage.all(Place)
    return jsonify([obj.to_dict() for obj in d_places.values()])


@app_views.route("places/<place_id>",
                 methods=['GET'],
                 strict_slashes=False)
def place(place_id):
    """returns a place according to id"""
    places = storage.get("Place", place_id)
    if not places:
        abort(404)
    return jsonify(placeses.to_dict())


@app_views.route("places/<place_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def place_del(place_id):
    """deletes an place object"""
    places = storage.get("Place", place_id)
    if not places:
        abort(404)
    else:
        place.delete()
        storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("places/<place_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def place_put(place_id):
    """updates an place object according to its id"""
    places = storage.get("Place", place_id)
    if not places:
        abort(404)

    http_request = request.get_json()
    if not http_request:
        abort(400, "Not a JSON")

    for j, k in http_request.items():
        if j != 'id' and j != 'created_at' and j != 'updated_at':
            setattr(place, j, k)

    storage.save
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route("cities/<city_id>/places",
                 methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """creates a new place object"""
    new_place = request.get_json()
    if not city_id:
        abort(404)
    if not user_id:
        abort(404)
    if not new_place:
        abort(400, "Not a JSON")
    if "user_id" not in new_place:
        abort(400, "Missing user_id")
    if "name" not in new_place:
        abort(400, "Missing name")
    place = Place(**new_place)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)
