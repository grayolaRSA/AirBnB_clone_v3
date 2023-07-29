#!/usr/bin/python3
"""States blueprint page """
from . import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State


@app_views.route("/states",  methods=['GET'], strict_slashes=False)
def states():
    """returns list of all states"""
    d_states = storage.all(State)
    return jsonify([obj.to_dict() for obj in d_states.values()])


@app_views.route("states/<state_id>", methods=['GET'], strict_slashes=False)
def state(state_id):
    """returns a single state object data according to id"""
    state = storage.get("State", state_id)
    if not else:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("states/<state_id>", methods=['DELETE'], strict_slashes=False)
def state_del(state_id):
    """deletes a state object according to its id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    else:
        state.delete()
        storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("states/<state_id>", methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """updates a state object according to its id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    http_request = request.get_json()
    if not http_request:
        abort(400, "Not a JSON")

    for j, k in http_request.items():
        if j != 'id' and j != 'created_at' and j != 'updated_at':
            setattr(state, j, k)

    storage.save
    return make_response(jsonify(state.to_dict()), 200)
