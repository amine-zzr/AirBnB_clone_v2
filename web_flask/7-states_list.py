#!/usr/bin/python3
'''starting a web app'''

from flask import Flask, render_template
from models.state import State
from models import storage
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    '''display a HTML page with the states'''
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    '''closes the storage on teardown'''
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
