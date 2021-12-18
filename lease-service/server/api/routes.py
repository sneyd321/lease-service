from . import lease
from flask import request, Response, jsonify, render_template, redirect
import json, requests
from server.api.forms import RentDetailsForm, AmenityForm, UtilityForm
from server.api.models import  RentDetails, Amenity, Utility, Lease
from server.api.RequestManager import RequestManager, Zookeeper
from server import app


zookeeper = Zookeeper()

def get_homeowner_gateway():
    return "34.107.132.144"




########################################################################################################


@lease.route("LeaseComplete/Ontario/<int:houseId>", methods=["POST"])
def lease_complete(houseId):
    service = zookeeper.get_service("image-upload-service")
    if not service:
        return Response(response="Error: Zookeeper down", status=503)

    ontarioLease = Lease(houseId)
    print(ontarioLease.toJson())
    imageUploadManager = RequestManager(request, service)
    return imageUploadManager.post("image/v1/Lease/Ontario/" + str(houseId), ontarioLease.toJson())
    

##############################################################################################################################################


@lease.route("RentDetails/Ontario/<int:houseId>")
def get_rent_details(houseId):
   
    service = get_homeowner_gateway()
   

    form = RentDetailsForm()
    return render_template("OntarioRentDetails.html", 
    form=form, 
    fields=list(form._fields.values()), 
    conflict="", 
    url="http://" + service + "/homeowner-gateway/v1/RentDetails/Ontario/" + str(houseId))


   
@lease.route("RentDetails/Ontario/<int:houseId>", methods=["POST"])
def create_rent_details(houseId):
    
    service = get_homeowner_gateway()
    form = RentDetailsForm(request.form)
    attrs = list(form._fields.values())

    if not request.form or "rentDueDate" not in request.form or "baseRent" not in request.form or "rentMadePayableTo" not in request.form or "parkingAmount" not in request.form or "parkingSpaces" not in request.form:
        return render_template("OntarioRentDetails.html", 
        form=form, 
        fields=attrs, 
        conflict="Error Invalid Request Data", 
        url="http://" + service + "/homeowner-gateway/v1/RentDetails/Ontario/" + str(houseId) )

    if not form.validate():
        return render_template("OntarioRentDetails.html", 
        form=form, 
        fields=attrs, 
        conflict="", 
        url="http://" + service + "/homeowner-gateway/v1/RentDetails/Ontario/" + str(houseId) )
    
    rentDetails = RentDetails.query.filter(RentDetails.houseId == houseId).first()
    if rentDetails:
        if not rentDetails.update():
            return render_template("OntarioRentDetails.html", 
            form=form, 
            fields=attrs, 
            conflict="Error: Failed to update rent details", 
            url="http://" + service + "/homeowner-gateway/v1/RentDetails/Ontario/" + str(houseId))

        print("UPDATE")
        return Response(response="Amenities/Ontario/" + str(houseId), status=201)
    else:
        rentDetails = RentDetails(houseId=houseId, **request.form)
        if not rentDetails.insert():
            return render_template("OntarioRentDetails.html", 
            form=form, 
            fields=attrs, 
            conflict="Error: Failed to insert rent details", 
            url="http://" + service + "/homeowner-gateway/v1/RentDetails/Ontario/" + str(houseId))

        print("INSERT")
        return Response(response="Amenities/Ontario/" + str(houseId), status=201)
    


@lease.route("Amenities/Ontario/<int:houseId>")
def view_amenities(houseId):
    
    service = get_homeowner_gateway()
    

    names = ["Air Conditioning", "Storage", "On-Site Laundry", "Gas", "Guest Parking"]
    form = AmenityForm()
    return render_template("OntarioAmenities.html", form=form, names=names, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/Amenities/Ontario/" + str(houseId))

 

@lease.route("Amenities/Ontario/<int:houseId>", methods=["GET", "POST"])
def create_amenities(houseId):
    service = get_homeowner_gateway()
    
    names = ["Air Conditioning", "Storage", "On-Site Laundry", "Gas", "Guest Parking"]
    form = AmenityForm(request.form)
    attrs = list(form._fields.values())
    if not request.form or "airConditioning" not in request.form or "storage" not in request.form or "onSiteLaundry" not in request.form or "gas" not in request.form or "guestParking" not in request.form:
        return render_template("OntarioAmenities.html", 
        form=form, 
        names=names, 
        fields=attrs, 
        conflict="Error Invalid Request Data", 
        url="http://" + service + "/homeowner-gateway/v1/Amenities/Ontario/" + str(houseId))


    if not form.validate():
        return render_template("OntarioAmenities.html", 
        form=form, 
        names=names, 
        fields=attrs, 
        conflict="", 
        url="http://" + service + "/homeowner-gateway/v1/Amenities/Ontario/" + str(houseId))

   
    
    amenities = Amenity.query.filter(Amenity.houseId == houseId).first()
    if amenities:
        print(request.form)
        
        if not amenities.update():
            return render_template("OntarioAmenities.html", 
            form=form, 
            names=names, 
            fields=attrs, 
            conflict="Error: Failed to update amenities", 
            url="http://" + service + "/homeowner-gateway/v1/Amenities/Ontario/" + str(houseId))
        return Response(response="Utilities/Ontario/" + str(houseId), status=201)
    else:
        amenities = Amenity(houseId=houseId, **request.form)
 
        if not amenities.insert():

            return render_template("OntarioAmenities.html", 
            form=form, 
            names=names, 
            fields=attrs, 
            conflict="Error: Failed to insert amenities", 
            url="http://" + service + "/homeowner-gateway/v1/Amenities/Ontario/" + str(houseId))
        return Response(response="Utilities/Ontario/" + str(houseId), status=201)


    

@lease.route("Utilities/Ontario/<int:houseId>")
def view_utilities(houseId):
    service = get_homeowner_gateway()
    

    names = ["Heat", "Electricity", "Water", "Internet"]
    form = UtilityForm()
    return render_template("OntarioUtilities.html", 
    form=form, 
    names=names, 
    fields=list(form._fields.values()), 
    conflict="",
    url="http://" + service + "/homeowner-gateway/v1/Utilities/Ontario/" + str(houseId))


   




@lease.route("Utilities/Ontario/<int:houseId>", methods=["POST"])
def create_utilities(houseId):
   
    service = get_homeowner_gateway()
  

    names = ["Heat", "Electricity", "Water", "Internet"]
    form = UtilityForm(request.form)
    attrs = list(form._fields.values())

    if not request.form or "heat" not in request.form or "electricity" not in request.form or "water" not in request.form or "internet" not in request.form:
        return render_template("OntarioUtilities.html", 
        form=form, 
        fields=attrs, 
        names=names, 
        conflict="Error Invalid Request Data", 
        url="http://" + service + "/homeowner-gateway/v1/Utilities/Ontario/" + str(houseId))

    if not form.validate():
        return render_template("OntarioUtilities.html", 
        form=form, 
        fields=attrs, 
        names=names, 
        conflict="", 
        url="http://" + service + "/homeowner-gateway/v1/Utilities/Ontario/" + str(houseId))

    utilities = Utility.query.filter(Utility.houseId == houseId).first()
    if utilities:
        if not utilities.update():
            return render_template("OntarioUtilities.html", 
            form=form, 
            fields=attrs, 
            names=names, 
            conflict="Error failed to update", 
            url="http://" + service + "/homeowner-gateway/v1/Utilities/Ontario/" + str(houseId))
        return Response(response="LeaseComplete/Ontario/" + str(houseId), status=201)

    else:
        utilities = Utility(houseId=houseId, **request.form)
        if not utilities.insert():
            return render_template("OntarioUtilities.html", 
            form=form, 
            fields=attrs, 
            names=names, 
            conflict="Error failed to insert", 
            url="http://" + service + "/homeowner-gateway/v1/Utilities/Ontario/" + str(houseId))
        return Response(response="LeaseComplete/Ontario/" + str(houseId), status=201)
    
    
  

@lease.route("RentDetails/<int:houseId>/Tenant")
def get_tenant_rent_details(houseId):
    rentDetails = RentDetails.query.filter(RentDetails.houseId == houseId).first()
    if rentDetails:
        return jsonify(rentDetails.toJson())
    return Response(status=404)