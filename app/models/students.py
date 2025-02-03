from sqlalchemy import Enum as EnumSQL
from sqlalchemy import Date
from enum import Enum
from datetime import datetime
from models.users import db
from models.users import User, UserType
from models.enrollments import Enrollment

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
    #degree_name      = db.Column(db.String(100), nullable = False)
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
    
    department_id = db.Column(db.String(11), db.ForeignKey('departments.department_id'), nullable=False)

    def __repr__(self) -> str:
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    

    @classmethod
    def add_student(cls, student_data):
        existing_student = cls.query.filter_by(student_id=student_data['student_id']).first()
        if existing_student:
            return None

        new_student = Student(
            student_id = student_data['student_id'],
            first_name = student_data['first_name'],
            middle_name = student_data['middle_name'],
            last_name = student_data['last_name'],
            sex = student_data['sex'],
            email = student_data['email'],
            grad_level = student_data['grad_level'],
            address = student_data['address'],
            city = student_data['city'],
            state = student_data['state'],
            address_pin = student_data['address_pin'],
            father_name = student_data['father_name'],
            mother_name = student_data['mother_name'],
            dob = student_data['dob'],
            bloodgroup = student_data['bloodgroup'],
            doa = student_data['doa'],
            father_occ = student_data['father_occ'],
            mother_occ = student_data['mother_occ'],
            student_phoneno = student_data['student_phoneno'],
            guardian_phoneno = student_data['guardian_phoneno'],
            department_id = student_data['department_id']
        )

        # Create user for the student
        user_password = f"{student_data['first_name'].lower()}{student_data['dob'].replace('-', '')}"
        new_user = User(user_id=student_data['student_id'], user_type = UserType.student)
        new_user.set_password(user_password)

        try:
            db.session.add(new_student)
            db.session.add(new_user)
            db.session.commit()
            return new_student
        
        except IntegrityError:
            db.session.rollback()
            return None
        
    
    @classmethod
    def delete_student(cls, student_id):
        student = cls.query.filter_by(student_id=student_id).first()
        if student:
            # Delete associated enrollments
            Enrollment.query.filter_by(student_id=student_id).delete()

            # Delete associated user
            User.query.filter_by(user_id=student_id).delete()

            # Delete the student
            db.session.delete(student)
            db.session.commit()
            return True
        return False
    
    
    def update_student_info(self, student_data):
        self.email = student_data['email']
        self.student_phoneno = student_data['student_phoneno']
        self.guardian_phoneno = student_data['guardian_phoneno']

        db.session.commit()
        
        
    @classmethod
    def enroll_in_course(cls, student_id, course_code):
        
        existing_enrollment = Enrollment.query.filter_by(
            student_id = student_id,
            course_code = course_code
        ).first()
        
        if existing_enrollment:
            return False
        
        new_enrollment = Enrollment(
            student_id=student_id,
            course_code=course_code,
            enrollment_date = datetime.now()
        )

        try:
            db.session.add(new_enrollment)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False
