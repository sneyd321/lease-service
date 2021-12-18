from server import db
from sqlalchemy.exc import IntegrityError, OperationalError




class Lease:

    def __init__(self, houseId):
        self._rentDetails = RentDetails.query.filter(RentDetails.houseId == houseId).first()
        self._amenities = Amenity.query.filter(Amenity.houseId == houseId).first()
        self._utilities = Utility.query.filter(Utility.houseId == houseId).first()


    def toJson(self):
        return {
            "rentDetails": self._rentDetails.toJson() if self._rentDetails else {},
            "amenities": self._amenities.toJson() if self._amenities else {},
            "utilities": self._utilities.toJson() if self._utilities else {}
        }


class RentDetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    rentDueDate = db.Column(db.String(10))
    baseRent = db.Column(db.Integer())
    rentMadePayableTo = db.Column(db.String(200))
    parkingAmount = db.Column(db.Integer())
    parkingSpaces = db.Column(db.Integer())
    houseId = db.Column(db.Integer(), nullable=False, unique=True)
    

    def __init__(self, **rentDetailsData):
        self.rentDueDate = rentDetailsData.get("rentDueDate", "")
        self.baseRent = rentDetailsData.get("baseRent", "")
        self.rentMadePayableTo = rentDetailsData.get("rentMadePayableTo", "")
        self.parkingAmount = rentDetailsData.get("parkingAmount", "")
        self.parkingSpaces = rentDetailsData.get("parkingSpaces", "")
        self.houseId = rentDetailsData.get("houseId")

       
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
        rows = RentDetails.query.filter(RentDetails.houseId == self.houseId).update(self.toDict(), synchronize_session=False)
        if rows == 1:
            try:
                db.session.commit()
                db.session.close()
                return True
            except OperationalError:
                db.session.rollback()
                db.session.close()
                return False
        return False


    def toDict(self):
        return {
            RentDetails.rentDueDate: self.rentDueDate,
            RentDetails.baseRent: self.baseRent,
            RentDetails.rentMadePayableTo: self.rentMadePayableTo,
            RentDetails.parkingAmount: self.parkingAmount,
            RentDetails.parkingSpaces: self.parkingSpaces,
            RentDetails.houseId: self.houseId
        }

    def toJson(self):
        return {
            "rentDueDate": self.rentDueDate,
            "baseRent": self.baseRent,
            "rentMadePayableTo": self.rentMadePayableTo,
            "parkingAmount": self.parkingAmount,
            "parkingSpaces": self.parkingSpaces,
            "houseId": self.houseId
        }
    

    def __repr__(self):
        return "< Rent Details: " + str(self.baseRent) + " >"



class Amenity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    airConditioning = db.Column(db.Boolean())
    gas = db.Column(db.Boolean())
    guestParking = db.Column(db.Boolean())
    storage = db.Column(db.Boolean())
    onSiteLaundry = db.Column(db.Boolean())
    houseId = db.Column(db.Integer(), nullable=False, unique=True)
    
    

    def __init__(self, **amenityData):
        self.airConditioning = amenityData.get("airConditioning", "") == "True"
        self.gas = amenityData.get("gas", "") == "True"
        self.guestParking = amenityData.get("guestParking", "") == "True"
        self.storage = amenityData.get("storage", "") == "True"
        self.onSiteLaundry = amenityData.get("onSiteLaundry", "") == "True"

        self.houseId = amenityData.get("houseId", "")
        


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
        print(self.toDict())
        

        rows = Amenity.query.filter(Amenity.houseId == self.houseId).update(self.toDict())
        print(rows)
        if rows == 1:
            try:
                db.session.commit()
                db.session.close()
                return True
            except OperationalError:
                db.session.rollback()
                db.session.close()
                return False
        return False

    def toDict(self):
        return {
            Amenity.airConditioning: self.airConditioning,
            Amenity.gas: self.gas,
            Amenity.guestParking: self.guestParking,
            Amenity.storage: self.storage,
            Amenity.onSiteLaundry: self.onSiteLaundry,
            Amenity.houseId: self.houseId
        }

    def toJson(self):
        return [
                    {
                        "name": "Air Conditioning",
                        "includedInRent": self.airConditioning
                    },
                    {
                        "name": "Gas",
                        "includedInRent": self.gas
                    },
                    {
                        "name": "On Site Laundry",
                        "includedInRent": self.onSiteLaundry
                    },
                    {
                        "name": "Storage",
                        "includedInRent": self.storage
                    },
                    {
                        "name": "Guest Parking",
                        "includedInRent": self.guestParking
                    }
                ]
        
    

    def __repr__(self):
        return "<Amenity " + str(self.airConditioning) + " >"
        
class Utility(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    heat = db.Column(db.Boolean())
    electricity = db.Column(db.Boolean())
    water = db.Column(db.Boolean())
    internet = db.Column(db.Boolean())
    houseId = db.Column(db.Integer(), nullable=False, unique=True)
    


    
    def __init__(self, **utilityData):
        self.heat = utilityData.get("heat", "") == "True"
        self.electricity = utilityData.get("electricity", "") == "True"
        self.water = utilityData.get("water", "") == "True"
        self.internet = utilityData.get("internet", "") == "True"
        self.houseId = utilityData.get("houseId", "0")


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
        rows = Utility.query.filter(Utility.houseId == self.houseId).update(self.toDict(), synchronize_session=False)
        if rows == 1:
            try:
                db.session.commit()
                db.session.close()
                return True
            except OperationalError:
                db.session.rollback()
                db.session.close()
                return False
        return False

    def toDict(self):
        return  {
            Utility.heat: self.heat,
            Utility.electricity: self.electricity,
            Utility.water: self.water,
            Utility.internet: self.internet,
            Utility.houseId: self.houseId
        }

    def toJson(self):
        return  [
                    {
                        "name": "Heat",
                        "responsibilityOf": "Tenant" if self.heat else "Homeowner"
                    },
                    {
                        "name": "Electricity",
                        "responsibilityOf": "Tenant" if self.electricity else "Homeowner"
                    },
                    {
                        "name": "Water",
                        "responsibilityOf": "Tenant" if self.water else "Homeowner"
                    },
                    {
                        "name": "Internet",
                        "responsibilityOf": "Tenant" if self.internet else "Homeowner"
                    }
                ]

   

    def __repr__(self):
        return "<Utility " + str(self.water) + " >"


