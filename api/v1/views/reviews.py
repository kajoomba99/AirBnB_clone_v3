#!/usr/bin/python3
"""This module defines the view Review"""

from models.place import Place
from models.review import Review
from models.user import User
from . import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id=None):
    """Retrieves the list of all Review objects from a determinated Place

    Args:
        place_id (str, optional): id to search a place. Defaults to None.

    Returns:
        Response: If the place_id is not linked to any Place object,
            raise a 404 error or a list of all Reviews with response 200
    """

    list_ = []
    place = storage.get(Place, place_id)
    if place:
        reviews = place.reviews
        list_ = []
        for value in reviews:
            list_.append(value.to_dict())
        return jsonify(list_), 200
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id=None):
    """Retrieves a Review Object

    Args:
        review_id (str, optional): id to search a Review. Defaults to None.

    Returns:
        Response: If the review_id is not linked to any Review object,
            raise a 404 error or a list with the Review, with response 200
    """

    review = storage.get(Review, review_id)
    return review.to_dict() if review else abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """Deletes a Review object

    Args:
        review_id (str, optional): id of the review to be deleted.
            Defaults to None.

    Returns:
        HTTP-Response: If the review_id is not linked to any Review object,
            raise a 404 error or Returns an empty dictionary
            with the status code 200
    """

    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(400)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def save_review(place_id=None):
    """[Creates a Review]

    Args:
        place_id (str, optional): id of the place where the review
            have to be created. Defaults to None.

    Returns:
        [HTTP-Response]: If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            If the dictionary doesn’t contain the key 'user_id',
            raise a 400 error with the message 'Missing user_id'
            if the dictionary doesn’t contain the key 'text'
            raise a 400 error with the message 'Missing text'
            Returns the new Review with the status code 201
    """

    body = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        return jsonify(error='Not a JSON'), 400
    if "user_id" not in body.keys():
        return jsonify(error="Missing user_id"), 404

    user = storage.get(User, body["user_id"])
    if not user:
        abort(404)

    if "text" not in body.keys():
        return jsonify(error="Missing text"), 404

    review = Review(place_id=place_id, **body)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """Updates a Review object

    Args:
        review_id ([str], optional): Id of the Review object to be updated.
            Defaults to None.

    Returns:
        [HTTP-Response]: If the review_id is not linked to any Review object,
            raise a 404 error
            If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            If everything is right
            returns the Review object with the status code 200
    """

    body = request.get_json()
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    elif not request.is_json:
        return jsonify(error='Not a JSON'), 400
    for k, v in body.items():
        if k in ['id', 'user_id', 'place_id', 'updated_at', 'updated_at',
                 'state_id']:
            continue
        setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict()), 200
