from app.models.users import db
from app.models.students import Student
from sqlalchemy.exc import IntegrityError

class Department(db.Model):
    __tablename__   = 'departments'
    department_id   = db.Column(db.String(11), primary_key = True)
    department_name = db.Column(db.String(100), nullable = False)
 
    def __repr__(self) -> str:
        return f"{self.department_name}"

    @classmethod
    def create(cls, department_id, department_name):
        existing_department = cls.query.filter_by(department_id = department_id).first()
        if existing_department:
            return "Department with this ID already exists."

        new_department = cls (
            department_id = department_id,
            department_name = department_name
        )

        try:
            db.session.add(new_department)
            db.session.commit()
            return "Department added successfully!"
        
        except IntegrityError as e:
            db.session.rollback()
            return f"Error: {str(e.orig)}"
        
        
    @classmethod
    def delete_department(cls, department_id):
        from models.courses import Course
        
        associated_students = Student.query.filter_by(department_id = department_id).all()
        associated_courses = Course.query.filter_by(department_id = department_id).all()

        if associated_students or associated_courses:
            return "Cannot delete department because there are associated students or courses."

        department = cls.query.filter_by(department_id=department_id).first()
        if department:
            try:
                db.session.delete(department)
                db.session.commit()
                return "Department deleted successfully!"
            
            except Exception as e:
                db.session.rollback()
                return f"Error: {str(e)}"
            
        return "Department not found."
