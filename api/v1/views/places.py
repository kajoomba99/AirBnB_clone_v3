#!/usr/bin/python3
"""This module defines the view Place"""

from models.place import Place
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from . import app_views
from flask import jsonify, abort, request
from models import storage
from os import getenv
STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id=None):
    """Retrieves the list of all Place objects from a determinated City

    Args:
        city_id (city_id, optional): id to search an city. Defaults to None.

    Returns:
        Response: If the state_id is not linked to any City object,
            raise a 404 error
            If everythin is right return
            a list of all places with response 200
    """

    list_ = []
    city = storage.get(City, city_id)
    if city:
        places = city.places
        for place in places:
            list_.append(place.to_dict())
        return jsonify(list_), 200
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """Retrieves a Place Object

    Args:
        place_id (str, optional): id to search a Place. Defaults to None.

    Returns:
        Response: If the state_id is not linked to any Place object,
            raise a 404 error or
            if everything is right return a list
            with the Place with response 200
    """

    place = storage.get(Place, place_id)
    return place.to_dict() if place else abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Deletes a Place object

    Args:
        place_id (str, optional): id of the place to be deleted.
            Defaults to None.

    Returns:
        HTTP-Response: If the place_id is not linked to any place object,
            raise a 404 error or Returns an empty dictionary
            with the status code 200
    """

    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def save_place(city_id=None):
    """[Creates a Place]

    Args:
        city_id (str, optional): id of the city where the place
            have to be created. Defaults to None.

    Returns:
        [HTTP-Response]: If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            If the dictionary doesn’t contain the key 'name',
            raise a 400 error with the message 'Missing name'
            Returns the new City with the status code 201
    """

    body = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        return jsonify(error='Not a JSON'), 400

    if "user_id" not in body.keys():
        return jsonify(error="Missing user_id"), 400
    user = storage.get(User, body['user_id'])

    if user is None:
        abort(404)
    if "name" not in body.keys():
        return jsonify(error="Missing name"), 400
    place = Place(city_id=city_id, **body)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """Updates a Place object

    Args:
        place_id ([str], optional): Id of the Place object to be updated.
            Defaults to None.

    Returns:
        [HTTP-Response]: If the place_id is not linked to any Place object,
            raise a 404 error
            If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            If everything is right
            returns the Amenity object with the status code 200
    """

    body = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    elif not request.is_json:
        return jsonify(error='Not a JSON'), 400

    for k, v in body.items():
        if k in ['id', 'updated_at', 'updated_at', 'user_id', 'city_id']:
            continue
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
