#!/usr/bin/python3
"""index.py to connect to API"""
from app.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage

all_classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
        }


@app_views.route('/status', strict_slashes=False)
def status():
    """display status response"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """display number of objects by type"""
    return_dict = {}
    for key, value in all_classes.item():
        return_dict[key] = storage.count(value)
        return jsonify(return_dict)
