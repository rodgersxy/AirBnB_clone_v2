#!/usr/bin/python3
"""
Start flask web app on port 5000
listen on 0.0.0.0
"""
from models import storage
from models.state import State
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """
    display a HTML page: (inside the tag BODY)
    H1 tag: “States”
    UL tag: with the list of all State objects present in DBStorage sorted
    by name (A->Z)
    """
    path = '8-cities_by_states.html'
    states = storage.all(State)
    return render_template(path, states=states)


@app.teardown_appcontext
def app_teardown(arg=None):
    """
    clean up
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
