from sqlalchemy import Enum as EnumSQL
from enum import Enum
from models.users import db

class Grades(Enum):
    AA = "AA"
    AB = "AB"
    BB = "BB"
    BC = "BC"
    CC = "CC"
    CD = "CD"
    DD = "DD"
    FF = "FF"
    FP = "FP"

class Grade(db.Model):
    __tablename__ = 'grades'
    grade_id      = db.Column(db.Integer, primary_key = True)
    enrollment_id = db.Column(db.Integer, nullable = False)
    grade         = db.Column(EnumSQL(Grades), nullable = True)

    def __repr__(self) -> str:
        return f"{self.grade_id} {self.grade}"
