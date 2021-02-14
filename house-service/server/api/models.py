from werkzeug.security import generate_password_hash, check_password_hash
from server import db
from sqlalchemy.exc import IntegrityError, OperationalError



amenities = db.Table("house_amenities",
db.Column("houseId", db.Integer(), db.ForeignKey("house.id")),
db.Column("amenityId", db.Integer(), db.ForeignKey("amenity.id")))

utilities = db.Table("house_utilities",
db.Column("houseId", db.Integer(), db.ForeignKey("house.id")),
db.Column("utilityId", db.Integer(), db.ForeignKey("utility.id")))


class House(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    homeownerId = db.Column(db.Integer(), nullable=False)
    rentalUnitLocation = db.relationship("RentalUnitLocation", backref="House", lazy=True, uselist=False)
    homeownerLocation = db.relationship("HomeownerLocation", backref="House", lazy=True, uselist=False)
    rentDetails = db.relationship("RentDetails", backref="House", lazy=True, uselist=False)
    utilities = db.relationship("Utility", secondary=utilities, backref=db.backref("House", lazy="dynamic"))
    amenities = db.relationship("Amenity", secondary=amenities, backref=db.backref("House", lazy="dynamic"))

    def __init__(self, houseData):
        self.homeownerId = houseData["homeownerId"]
        self.homeownerLocation = HomeownerLocation(houseData["homeownerLocation"])
        self.rentalUnitLocation = RentalUnitLocation(houseData["rentalUnitLocation"])    
        self.rentDetails = RentDetails(houseData["rentDetails"])
        self.utilities = [Utility(utilityData) for utilityData in houseData["utilities"]]
        self.amenities = [Amenity(amenityData) for amenityData in houseData["amenities"]]

    def toJson(self):
        return {
            "houseId": self.id,
            "homeownerId": self.homeownerId,
            "homeownerLocation": self.homeownerLocation.toJson(),
            "rentalUnitLocation": self.rentalUnitLocation.toJson(),
            "rentDetails": self.rentDetails.toJson(),
            "utilities": [utility.toJson() for utility in self.utilities],
            "amenities": [amenity.toJson() for amenity in self.amenities],
        }
 
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False
            
    

    def update(self):
        try:
            self.homeownerLocation.update()
            self.rentalUnitLocation.update()
            self.rentDetails.update()
            for utility in self.utilities:
                utility.update()
            for amenity in self.amenities:
                amenity.update()
            db.session.commit()
            return True
        except OperationalError:
            db.session.rollback()
            return False
    
    def __repr__(self):
        return "< House: House >"


class RentalUnitLocation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    streetNumber = db.Column(db.Integer())
    streetName = db.Column(db.String(200))
    city = db.Column(db.String(100))
    province = db.Column(db.String(100))
    postalCode = db.Column(db.String(10))
    unitName = db.Column(db.String(100))
    parkingSpaces = db.Column(db.Integer())
    isCondo = db.Column(db.Boolean())
    houseId = db.Column(db.Integer(), db.ForeignKey('house.id'), nullable=False)
    

    def __init__(self, rentalUnitLocationData):
        self.streetNumber = rentalUnitLocationData["streetNumber"]
        self.streetName = rentalUnitLocationData["streetName"]
        self.city = rentalUnitLocationData["city"]
        self.province = rentalUnitLocationData["province"]
        self.postalCode = rentalUnitLocationData["postalCode"]
        self.unitName = rentalUnitLocationData["unitName"]
        self.parkingSpaces = rentalUnitLocationData["parkingSpaces"]
        self.isCondo = rentalUnitLocationData["isCondo"]


   
    def update(self):
        RentalUnitLocation.query.update(self.toDict(), synchronize_session=False)
        db.session.commit()

    def toDict(self):
        return {
            RentalUnitLocation.streetNumber: self.streetNumber,
            RentalUnitLocation.streetName: self.streetName,
            RentalUnitLocation.city: self.city,
            RentalUnitLocation.province: self.province,
            RentalUnitLocation.postalCode: self.postalCode,
            RentalUnitLocation.unitName: self.unitName,
            RentalUnitLocation.parkingSpaces: self.parkingSpaces,
            RentalUnitLocation.isCondo: self.isCondo
        }

    def toJson(self):
        return {
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitName": self.unitName,
            "parkingSpaces": self.parkingSpaces,
            "isCondo": self.isCondo
        }

    def __repr__(self):
        return "< Rental Unit Location: " + str(self.streetNumber) + " " + self.streetName + " >"


class RentDetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    rentDueDate = db.Column(db.String(10))
    baseRent = db.Column(db.Integer())
    parkingAmount = db.Column(db.Integer())
    paymentOptions = db.relationship("PaymentOption", backref="rentDetails", lazy="dynamic")
    houseId = db.Column(db.Integer(), db.ForeignKey('house.id'), nullable=False)
    

    def __init__(self, rentDetailsData):
        self.rentDueDate = rentDetailsData["rentDueDate"]
        self.baseRent = rentDetailsData["baseRent"]
        self.parkingAmount = rentDetailsData["parkingAmount"]
        self.paymentOptions = [PaymentOption(paymentOptionData) for paymentOptionData in rentDetailsData["paymentOptions"]]
    
    def update(self):
        RentDetails.query.update(self.toDict(), synchronize_session=False)
        for paymentOption in self.paymentOptions:
            paymentOption.update()
        db.session.commit()


    def toDict(self):
        return {
            RentDetails.baseRent: self.baseRent,
            RentDetails.parkingAmount: self.parkingAmount
        }

    def toJson(self):
        return {
            "rentDueDate": self.rentDueDate,
            "baseRent": self.baseRent,
            "parkingAmount": self.parkingAmount,
            "paymentOptions": [paymentOption.toJson() for paymentOption in self.paymentOptions]
        }
    

    def __repr__(self):
        return "< Rent Details: " + str(self.baseRent) + " >"

class PaymentOption(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20))
    rentMadePayableTo = db.Column(db.String(100))
    rentDetailsId = db.Column(db.Integer(), db.ForeignKey('rent_details.id'), nullable=False)

    def __init__(self, paymentOptionsData):
        self.name = paymentOptionsData["name"]
        self.rentMadePayableTo = paymentOptionsData["rentMadePayableTo"]

    def update(self):
        PaymentOption.query.update(self.toDict(), synchronize_session=False)
        db.session.commit()

    def toDict(self):
        return {
            PaymentOption.name: self.name,
            PaymentOption.rentMadePayableTo: self.rentMadePayableTo
        }
    
    def toJson(self):
        return {
            "name": self.name,
            "rentMadePayableTo": self.rentMadePayableTo
        }

    def __repr__(self):
        return "< Payment Options: " + self.name + " >"

class Amenity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    includedInRent = db.Column(db.Boolean())
    payPerUse = db.Column(db.Boolean())
    

    def __init__(self, amenityData):
        self.name = amenityData["name"]
        self.payPerUse = amenityData["payPerUse"]
        self.includedInRent = amenityData["includedInRent"]

   
    def update(self):
        Amenity.query.update(self.toDict(), synchronize_session=False)
        db.session.commit()

    def toDict(self):
        return {
            Amenity.name: self.name,
            Amenity.includedInRent: self.includedInRent
        
        }

    def toJson(self):
        return {
            "name": self.name,
            "includedInRent": self.includedInRent
        }
    

    def __repr__(self):
        return "<Amenity " + self.name + " >"
        
class Utility(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    responsibilityOf = db.Column(db.String(100))


    def __init__(self, utilityData):
        self.name = utilityData["name"]
        self.responsibilityOf = utilityData["responsibilityOf"]

   

    def update(self):
        Utility.query.update(self.toDict(), synchronize_session=False)
        db.session.commit()

    def toDict(self):
        return  {
            Utility.name: self.name,
            Utility.responsibilityOf: self.responsibilityOf
        }

    def toJson(self):
        return  {
            "name": self.name,
            "responsibilityOf": self.responsibilityOf
        }
   

    def __repr__(self):
        return "<Utility " + self.name + " >"


class HomeownerLocation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    streetNumber = db.Column(db.Integer())
    streetName = db.Column(db.String(200))
    city = db.Column(db.String(100))
    province = db.Column(db.String(100))
    postalCode = db.Column(db.String(10))
    unitNumber = db.Column(db.String(10))
    poBox = db.Column(db.String(10))
    houseId = db.Column(db.Integer(), db.ForeignKey('house.id'), nullable=False)

    def __init__(self, homeownerLocationData):
        self.streetNumber = homeownerLocationData["streetNumber"]
        self.streetName = homeownerLocationData["streetName"]
        self.city = homeownerLocationData["city"]
        self.province = homeownerLocationData["province"]
        self.postalCode = homeownerLocationData["postalCode"]
        self.unitNumber = homeownerLocationData["unitNumber"]
        self.poBox = homeownerLocationData["poBox"]

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            return False

    def update(self):
        HomeownerLocation.query.filter(HomeownerLocation.homeownerId == self.homeownerId).update(self.toDict(), synchronize_session=False)
        db.session.commit()

    def delete(self):
        HomeownerLocation.query.filter(HomeownerLocation.homeownerId == self.homeownerId).delete()
        db.session.commit()

    def toDict(self):
        return {
            HomeownerLocation.streetNumber: self.streetNumber,
            HomeownerLocation.streetName: self.streetName,
            HomeownerLocation.city: self.city,
            HomeownerLocation.province: self.province,
            HomeownerLocation.postalCode: self.postalCode,
            HomeownerLocation.unitNumber: self.unitNumber,
            HomeownerLocation.poBox: self.poBox
        }

    def toJson(self):
        return {
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitNumber": self.unitNumber,
            "poBox": self.poBox
        }

    def __repr__(self):
        return "< Homeowner Location: " + str(self.streetNumber) + " " + self.streetName + " >"