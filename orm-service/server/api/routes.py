from . import house
from flask import request, Response, jsonify
import json, requests

from server.api.models import House


@house.route("Homeowner/<int:id>/House", methods=["POST"])
def create_house(id):
    data = request.get_json()
    try:
        resource = House(data)
        resource.homeownerId = id
        if resource.insert():
            return Response(status=201)
        return Response(response="Error: Conflict in database", status=409)
    except KeyError:
        return Response(response="Error: Data in invalid format", status=400)

@house.route("Homeowner/<int:id>/House")
def get_house(id):
    houses = House.query.filter(House.homeownerId == id).all()
    if houses:
        return jsonify([house.toJson() for house in houses])
    return Response(response="Error: No house with homeowner id: " + id, status=404)
