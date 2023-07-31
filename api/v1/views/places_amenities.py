#!/usr/bin/python3
"""Place-Amenity blueprint page """
from . import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("places/<place_id>/amenities",
                 methods=['GET'],
                 strict_slashes=False)
def place(place_id):
    """returns a place's amenities according to id"""
    place = storage.get("Place", place_id)
    if not places:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        a = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(a)
    else:
        a = storage.get("Amenity", amenity_id).to_dict()
        return jsonify(a)


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def place_amenity_del(place_id, amenity_id):
    """deletes an amenity object to a place"""
    place = storage.get("Place", place_id)
    if not places:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            indice = place.amenity_ids.indice(amenity_id)
            place.amenity_ids.pop(indice)

    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=['POST'],
                 strict_slashes=False)
def place_amenity_post(place_id, amenity_id):
    """creates a new amenity for a place object"""
    place = storage.get("City", city_id)
    if not place:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
