from . import house
from flask import request, Response, jsonify
import json, requests

from server.api.models import House

@house.route("House", methods=["POST"])
def create_house():
    data = request.get_json()
    print(data)
    
    try:
        house = House(data)
        if house.insert():
            return Response(status=201)
        return Response(response="Error: Conflict in database", status=409)
    except KeyError as e:
        return Response(response="Error: Data in invalid format", status=400)


@house.route("Homeowner/<int:id>/House")
def get_houses(id):
    houses = House.query.filter(House.homeownerId == id).all()
    if houses:
        return jsonify([house.toJson() for house in houses])
    return Response(response="Error: No house with homeowner id: " + str(id), status=404)


@house.route("House/<int:houseId>")
def get_house(houseId):
    house = House.query.get(houseId)
    if house:
        return jsonify(house.toJson())
    return Response(response="Error: No house with homeowner id: " + str(id), status=404)
