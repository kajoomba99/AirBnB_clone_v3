#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, escape, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
import uuid
app = Flask(__name__)


@app.route('/3-hbnb/', strict_slashes=False)
def hbnb():
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template(
        '3-hbnb.html',
        states=states,
        amenities=amenities,
		places=places,
        cache_id =uuid.uuid4()
    )


@app.teardown_appcontext
def tear_dow(void):
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)