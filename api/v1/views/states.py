#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, Blueprint, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get states information for all states"""
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get state information by state_id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """delete a state based on its state_id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/',
                 methods=['POST'], strict_slashes=False)
def post_state():
    """create a new state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>',
                 methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """update a state by state_id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for attr, val in ['id', 'created_at', 'updated_at']:
        setattr(state, attr, val)
    state.save()
    return (jsonify(state.to_dict()), 200)
