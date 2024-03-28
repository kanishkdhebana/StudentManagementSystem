from sqlalchemy import Enum as EnumSQL
from sqlalchemy import Date
from enum import Enum
from models.users import db

class Sex(Enum):
    Male = 'Male'
    Female = 'Female'
    Other = 'Other'

class GradLevel(Enum):
    B_Tech = 'B_Tech'
    M_Tech = 'M_Tech'
    PHD = 'PHD'

class BloodGroup(Enum):
    A_plus = "A_plus"
    A_minus = "A_minus"
    B_plus = "B_plus"
    B_minus = "B_minus"
    AB_plus = "AB_plus"
    AB_minus = "AB_minus"
    O_plus = "O_plus"
    O_minus = "O_minus"

class Student(db.Model):
    __tablename__ = 'students'
    student_id       = db.Column(db.String(11), primary_key = True)
    first_name       = db.Column(db.String(45), nullable = False)
    middle_name      = db.Column(db.String(45), nullable = True)
    last_name        = db.Column(db.String(45), nullable = False)
    sex              = db.Column(EnumSQL(Sex), nullable = False)
    email            = db.Column(db.String(50), nullable = False)
    degree_name      = db.Column(db.String(100), nullable = False)
    grad_level       = db.Column(EnumSQL(GradLevel), nullable = False)
    address          = db.Column(db.String(400), nullable = False)
    city             = db.Column(db.String(50), nullable = False)
    state            = db.Column(db.String(50), nullable = False)
    address_pin      = db.Column(db.Integer, nullable = False)
    father_name      = db.Column(db.String(100), nullable = False)
    mother_name      = db.Column(db.String(100), nullable = False)
    dob              = db.Column(Date, nullable = False)
    bloodgroup       = db.Column(EnumSQL(BloodGroup), nullable = False)
    doa              = db.Column(Date, nullable = False)
    father_occ       = db.Column(db.String(100), nullable = False)
    mother_occ       = db.Column(db.String(100), nullable = False)
    student_phoneno  = db.Column(db.BigInteger, nullable = False)
    guardian_phoneno = db.Column(db.BigInteger, nullable = False)

    def __repr__(self) -> str:
        return f"{self.first_name} {self.middle_name} {self.last_name}"
