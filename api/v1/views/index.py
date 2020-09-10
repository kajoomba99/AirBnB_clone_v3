#!/usr/bin/python3
"""
Restful API for Airbnb clone
"""
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardowndb(self):
    """
    method that calls storage.close()
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 error with JSON response 404
    """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=getenv('HBNB_API_PORT', default='5000'),
        threaded=True
    )
