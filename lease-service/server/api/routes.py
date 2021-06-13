from . import lease
from flask import request, Response, jsonify, render_template, redirect
import json, requests
from server.api.forms import RentDetailsForm, AmenityForm, UtilityForm
from server.api.models import  RentDetails, Amenity, Utility, Lease
from server.api.RequestManager import RequestManager, Zookeeper


zookeeper = Zookeeper()

def get_homeowner_gateway():
    return "192.168.0.108:8080"

def parse_token(request):
    bearer = request.headers.get("Authorization")
    if bearer:
        print(bearer, flush=True)
        return bearer[7:]
    return None


########################################################################################################


@lease.route("LeaseComplete/Ontario/<int:houseId>", methods=["POST"])
def lease_complete(houseId):
    service = zookeeper.get_service("image-upload-service")
    if service:
        ontarioLease = Lease(houseId)
        print(ontarioLease.toJson())
        
        imageUploadManager = RequestManager(request, service)
        return imageUploadManager.post("image/v1/Lease/Ontario/" + str(houseId), ontarioLease.toJson())
    return Response(response="Error: Zookeeper down", status=503)

##############################################################################################################################################


@lease.route("RentDetails/Ontario/<int:houseId>")
def get_rent_details(houseId):
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    if service:
        token = parse_token(request)
        if token:
            form = RentDetailsForm()
            return render_template("OntarioRentDetails.html", form=form, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/RentDetails/Ontario/" + str(houseId), token=token )
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Zookeeper down", status=503)
   
@lease.route("RentDetails/Ontario/<int:houseId>", methods=["POST"])
def create_rent_details(houseId):
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    if service:
        form = RentDetailsForm(request.form)
        attrs = list(form._fields.values())
        if form.validate():
            rentDetails = RentDetails(houseId=houseId, **request.form)
            if RentDetails.query.filter(RentDetails.houseId == houseId).first():
                if rentDetails.update():
                    print("RENT DETAILS UPDATE")
                    return Response(response="Amenities/Ontario/" + str(houseId), status=201)
            else:
                if rentDetails.insert():
                    print("RENT DETAILS INSERT")
                    return Response(response="Amenities/Ontario/" + str(houseId), status=201)
            return render_template("OntarioRentDetails.html", form=form, fields=attrs, conflict="Error: Failed to insert rent details", url="http://" + service + "/homeowner-gateway/v1/RentDetails/Ontario/" + str(houseId))
        return render_template("OntarioRentDetails.html", form=form, fields=attrs, conflict="", url="http://" + service + "/homeowner-gateway/v1/RentDetails/Ontario/" + str(houseId) )
    return Response(response="Error: Zookeeper down", status=503)
    


@lease.route("Amenities/Ontario/<int:houseId>")
def view_amenities(houseId):
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    names = ["Air Conditioning", "Storage", "On-Site Laundry", "Gas", "Guest Parking"]
    if service:
        form = AmenityForm()
        return render_template("OntarioAmenities.html", form=form, names=names, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/Amenities/Ontario/" + str(houseId))
    return Response(response="Error: Zookeeper down", status=503)
   
 

@lease.route("Amenities/Ontario/<int:houseId>", methods=["GET", "POST"])
def create_amenities(houseId):
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    names = ["Air Conditioning", "Storage", "On-Site Laundry", "Gas", "Guest Parking"]
    if service:
        form = AmenityForm(request.form)
        attrs = list(form._fields.values())
        if form.validate():
            amenities = Amenity(houseId=houseId, **request.form)
            

            if Amenity.query.filter(Amenity.houseId == amenities.houseId).first():
                if amenities.update():
                    print("Amenity UPDATE")
                    return Response(response="Utilities/Ontario/" + str(houseId), status=201)
            else:
                if amenities.insert():
                    print("Amenity INSERT")
                    return Response(response="Utilities/Ontario/" + str(houseId), status=201)
        
            return render_template("OntarioAmenities.html", form=form, names=names, fields=attrs, conflict="Error: Failed to insert amenities", url="http://" + service + "/homeowner-gateway/v1/Amenities/Ontario/" + str(houseId))
        return render_template("OntarioAmenities.html", form=form, names=names, fields=attrs, conflict="", url="http://" + service + "/homeowner-gateway/v1/Amenities/Ontario/" + str(houseId))

    return Response(response="Error: Zookeeper down", status=503)
    

@lease.route("Utilities/Ontario/<int:houseId>")
def view_utilities(houseId):
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    names = ["Heat", "Electricity", "Water", "Internet"]
    if service:
        form = UtilityForm()
        return render_template("OntarioUtilities.html", form=form, names=names, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/Utilities/Ontario/" + str(houseId))
    return Response(response="Error: Zookeeper down", status=503)
   
   




@lease.route("Utilities/Ontario/<int:houseId>", methods=["POST"])
def create_utilities(houseId):
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    names = ["Heat", "Electricity", "Water", "Internet"]
    if service:
        form = UtilityForm(request.form)
        attrs = list(form._fields.values())
        if form.validate():
            utilities = Utility(houseId=houseId, **request.form)
            if Utility.query.filter(Utility.houseId == houseId).first():
                if utilities.update():
                    print("Utility UPDATE")

                    return Response(response="LeaseComplete/Ontario/" + str(houseId), status=201)
            else:
                if utilities.insert():
                    print("Utility INSERT")
                    return Response(response="LeaseComplete/Ontario/" + str(houseId), status=201)
            
            return render_template("OntarioUtilities.html", form=form, fields=attrs, names=names, conflict="", url="http://" + service + "/homeowner-gateway/v1/Utilities/Ontario/" + str(houseId))
        return render_template("OntarioUtilities.html", form=form, fields=attrs, names=names, conflict="", url="http://" + service + "/homeowner-gateway/v1/Utilities/Ontario/" + str(houseId))
    return Response(response="Error: Zookeeper down", status=503)
  

