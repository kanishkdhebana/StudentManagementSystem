from sqlalchemy import Enum as EnumSQL
from sqlalchemy import Date
from enum import Enum
from app.models.users import db
from app.models.users import UserType, User
from app.models.courses import Course

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

    @classmethod
    def create_instructor(cls, instructor_data):
        # Check if instructor already exists
        existing_instructor = cls.query.filter_by(instructor_id = instructor_data['instructor_id']).first()
       
        if existing_instructor:
            return False, "Instructor already exists"

        # Create new instructor
        new_instructor = cls(
            instructor_id = instructor_data['instructor_id'],
            first_name = instructor_data['first_name'],
            last_name = instructor_data['last_name'],
            sex = instructor_data['sex'],
            email = instructor_data['email'],
            address = instructor_data['address'],
            city = instructor_data['city'],
            state = instructor_data['state'],
            address_pin = instructor_data['address_pin'],
            dob = instructor_data['dob'],
            bloodgroup = instructor_data['bloodgroup'],
            doj = instructor_data['doj'],
            phone_number = instructor_data['phone_number'],
        )

        # Add instructor to database
        db.session.add(new_instructor)
        db.session.commit()

        # Create associated user for the instructor
        user_password = f"{instructor_data['first_name'].lower()}{instructor_data['dob'].replace('-', '')}"
        new_user = User(user_id=instructor_data['instructor_id'], user_type = UserType.instructor)
        new_user.set_password(user_password)
        db.session.add(new_user)
        db.session.commit()

        return True, None
    
    def __is_valid_phone_number__(phone_number):
        return len(phone_number) == 10 and phone_number.isdigit()
    
    @classmethod
    def update_instructor_info(cls, instructor_id, email, phone_number):
        instructor = cls.query.filter_by(instructor_id=instructor_id).first()
        if not instructor:
            raise ValueError("Instructor not found.")

        # Validation logic
        if not __is_valid_phone_number__(phone_number):
            raise ValueError("Invalid phone number.")

        # Update instructor information
        instructor.email = email
        instructor.phone_number = phone_number

        db.session.commit()
        return instructor
    
    @classmethod
    def delete_instructor(cls, instructor_id):
        instructor = cls.query.filter_by(instructor_id=instructor_id).first()
        if not instructor:
            raise ValueError("Instructor not found.")

        # Disassociate instructor from courses
        associated_courses = Course.query.filter_by(instructor_id = instructor_id).all()
        for course in associated_courses:
            course.instructor_id = None
        
        # Delete the instructor
        db.session.delete(instructor)
        db.session.commit()

