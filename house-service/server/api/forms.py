from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, Optional


class CustomRadioField(RadioField):

    def pre_validate(self, form):
        pass

class CustomSelectField(SelectField):

    def pre_validate(self, form):
        pass



class ArrangementForm(FlaskForm):
    arrangement = CustomRadioField('Arrangement',  choices=[("Basement", "Basement"), ("Condo", "Condo")])
    province = CustomSelectField("Province",  choices=[("Ontario", "Ontario")] )


class HomeownerLocationForm(FlaskForm):

    streetNumber = StringField('Street Number', 
    validators=[InputRequired("Please enter a street number"), Length(min=1, max=10, message="Please enter a street number less that 10 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. 1234"})

    streetName = StringField('Street Name', 
    validators=[InputRequired("Please enter a street name"), Length(min=1, max=200, message="Please enter a street name less that 200 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. Front St."})

    city = StringField('City', 
    validators=[InputRequired("Please enter a street name"), Length(min=1, max=100, message="Please enter a city less that 100 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. Toronto"})

    postalCode = StringField('Postal Code', 
    validators=[InputRequired("Please enter a postal code"), Length(min=1, max=10, message="Please enter a postal code less that 10 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. L1T 0E2"})

    poBox = StringField('P.O. Box', 
    validators=[Optional(), Length(min=1, max=10, message="Please enter a P.O. box less that 10 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. 1234"})

    unitNumber = StringField('Unit Number', 
    validators=[Optional(), Length(min=1, max=10, message="Please enter a unit number less that 10 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. 1234"})


 

class RentalUnitLocationForm(FlaskForm):
    streetNumber = StringField('Street Number', 
    validators=[InputRequired("Please enter a street number"), Length(min=1, max=10, message="Please enter a street number less that 10 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. 1234"})

    streetName = StringField('Street Name', 
    validators=[InputRequired("Please enter a street name"), Length(min=1, max=200, message="Please enter a street name less that 200 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. Front St."})

    city = StringField('City', 
    validators=[InputRequired("Please enter a street name"), Length(min=1, max=200, message="Please enter a city less that 100 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. Toronto"})

    postalCode = StringField('Postal Code', 
    validators=[InputRequired("Please enter a postal code"), Length(min=1, max=200, message="Please enter a postal code less that 10 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. L1T 0E2"})


        
class RentDetailsForm(FlaskForm):

    rentDueDate = CustomRadioField('Rent Due Date', coerce=bool, choices=[(True, "First"), (True, "Second"), (True, "Last")])

    rentAmount = IntegerField('Rent Amount',
    validators=[InputRequired("Please enter a rent amount")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. $500", "type": "number"})

    rentMadePayableTo = IntegerField('Rent Made Payable To', 
    validators=[InputRequired("Please enter who rent is made payable to")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. John Smith", "type": "text"})

    parkingAmount = IntegerField('Parking Amount',
    validators=[InputRequired("Please enter a parking amount")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. $50", "type": "number"})

    parkingSpaces = IntegerField('Parking Spaces', 
    validators=[InputRequired("Please enter a parking spaces")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. 2", "type": "number"})

    

class AmenityForm(FlaskForm):
    airConditoning = CustomRadioField('Air Conditioning', coerce=bool, choices=[(True, "Included In Rent"), (False, "Not Included in Rent")])
    storage = CustomRadioField('Storage', coerce=bool, choices=[(True, "Included In Rent"), (False, "Not Included in Rent")])
    onSiteLaundry = CustomRadioField('On-Site Laundry', coerce=bool, choices=[(True, "Included In Rent"), (False, "Not Included in Rent")])
    gas = CustomRadioField('Gas', coerce=bool, choices=[(True, "Included In Rent"), (False, "Not Included in Rent")])
    guestParking = CustomRadioField('Guest Parking', coerce=bool, choices=[(True, "Included In Rent"), (False, "Not Included in Rent")])


class UtilityForm(FlaskForm):
    heat = CustomRadioField('Heat', coerce=bool, choices=[(True, "Tenant Responsibility"), (True, "My Responsibility")])
    electricity = CustomRadioField('Electricity', coerce=bool, choices=[(True, "Tenant Responsibility"), (True, "My Responsibility")])
    water = CustomRadioField('Water', coerce=bool, choices=[(True, "Tenant Responsibility"), (True, "My Responsibility")])  