#!/usr/bin/python3
"""This module defines the view User"""

from models.user import User
from . import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """Retrieves the list of all Users objects

    Args:
        user_id (str, optional): id to search an user. Defaults to None.

    Returns:
        Response: If the user_id is not linked to any User object,
            raise a 404 error or a list of all User with response 200
    """

    list_ = []
    all_users = storage.all(User)
    if user_id:
        user = all_users.get("User." + user_id, None)
        return user.to_dict() if user else abort(404)
    else:
        for value in all_users.values():
            list_.append(value.to_dict())
        return jsonify(list_), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """Deletes a User object

    Args:
        user_id (str, optional): id of the user to be deleted.
            Defaults to None.

    Returns:
        HTTP-Response: If the user_id is not linked to any User object,
            raise a 404 error or Returns an empty dictionary
            with the status code 200
    """

    all_users = storage.all(User)
    user = all_users.get("User." + user_id, None)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(400)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def save_user():
    """[Creates a User]

    Returns:
        [HTTP-Response]: If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            If the dictionary doesn’t contain the key 'email',
            raise a 400 error with the message 'Missing email',
            If the dictionary doesn’t contain the key 'password',
            raise a 400 error with the message 'Missing password'
            Returns the new User with the status code 201
    """

    body = request.get_json()
    if request.is_json:
        if "email" not in body.keys():
            return jsonify(error="Missing email"), 404
        elif "password" not in body.keys():
            return jsonify(error="Missing password"), 404
        else:
            user = User(**body)
            user.save()
            return jsonify(user.to_dict()), 201
    return jsonify(error='Not a JSON'), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """Updates a Amenity object

    Args:
        amenity_id ([str], optional): Id of the User object to be updated.
            Defaults to None.

    Returns:
        [HTTP-Response]: If the amenity_id is not linked to any Amenity object,
            raise a 404 error
            If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            If everything is right
            returns the Amenity object with the status code 200
    """

    body = request.get_json()
    all_users = storage.all(User)
    user = all_users.get("User." + user_id, None)
    if user is None:
        abort(404)
    elif not request.is_json:
        return jsonify(error='Not a JSON'), 400

    for k, v in body.items():
        if k in ['id', 'updated_at', 'updated_at', 'email']:
            continue
        setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
