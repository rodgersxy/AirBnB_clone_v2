#!/usr/bin/python3
"""
a script that starts a Flask web application
"""


from flask import Flask, render_template
from models.state import State
from models import storage
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    the list of all State objects present in DBStorage sorted by name (A->Z)
    """
    path = '7-states_list.html'
    states = storage.all(State)
    sorted_states = sorted(states.values(), key=lambda state: state.name)
    return render_template(path, sorted_states=sorted_states)


@app.teardown_appcontext
def app_teardown(arg=None):
    """
    clean-up the storag
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
