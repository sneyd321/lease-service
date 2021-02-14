from . import house
from flask import request, Response, jsonify
import json, requests

from server.api.models import House

def get_tenant_service():
    return "http://host.docker.internal:8083/tenant/v1/"

def get_lease_service():
    return "http://host.docker.internal:8084/lease/v1/"

def get_problem_service():
    return "http://host.docker.internal:8085/problem/v1/"

def handle_post(url, request):
    try:
        response = requests.post(url, json=request.get_json(), headers=request.headers)
        return Response(response=response.text, status=response.status_code)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)


def handle_put(url, request):
    try: 
        response = requests.put(url, json=request.get_json(), headers=request.headers)
        return Response(response=response.text, status=response.status_code)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)

def handle_get(url, request):
    try:
        print(url)

        response = requests.get(url, headers=request.headers, timeout=5)
        if response.ok:
            return jsonify(response.json())
        return Response(response=response.text, status=response.status_code)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)



@house.route("House", methods=["POST"])
def create_house():
    try:
        data = request.get_json()
        house = House(data)
        if house.insert():
            return Response(response="House Created Successfully", status=201)
        return Response(response="Error: Conflict in database", status=409)
    except KeyError as e:
        return Response(response="Error: Invalid key entry " + str(e), status=400)
    

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
    return Response(response="Error: No house with homeowner id: " + str(houseId), status=404)


@house.route("House/<int:houseId>/Tenant")
def get_tenants_by_house_id(houseId):
    house = House.query.get(houseId)
    if house:
        url = get_tenant_service() + "House/" + str(houseId) + "/Tenant"
        return handle_get(url, request)
    return Response(response="Error: No house with homeowner id: " + str(id), status=404)
    


  
@house.route("Tenant/<int:tenantId>/Approve", methods=["PUT"])
def update_tenant(tenantId):
    url = get_tenant_service() + "Tenant/" + str(tenantId) + "/approve"
    return handle_put(url, request)


@house.route("House/<int:houseId>/Problem")
def get_problems(houseId):
    url = get_problem_service() + "House/" + str(houseId) + "/Problem"
    return handle_get(url, request)

@house.route("Problem/<int:problemId>", methods=["GET"])
def get_problem(problemId):
    print(vars(request))

    url = get_problem_service() + "Problem/" + str(problemId)
    return handle_get(url, request)
    

@house.route("Problem/<int:problemId>/Status", methods=["PUT"])
def put_problem(problemId):
    url = get_problem_service() + "Problem/" + str(problemId) + "/Status"
    return handle_put(url, request)




@house.route("Lease", methods=["POST"])
def upload_lease_agreement():
    try:
        homeownerData = request.get_json()
        house = House.query.get(homeownerData["houseId"])
        if house:
            homeownerData["house"] = house.toJson()
            print(homeownerData)
            response = requests.post(get_lease_service() + "OntarioLease", json=request.get_json(), headers=request.headers)
            return Response(response=response.text, status=response.status_code)
        return Response(response="Error: No house with homeowner id: " + str(id), status=404)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)

