#!/usr/bin/python
"""
a script that starts a Flask web application
web application must be listening on 0.0.0.0, port 5000
"""


from models.state import State
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def state():
    """
    display a HTML page: (inside the tag BODY)
    with the list of all State objects present in DBStorage sorted by name
    """
    states = storage.all(State)
    return render_template('9-states.html', states=states, mode='all')


@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """
    display a HTML page: (inside the tag BODY)
    State object is found with this id
    """
    for state in storage.all(State).values():
        if state.id == id:
            return render_template('9-states.html', states=state, mode='id')
    return render_template('9-states.html', states=state, mode='none')


@app.teardown_appcontext
def close(self):
    """
    Close session(method)
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
