#!/usr/bin/python3
"""This module defines the view City"""

from models.city import City
from models.state import State
from . import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id=None):
    """Retrieves the list of all City objects from a determinated State

    Args:
        state_id (str, optional): id to search an state. Defaults to None.

    Returns:
        Response: If the state_id is not linked to any State object,
            raise a 404 error or a list of all Cities with response 200
    """

    list_ = []
    state = storage.get(State, state_id)
    if state:
        cities = state.cities
        list_ = []
        for value in cities:
            list_.append(value.to_dict())
        return jsonify(list_), 200
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities_by_id(city_id=None):
    """Retrieves a City Object

    Args:
        city_id (str, optional): id to search a City. Defaults to None.

    Returns:
        Response: If the state_id is not linked to any City object,
            raise a 404 error or a list with the City with response 200
    """

    city = storage.get(City, city_id)
    return city.to_dict() if city else abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """Deletes a City object

    Args:
        city_id (str, optional): id of the city to be deleted.
            Defaults to None.

    Returns:
        HTTP-Response: If the city_id is not linked to any City object,
            raise a 404 error or Returns an empty dictionary
            with the status code 200
    """

    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def save_city(state_id=None):
    """[Creates a City]

    Args:
        state_id (str, optional): id of the state where the city
            have to be created. Defaults to None.

    Returns:
        [HTTP-Response]: If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            If the dictionary doesn’t contain the key 'name',
            raise a 400 error with the message 'Missing name'
            Returns the new City with the status code 201
    """

    body = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif request.is_json:
        if "name" in body.keys():
            city = City(state_id=state_id, **body)
            city.save()
            return jsonify(city.to_dict()), 201
        else:
            return jsonify(error="Missing name"), 400
    return jsonify(error='Not a JSON'), 400


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id=None):
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
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    elif not request.is_json:
        return jsonify(error='Not a JSON'), 400

    for k, v in body.items():
        if k in ['id', 'updated_at', 'updated_at', 'state_id']:
            continue
        setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
