#!/usr/bin/python3
"""simple Flask app"""

from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "0.0.0.0"
    }
})


@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"


@app.teardown_appcontext
def close(exception):
    """tears down the app when its closed"""
    storage.close()


@app.errorhandler(404)
def not_fnd(error):
    """ Returns 404 status JSON response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    # Change the host parameter from '127.0.0.1' to '0.0.0.0'
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
