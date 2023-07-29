#!/usr/bin/python3
<<<<<<< HEAD
"""
View for States that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_all():
    """ returns list of all State objects """
    states_all = []
    states = storage.all("State").values()
    for state in states:
        states_all.append(state.to_json())
    return jsonify(states_all)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_get(state_id):
    """ handles GET method """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state = state.to_json()
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """ handles DELETE method """
    empty_dict = {}
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """ handles POST method """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    state = state.to_json()
    return jsonify(state), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """ handles PUT method """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            state.bm_update(key, value)
    state.save()
    state = state.to_json()
    return jsonify(state), 200
=======
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
def state_put():
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
>>>>>>> 2798b423504511b967c314be102d64295ffff516
