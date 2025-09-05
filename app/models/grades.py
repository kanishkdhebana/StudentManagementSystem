from sqlalchemy import Enum as EnumSQL
from enum import Enum
from app.models.users import db

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
    
    @classmethod
    def update_or_add_grade(cls, enrollment_id, new_grade):
        grade = cls.query.filter_by(enrollment_id = enrollment_id).first()
        
        if grade:
            grade.grade = new_grade
            db.session.commit()
            return True
        
        else:
            new_grade_record = cls(enrollment_id=enrollment_id, grade=new_grade)
            db.session.add(new_grade_record)
            db.session.commit()
            return True
        return False
 