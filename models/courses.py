from flask_sqlalchemy import SQLAlchemy
from models.users import db

class Course(db.Model):
    __tablename__  = 'courses'
    course_code    = db.Column(db.String(8), primary_key = True)
    course_name    = db.Column(db.String(100), nullable = False)
    instructor_id  = db.Column(db.String(11), nullable = True)
    department_id  = db.Column(db.String(11), nullable = False)
    description    = db.Column(db.String(400), nullable = False)
    credit_hours   = db.Column(db.Integer, nullable = False)

    def __repr__(self) -> str:
        return f"{self.course_name} {self.description}"
