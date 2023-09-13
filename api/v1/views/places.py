#!/usr/bin/python3
"""Places blueprint page """
from . import app_views
from flask import jsonify, request, abort, make_response
from models.city import City
from models import storage
from models.place import Place
from models.user import User
from os import getenv


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
    return jsonify(places.to_dict())


@app_views.route("places/<place_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def place_del(place_id):
    """deletes an place object"""
    places = storage.get("Place", place_id)
    if not places:
        abort(404)
    else:
        places.delete()
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
            setattr(places, j, k)

    storage.save
    return make_response(jsonify(places.to_dict()), 200)


@app_views.route("cities/<city_id>/places",
                 methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """creates a new place object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    http_request = request.get_json()
    if not http_request:
        abort(400, "Not a JSON")

    user = storage.get("User", http_request["user_id"])
    if not user:
        abort(404)

    if "user_id" not in http_request:
        abort(400, "Missing user_id")

    if "name" not in http_request:
        abort(400, "Missing name")

    new_place = Place(city_id=city_id, **http_request)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/api/v1/places_search",
                 methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Search for places based on JSON request body"""
    request_data = request.get_json()

    if not request_data:
        abort(400, "Not a JSON")

    states = request_data.get('states', [])
    cities = request_data.get('cities', [])
    amenities = request_data.get('amenities', [])

    # Retrieve all places if all lists are empty or missing
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        # Gather places based on states and cities
        place_ids = set()

        # Include places for each State
        for state_id in states:
            state = storage.get("State", state_id)
            if state:
                for city in state.cities:
                    place_ids.update([place.id for place in city.places])

        # Include places for each City (unless already included by states)
        for city_id in cities:
            city = storage.get("City", city_id)
            if city:
                place_ids.update([place.id for place in city.places])

        places = [storage.get("Place", place_id) for place_id in
                  place_ids if storage.get("Place", place_id)]

    # Filter places based on amenities (exclusive filter)
    if amenities:
        filtered_places = []
        for place in places:
            if all(amenity_id in place.amenities_id for
                   amenity_id in amenities):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])
