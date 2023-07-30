#!/usr/bin/python3
"""Index blueprint page """
from . import app_views
from flask import jsonify
from models import storage

@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """returns number of each instance type """
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
