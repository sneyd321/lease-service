from . import house
from flask import request, Response, jsonify, render_template, redirect
import json, requests
from server.api.forms import HomeownerLocationForm, RentalUnitLocationForm, RentDetailsForm, AmenityForm, UtilityForm, ArrangementForm

from server.api.models import House

def get_tenant_service():
    return "http://tenant-service.default.svc.cluster.local:8083/tenant/v1/"

def get_lease_service():
    return "http://lease-service.default.svc.cluster.local:8084/lease/v1/"

def get_problem_service():
    return "http://problem-service.default.svc.cluster.local:8085/problem/v1/"


def get_homeowner_gateway_service():
    return "http://192.168.0.107:8080/homeowner-gateway/v1/"

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




@house.route("House", methods=["POST", "GET"])
def create_house():
    if request.method == 'GET':
        form = ArrangementForm()
        attrs = list(form._fields.values())
        print(request.form)
        return render_template("Arrangement.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "House")


    if request.method == 'POST':
        print(request.form)
        form = ArrangementForm(request.form)
        attrs = list(form._fields.values())

        if form.validate():
            

            return Response(response="OntarioHomeownerLocation", status=201)
            #rentalUnitLocation = RentalUnitLocation(**request.form)
            
            #if rentalUnitLocation.insert():
            #return "<h1>Account successfully created</h1>"
            #return render_template("RentalUnitLocation.html", form=form, fields=attrs, conflict="Error: Account already exists")
        return render_template("Arrangement.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "House")



@house.route("OntarioHomeownerLocation", methods=["POST", "GET"])
def create_homeowner_location():
    if request.method == 'GET':
        form = HomeownerLocationForm()
        attrs = list(form._fields.values())
        return render_template("OntarioHomeownerLocation.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "OntarioHomeownerLocation")

    if request.method == 'POST':
        print(request.form)
        form = HomeownerLocationForm(request.form)
        attrs = list(form._fields.values())

        if form.validate():
    
            return Response(response="OntarioRentalUnitLocation", status=201)
            #rentalUnitLocation = RentalUnitLocation(**request.form)
            #return Response(response="Homeowner location created successfully.", status=200)
            #if rentalUnitLocation.insert():
            #return "<h1>Account successfully created</h1>"
            #return render_template("RentalUnitLocation.html", form=form, fields=attrs, conflict="Error: Account already exists")
        return render_template("OntarioHomeownerLocation.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "OntarioHomeownerLocation")




@house.route("OntarioRentalUnitLocation", methods=["POST", "GET"])
def create_rental_unit_basement_location():
    if request.method == 'GET':
        form = RentalUnitLocationForm()
        attrs = list(form._fields.values())
        return render_template("OntarioRentalUnitLocation.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "OntarioRentalUnitLocation")

    if request.method == 'POST':
        print(request.form)
        form = RentalUnitLocationForm(request.form)
        attrs = list(form._fields.values())

        if form.validate():
            
   
            #rentalUnitLocation = RentalUnitLocation(**request.form)
           
            #if rentalUnitLocation.insert():
            return Response(response="OntarioRentDetails", status=201)
            #return render_template("RentalUnitLocation.html", form=form, fields=attrs, conflict="Error: Account already exists")
        return render_template("OntarioRentalUnitLocation.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "OntarioRentalUnitLocation")






@house.route("OntarioRentDetails", methods=["GET", "POST"])
def create_rent_details():
    if request.method == 'GET':
        form = RentDetailsForm()
        attrs = list(form._fields.values())
        return render_template("OntarioRentDetails.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "OntarioRentDetails")

    if request.method == 'POST':
        print(request.form)
        form = RentDetailsForm(request.form)
        attrs = list(form._fields.values())



        if form.validate():
    
            #return redirect("http://host.docker.internal:8088/location/v1/RentalUnitLocation")
            #rentalUnitLocation = RentalUnitLocation(**request.form)
            return Response(response="OntarioAmenities", status=201)
            #if rentalUnitLocation.insert():
            #return render_template("RentalUnitLocation.html", form=form, fields=attrs, conflict="Error: Account already exists")
        return render_template("OntarioRentDetails.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "OntarioRentDetails")



@house.route("OntarioAmenities", methods=["GET", "POST"])
def create_amenities():
    if request.method == 'GET':
        form = AmenityForm()
        attrs = list(form._fields.values())
        return render_template("OntarioAmenities.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "OntarioAmenities")

    if request.method == 'POST':
        print(request.form)
        form = AmenityForm(request.form)
        attrs = list(form._fields.values())



        if form.validate():
    
            return Response(response="OntarioUtilities", status=201)
            #rentalUnitLocation = RentalUnitLocation(**request.form)
           
            #if rentalUnitLocation.insert():
            #return "<h1>Account successfully created</h1>"
            #return render_template("RentalUnitLocation.html", form=form, fields=attrs, conflict="Error: Account already exists")
        return render_template("OntarioAmenities.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "OntarioAmenities")


@house.route("OntarioUtilities", methods=["GET", "POST"])
def create_utilities():
    if request.method == 'GET':
        form = UtilityForm()
        attrs = list(form._fields.values())
        return render_template("OntarioUtilities.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "OntarioUtilities")

    if request.method == 'POST':
        print(request.form)
        form = UtilityForm(request.form)
        attrs = list(form._fields.values())



        if form.validate():
    
            #return redirect("http://host.docker.internal:8088/location/v1/RentalUnitLocation")
            #rentalUnitLocation = RentalUnitLocation(**request.form)

            #if rentalUnitLocation.insert():
            return "<h1>House successfully created</h1>"
            #return render_template("RentalUnitLocation.html", form=form, fields=attrs, conflict="Error: Account already exists")
        return render_template("OntarioUtilities.html", form=form, fields=attrs, conflict="", url=get_homeowner_gateway_service() + "OntarioUtilities")













    

@house.route("Homeowner/<int:id>/House")
def get_houses(id):
    houses = House.query.filter(House.homeownerId == id).all()
    if houses:
        return jsonify([house.toJson() for house in houses])
    return Response(response="Error: No houses with homeowner id: " + str(id), status=404)


@house.route("House/<int:houseId>")
def get_house(houseId):
    house = House.query.get(houseId)
    if house:
        return jsonify(house.toJson())
        
    return Response(response="Error: No house with house id: " + str(houseId), status=404)

























@house.route("House/<int:houseId>/Tenant")
def get_tenants_by_house_id(houseId):
    house = House.query.get(houseId)
    if house:
        url = get_tenant_service() + "House/" + str(houseId) + "/Tenant"
        return handle_get(url, request)
    return Response(response="Error: No house with house id: " + str(houseId), status=404)
    


  
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

@house.route("/Problem", methods=["POST"])
def create_problem():
    url = get_problem_service() + "Problem"
    image = request.files["image"]
    data = request.files['data']
    files = {
        "image": (image.filename, image.read(), "image/jpg"),
        "data": ("data", data.read(), "application/json")
    }
    try:
        response = requests.post(url, files=files)
        return Response(response=response.text, status=response.status_code)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)





















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
        return Response(response="Error: No house with house id: " + str(homeownerData["houseId"]), status=404)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)

@house.route("House/<int:houseId>/lease", methods=["PUT"])
def update_lease(houseId):
    data = request.get_json()
    lease = data["lease"]
    house = House.query.get(houseId)
    if house:
        house.lease = lease
        if house.update():
            return Response(response="Update Successful", status=200) 
        return Response(response="Failed to update lease", status=500) 
    return Response(response="House not found", status=404)
