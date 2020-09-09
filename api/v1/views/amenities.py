#!/usr/bin/python3
"""This module defines the view City"""

from models.amenity import Amenity
from . import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """Retrieves the list of all Amenity objects

    Args:
        amenity_id (str, optional): id to search an amenity. Defaults to None.

    Returns:
        Response: If the amenity_id is not linked to any Amenity object,
            raise a 404 error or a list of all Amenity with response 200
    """

    list_ = []
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            return jsonify(amenity.to_dict()), 200
        abort(404)
    else:
        amenities = storage.all(Amenity)
        for amenity in amenities.values():
            list_.append(amenity.to_dict())
        return jsonify(list_), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Deletes a Amenity object

    Args:
        amenity_id (str, optional): id of the amenity to be deleted.
            Defaults to None.

    Returns:
        HTTP-Response: If the amenity_id is not linked to any Amenity object,
            raise a 404 error or Returns an empty dictionary
            with the status code 200
    """

    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(400)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def save_amenity():
    """[Creates a Amenity]

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
            amenity = Amenity(**body)
            amenity.save()
            return jsonify(amenity.to_dict()), 201
        else:
            return jsonify(error="Missing name"), 404
    return jsonify(error='Not a JSON'), 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id=None):
    """Updates a Amenity object

    Args:
        amenity_id ([str], optional): Id of the Amenity object to be updated.
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
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    elif not request.is_json:
        return jsonify(error='Not a JSON'), 400

    for k, v in body.items():
        if k in ['id', 'updated_at', 'updated_at']:
            continue
        setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
