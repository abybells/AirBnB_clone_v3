#!/usr/bin/python3
"""views for amenities"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def all_amenities():
    """get amenity information for all amenities"""
    amenities = []
    for key, value in storage.all("Amenity").item():
        amenities.append(value.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'], strict_slashes=False)
def obj_amenity(amenity_id):
    """get amenity info. by amenity_id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """delete amenity by amenity_id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenity', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """create new amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response.get_json(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenity/<string:amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """update an amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, val)
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
