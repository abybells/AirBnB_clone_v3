#!/usr/bin/python3
"""views for places"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
  """get all places in a specified city"""
  city = storage.get("City", city_id)
  if city is None:
    abort(404)
  places = []
  for place in city.places:
    places.append(place.to_dict())
  return (jsonify(places))


@app_views.route('/places/<string:place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
  """get place info by place_id"""
  place = storage.get("Place", place_id)
  if place is None:
    abort(404)
  return (jsonify(place.to_dict()n))


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
  """delete place info by place_id"""
  place = storage.get("Place", place_id)
  if place is None:
    abort(404)
  place.delete()
  storage.save()
  return (jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
  """create new place in a city identified by city_id"""
  city = storage.get("City", city_id)
  if city is None:
    abort(404)
  if not request.get_json():
    return make_response(jsonify({'error': 'Not a JSON'}))
  kwargs = request.get_json()
  if 'user_id' not in kwargs:
    return make_response(jsonify({'error': 'Missing user_id'}), 400)
  user = storage.get("User", kwargs['user_id'])
  if user is None:
    abort(404)
  if 'name' not in kwargs:
    return make_response(jsonify({'error': 'Missing name'}), 400)
  kwargs['city_id'] = city_id
  place = Place(**kwargs)
  place.save()
  return (jsonify(place.to_dict()), 201)


@app_views.route('places/<string:place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
  """update a place identified with place_id"""
  place = storage.get("Place", place_id)
  if place is None:
    abort(404)
  if not request.get_json():
    return make_response(jsonify({'error': 'Not a JSON'}), 400)
  for attr, val in request.get_json().items():
    if attr not in ['id', 'user_id', 'city_id',
                      'created_at', 'updated_at']:
      setattr(place, attr, val)
  place.save()
  return (jsonify(place.to_dict()), 200)


@app_views.route('/places_search',
                 methods=['POST'], strict_slashes=False)
def places_search():
  """searches for a place"""
  all_places = [p for p in storage.all('Place').values()]
  if request.get_json() is None:
    abort(400, 'Not a JSON')
  states = request.get_json().get('states')
  if states and len(states) > 0:
    all_cities = storage.all('City')
    state_cities = set([city.id for city in all_cities.values()
                        if city.cates_id in states])
  else:
    state_cities = set()
  cities = request.get_json().get('cities')
  if cities and len(cities) > 0:
    cities = set([
      c_id for c_id in cities if storage.get('City', c_id)])
    state_cities = state_cities.union(cities)
  amenities = request.get_json().get('amenities')
  if len(state_cities) > 0:
    all_places = [p for p in all_places if p.city_id in state_cities]
  elif amenities is None or len(amenities) == 0:
    result = [place.to_json() for place in all_places]
    return jsonify(result)
  place_amenities = []
  if amenities and len(amenities) > 0:
    amenities = set([
      a_id for a_id in amenities if storage.get('Amenity', a_id)])
    for p in all_places:
      p_amenities = None
      if STORAGE_TYPE == 'db' and p.amenities:
        p_amenities = [a.id for a in p.amenities]
      elif len(p.amenities) > 0:
        p_amenities = p_amenities
      if p_amenities and all([a in p_amenities for a in amenities]):
        places_amenities.append(p)
  else:
    places_amenities = all_places
  result = [place.to_json() for place in places_amenities]
  return jsonify(result)
