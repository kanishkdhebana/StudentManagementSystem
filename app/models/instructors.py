from sqlalchemy import Enum as EnumSQL
from sqlalchemy import Date
from enum import Enum
from models.users import db

class Sex(Enum):
    Male = 'Male'
    Female = 'Female'
    Other = 'Other'

class BloodGroup(Enum):
    A_plus = "A_plus"
    A_minus = "A_minus"
    B_plus = "B_plus"
    B_minus = "B_minus"
    AB_plus = "AB_plus"
    AB_minus = "AB_minus"
    O_plus = "O_plus"
    O_minus = "O_minus"

class Instructor(db.Model):
    __tablename__ = 'instructors'
    instructor_id = db.Column(db.String(11), primary_key = True)
    first_name    = db.Column(db.String(50), nullable = False)
    last_name     = db.Column(db.String(50), nullable = False)
    dob           = db.Column(Date, nullable = False)
    sex           = db.Column(EnumSQL(Sex), nullable = False)
    address       = db.Column(db.String(400), nullable = False)
    email         = db.Column(db.String(50), nullable = False)
    phone_number  = db.Column(db.BigInteger, nullable = False)
    doj           = db.Column(Date, nullable = False)
    city          = db.Column(db.String(50), nullable = False)
    state         = db.Column(db.String(50), nullable = False)
    address_pin   = db.Column(db.Integer, nullable = False)
    bloodgroup    = db.Column(EnumSQL(BloodGroup), nullable = False)

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"
