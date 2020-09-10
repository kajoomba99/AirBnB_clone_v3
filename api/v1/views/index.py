#!/usr/bin/python3
"""
Index file of views packages
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Return json with Ok status for /status route
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    Return the number of each object by type
    """
    return jsonify({'amenities': storage.count('Amenity'),
                    'cities': storage.count('City'),
                    'places': storage.count('Place'),
                    'reviews': storage.count('Review'),
                    'states': storage.count('State'),
                    'users': storage.count('User')})
