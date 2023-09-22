#!/usr/bin/python3
"""
a script that will start flask web app
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """To display Hello HBNB!"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """To display HBNB"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """
    display C followed by the value of the text variable
    (replace underscore _ symbols with a space )
    """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    """
    display 'Python', followed by the value of the text variable
    The default value of text is 'is cool'
    """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """
    /number/<n>: display 'n is a number' only if n is an integer
    """
    return '{:d} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def num_template(n):
    """
    display a HTML page only if n is an integer
    H1 tag: 'Number: n' inside the tag BODY
    """
    path = '5-number.html'
    return render_template(path, n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_even_or_odd(n):
    """
    display a HTML page only if n is an integer
    H1 tag: 'Number: n is even|odd' inside the tag BODY
    """
    if n % 2 == 0:
        evenly = 'even'
    else:
        evenly = 'odd'
    return render_template('6-number_odd_or_even.html', n=n, evenly=evenly)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
