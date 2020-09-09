#!/usr/bin/python3
"""This module defines the view State"""

from models.state import State
from . import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """Retrieves the list of all State objects

    Args:
        state_id (str, optional): id to search an state. Defaults to None.

    Returns:
        Response: If the state_id is not linked to any Amenity object,
            raise a 404 error or a list of all Amenity with response 200
    """
    list_ = []
    all_states = storage.all(State)
    if state_id:
        state = all_states.get("State." + state_id, None)
        return state.to_dict() if state else abort(404)
    else:
        for value in all_states.values():
            list_.append(value.to_dict())
        return jsonify(list_), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """Deletes a State object

    Args:
        state_id (str, optional): id of the state to be deleted.
            Defaults to None.

    Returns:
        HTTP-Response: If the state_id is not linked to any State object,
            raise a 404 error or Returns an empty dictionary
            with the status code 200
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(400)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def save_state():
    """[Creates a State]

    Returns:
        [HTTP-Response]: If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            If the dictionary doesn’t contain the key 'name',
            raise a 400 error with the message 'Missing name'
            Returns the new Amenity with the status code 201
    """
    body = request.get_json()
    if request.is_json:
        if "name" in body.keys():
            state = State(**body)
            state.save()
            return jsonify(state.to_dict()), 201
        else:
            return jsonify(error="Missing name"), 404
    return jsonify(error='Not a JSON'), 400


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    """Updates a Amenity object

    Args:
        state_id ([str], optional): Id of the State object to be updated.
            Defaults to None.

    Returns:
        [HTTP-Response]: If the state_id is not linked to any Amenity object,
            raise a 404 error
            If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            If everything is right
            returns the Amenity object with the status code 200
    """
    body = request.get_json()
    all_states = storage.all(State)
    state = all_states.get("State." + state_id, None)
    if state is None:
        abort(404)
    elif not request.is_json:
        return jsonify(error='Not a JSON'), 400

    for k, v in body.items():
        if k in ['id', 'updated_at', 'updated_at']:
            continue
        setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
