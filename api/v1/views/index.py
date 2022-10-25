#!/usr/bin/python3
"""index.py to connect to API"""
from app.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """display status response"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """display number of objects by type"""
    classes = {"Amenity": "amenities", "City": "cities",
               "Place": "places", "Review": "reviews",
               "State": "states", "User": "users"}
    stats_dict = {}
    for cls in classes.keys():
        stats_dict[classes[cls]] = storage.count(cls)
    return jsonify(stats_dict)
