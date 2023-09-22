#!/usr/bin/python3
"""
a script that starts a Flask web application
"""


from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state_list():
    """
    the list of all State objects present in DBStorage sorted by name (A->Z)
    """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """
    clean-up the storag
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
