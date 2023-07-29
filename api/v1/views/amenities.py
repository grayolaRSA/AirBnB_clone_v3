#!/usr/bin/python3
"""Amenities blueprint page """
from . import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities",  methods=['GET'], strict_slashes=False)
def amenities():
    """returns list of all amenities"""
    d_amenities = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in d_amenities.values()])


@app_views.route("amenities/<amenity_id>",
                 methods=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    """returns a single amenity object data according to id"""
    amenities = storage.get("Amenity", amenity_id)
    if not amenities:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route("amenities/<amenity_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def amenity_del(amenity_id):
    """deletes an amenity object according to its id"""
    amenities = storage.get("Amenity", amenity_id)
    if not amenities:
        abort(404)
    else:
        state.delete()
        storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("amenities/<amenity_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """updates an amenity object according to its id"""
    amenities = storage.get("Amenity", amenity_id)
    if not amenities:
        abort(404)

    http_request = request.get_json()
    if not http_request:
        abort(400, "Not a JSON")

    for j, k in http_request.items():
        if j != 'id' and j != 'created_at' and j != 'updated_at':
            setattr(state, j, k)

    storage.save
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route("amenities/<amenity_id>",
                 methods=['POST'],
                 strict_slashes=False)
def amenity_post():
    """creates a new amenity object"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "Missing name")
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
