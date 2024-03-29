from sqlalchemy import Date
from models.users import db

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id    = db.Column(db.Integer, primary_key = True)
    student_id       = db.Column(db.String(11), nullable = False)
    course_code      = db.Column(db.String(8), nullable = False)
    enrollment_date              = db.Column(Date, nullable = False)

    def __repr__(self) -> str:
        return f"{self.enrollment_id} {self.student_id} {self.enrollment_date}"
