from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, Optional


class CustomRadioField(RadioField):

    def pre_validate(self, form):
        pass

class CustomSelectField(SelectField):

    def pre_validate(self, form):
        pass



class RentDetailsForm(FlaskForm):

    rentDueDate = CustomRadioField('rentDueDate', coerce=bool, choices=[(True, "First"), (True, "Second"), (True, "Last")])

    baseRent = IntegerField('Rent Amount',
    validators=[InputRequired("Please enter a rent amount")], 
    render_kw={"icon": "monetization_on", "required": False, "helperText": "Ex. $500", "type": "number"})

    rentMadePayableTo = StringField('Rent Made Payable To', 
    validators=[InputRequired("Please enter who rent is made payable to")], 
    render_kw={"icon": "fact_check", "required": False, "helperText": "Ex. John Smith", "type": "text"})

    parkingAmount = IntegerField('Parking Amount',
    validators=[InputRequired("Please enter a parking amount")], 
    render_kw={"icon": "monetization_on", "required": False, "helperText": "Ex. $50", "type": "number"})

    parkingSpaces = IntegerField('Parking Spaces', 
    validators=[InputRequired("Please enter a parking spaces")], 
    render_kw={"icon": "local_parking", "required": False, "helperText": "Ex. 2", "type": "number"})

    

class AmenityForm(FlaskForm):
    airConditoning = CustomRadioField('airConditioning', coerce=bool, choices=[(True, "Included In Rent"), (False, "Not Included in Rent")])
    storage = CustomRadioField('storage', coerce=bool, choices=[(True, "Included In Rent"), (False, "Not Included in Rent")])
    onSiteLaundry = CustomRadioField('onSiteLaundry', coerce=bool, choices=[(True, "Included In Rent"), (False, "Not Included in Rent")])
    gas = CustomRadioField('gas', coerce=bool, choices=[(True, "Included In Rent"), (False, "Not Included in Rent")])
    guestParking = CustomRadioField('guestParking', coerce=bool, choices=[(True, "Included In Rent"), (False, "Not Included in Rent")])


class UtilityForm(FlaskForm):
    heat = CustomRadioField('heat', coerce=bool, choices=[(True, "Tenant Responsibility"), (False, "My Responsibility")])
    electricity = CustomRadioField('electricity', coerce=bool, choices=[(True, "Tenant Responsibility"), (False, "My Responsibility")])
    water = CustomRadioField('water', coerce=bool, choices=[(True, "Tenant Responsibility"), (False, "My Responsibility")])  
    internet = CustomRadioField('internet', coerce=bool, choices=[(True, "Tenant Responsibility"), (False, "My Responsibility")])  