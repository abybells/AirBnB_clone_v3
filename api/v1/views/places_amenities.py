#!/usr/bin/python3
"""views for places_amenity"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from datetime import datetime
import uuid
from os import getenv

@app_views.route('/places/<string:place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """get amenity information for a specific place"""
    amenities = []
    place = storage.get("Place", place_id)
    if place is None:
      abort(404)
    amenity = place.amenities
    for val in amenity:
      amenities.append(val.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>', 
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
  """deletes an amenity object from a place"""
  place = storage.get("Place", place_id)
  amenity = storage.get("Amenity", amenity_id)
  if place is None or amenity is None:
    abort(404)
  if amenity_id not in [ameni.id for ameni in place.amenities]:
    abort(404)
  place.amenities.remove(amenity)
  storage.save()
  return (jsonify({}), 200)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
  """adds an amenity object to a place"""
  place = storage.get("Place", place_id)
  amenity = storage.get("Amenity", amenity_id)
  if place is None or amenity is None:
    abort(404)
  if amenity_id in [ameni.id for ameni in place.amenities]:
    return (jsonify(amenity.to_dict()), 200)
  else:
    place.amenities.append(amenity)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)
