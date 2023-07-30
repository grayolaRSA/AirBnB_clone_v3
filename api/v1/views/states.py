#!/usr/bin/python3
"""States blueprint page """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State


@app_views.route("/states",  methods=['GET', 'POST'], strict_slashes=False)
def states():
    """returns list of all states or creates a new state"""
    if request.method == 'GET':
        d_states = storage.all(State)
        return jsonify([obj.to_dict() for obj in d_states.values()])
    elif request.method == 'POST':
        new_state = request.get_json()
        if not new_state:
            abort(400, "Not a JSON")
        if "name" not in new_state:
            abort(400, "Missing name")
        state = State(**new_state)
        storage.new(state)
        storage.save()
        return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>",
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def state(state_id):
    """returns, updates, or deletes
    a single state object data according to id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    elif request.method == 'PUT':
        http_request = request.get_json()
        if not http_request:
            abort(400, "Not a JSON")

        for j, k in http_request.items():
            if j != 'id' and j != 'created_at' and j != 'updated_at':
                setattr(state, j, k)

        storage.save()
        return make_response(jsonify(state.to_dict()), 200)

    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)
