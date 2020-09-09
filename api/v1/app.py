#!/usr/bin/python3
"""main app module"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

port = os.environ.get('HBNB_API_PORT', '5000')
host = os.environ.get('HBNB_API_HOST', '0.0.0.0')

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(void):
    """
        Method excecuted when the connection is closed

        close the connection with the DBStorage
    """
    storage.close()


@app.errorhandler(404)
def notfound(e):
    return jsonify(error=e.name), 404


if __name__ == "__main__":
    app.run(port=port, host=host, threaded=True)
