#!/usr/bin/python3
'''starting a web app'''

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    '''Display "Hello HBNB!" on the root route'''
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''Display "HBNB" on the hbnb route'''
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    ''' display “C” followed by the value of the text variable'''
    new_text = text.replace('_', ' ')
    return f'C {new_text}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
