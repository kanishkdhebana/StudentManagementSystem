from app.models.users import db
from app.models.enrollments import Enrollment
from sqlalchemy.exc import IntegrityError

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
    
    def add_course(cls, course_code, course_name, instructor_id, department_name, description, credit_hours):
        from models.departments import Department
        
        department = Department.query.filter_by(department_name=department_name).first()
        department_id = department.department_id if department else None

        new_course = cls(
            course_code = course_code,
            course_name = course_name,
            instructor_id = instructor_id,
            department_id = department_id,
            description = description,
            credit_hours = credit_hours
        )
        
        try:
            db.session.add(new_course)
            db.session.commit()
            return True, None  
        
        except IntegrityError as e:
            db.session.rollback()
            return False, str(e.orig) if e.orig else "An error occurred. Please try again later." 
    
    def assign_instructor(self, instructor_id): 
        self.instructor_id = instructor_id
        db.session.commit()
    
    def __has_enrollments__(self):
        return Enrollment.query.filter_by(course_code=self.course_code).count() > 0
    
    def delete(self):
        if self.__has_enrollments__():
            return False  
        
        db.session.delete(self)
        db.session.commit()
        return True