#!/usr/bin/python3
"""Amenities blueprint page """
from . import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities",  methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """returns list of all amenities, or creates a new one"""
    if request.method == 'GET':
        d_amenities = storage.all(Amenity)
        return jsonify([obj.to_dict() for obj in d_amenities.values()])
    elif request.method == 'POST':
        new_amenity = request.get_json()
        if not new_amenity:
            abort(400, "Not a JSON")
        if "name" not in new_amenity:
            abort(400, "Missing name")
        amenity = Amenity(**new_amenity)
        storage.new(amenity)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("amenities/<amenity_id>",
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def amenity(amenity_id):
    """returns, updates or deletes amenity according to id"""
    amenities = storage.get("Amenity", amenity_id)
    if not amenities:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenities.to_dict())

    elif request.method == 'DELETE':
        amenities.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        http_request = request.get_json()
        if not http_request:
            abort(400, "Not a JSON")

        for j, k in http_request.items():
            if j != 'id' and j != 'created_at' and j != 'updated_at':
                setattr(amenities, j, k)
        storage.save()
        return make_response(jsonify(amenities.to_dict()), 200)
