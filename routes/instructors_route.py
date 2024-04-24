"""
Routes for managing instructors in the application.

This module defines routes for adding, viewing, and managing instructors.

Attributes:
    instructors_blueprint (flask.Blueprint): Blueprint object for defining instructor routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.instructors import Instructor, db
from models.users import User, UserType
from models.students import Student
from models.enrollments import Enrollment
from models.grades import Grade, Grades
from models.courses import Course
from models.departments import Department
from sqlalchemy.exc import IntegrityError

# Blueprint object for defining instructor routes
instructors_blueprint = Blueprint('instructors', __name__)

@instructors_blueprint.route("/add_instructor", methods=['GET', 'POST'])
@login_required
def add_instructor():
    """
    Route for adding a new instructor.

    This route allows administrators to add a new instructor by submitting a form. If the form is submitted via POST method, it validates the input and adds the new instructor to the database.

    Returns:
        str: Rendered template for adding an instructor or a redirect to the admin_dashboard route.
    """
    if current_user.user_type != UserType.admin:
        return 'Unauthorized', 403
    
    if request.method == 'POST':
        instructor_id = request.form['instructor_id']
        
        existing_instructor = Instructor.query.filter_by(instructor_id = instructor_id).first()
        if existing_instructor:
            return redirect(url_for('instructors.add_instructor'))
        
        first_name  = request.form['first_name']
        last_name    = request.form['last_name']
        sex          = request.form['sex']
        email        = request.form['email']
        address      = request.form['address']
        city         = request.form['city']
        state        = request.form['state']
        address_pin  = int(request.form['address_pin'])
        dob          = request.form['dob']
        bloodgroup   = request.form['bloodgroup'] 
        doj          = request.form['doj']
        phone_number = request.form['phone_number']

        new_instructor = Instructor(
            instructor_id = instructor_id,
            first_name    = first_name,
            last_name     = last_name,
            sex           = sex,
            email         = email,
            address       = address,
            city          = city,
            state         = state,
            address_pin   = address_pin,
            dob           = dob,
            bloodgroup    = bloodgroup,
            doj           = doj,
            phone_number  = phone_number,
        ) 

        try:
            db.session.add(new_instructor)
            db.session.commit()
            
            user_password = f"{request.form['first_name'].lower()}{request.form['dob'].replace('-', '')}"
            new_user = User(user_id = instructor_id, user_type = UserType.instructor)
            new_user.set_password(user_password)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for("dashboard.admin_dashboard"))
        
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig) if e.orig else "An error occurred. Please try again later."
            return render_template("error.html", message = error_message)

    return render_template("add_instructor.html")


@instructors_blueprint.route("/edit_instructor_info/<string:instructor_id>", methods=['GET', 'POST'])
@login_required
def edit_instructor(instructor_id):
    """
    Route for editing instructor information.

    This route allows instructors to edit their information. If the form is submitted via POST method, it updates the instructor information in the database.

    Args:
        instructor_id (str): The ID of the instructor to be edited.

    Returns:
        str: Rendered template for editing instructor information or a redirect to the instructor dashboard.
    """
    
    if current_user.user_type != UserType.instructor or current_user.user_id != instructor_id:
        return 'Unauthorized', 403
    
    if request.method == 'POST':
        instructor = Instructor.query.filter_by(instructor_id = instructor_id).first()
        
        # Validate phone numbers
        if not is_valid_phone_number(request.form['phone_number']):
            return redirect(url_for('instructors.edit_instructor', instructor_id = instructor_id))

        instructor.email = request.form['email']
        instructor.phone_number = request.form['phone_number']

        db.session.commit()

        return redirect(url_for('dashboard.instructor_dashboard'))

    instructor = Instructor.query.filter_by(instructor_id = instructor_id).first()
    return render_template('edit_instructor_info.html', instructor = instructor ) 

def is_valid_phone_number(phone_number):
    """
    Check if the phone number consists of exactly 10 digits.

    Args:
        phone_number (str): Phone number to validate.

    Returns:
        bool: True if the phone number consists of exactly 10 digits, False otherwise.
    """
    return len(phone_number) == 10 and phone_number.isdigit()


# Define a mapping function for enum values
def get_enum_display(enum_value):
    """
    Map enum values to human-readable strings.

    Args:
        enum_value (enum.Enum): The enum value to be mapped.

    Returns:
        str: The human-readable string representation of the enum value.
    """
    if enum_value is None:
        return None
    elif enum_value.__class__.__name__ == 'BloodGroup':
        blood_group_mapping = {
            'A_plus'  : 'A+',
            'A_minus' : 'A-',
            'B_plus'  : 'B+',
            'B_minus' : 'B-',
            'AB_plus' : 'AB+',
            'AB_minus': 'AB-',
            'O_plus'  : 'O+',
            'O_minus' : 'O-'
        }
        return blood_group_mapping.get(enum_value.value)
    return str(enum_value).replace('_', ' ')


# Pass the mapped values to the template
@instructors_blueprint.route('/view_instructors', methods = ['GET', 'POST'])
@login_required
def view_instructors():
    """
    Route for viewing all instructors.

    This route retrieves all instructors from the database and renders the view_instructors.html template.

    Returns:
        str: Rendered template for viewing instructors.
    """
    
    if current_user.user_type != UserType.admin:
        return 'Unauthorized', 403
    
    if request.method == 'POST':
        instructor_id = request.form.get('instructor_id')
        Enrollment.query.filter_by(instructor_id = instructor_id).delete()
        instructor = Instructor.query.filter_by(instructor_id = instructor_id).first()
        if instructor:
            db.session.delete(instructor)
            db.session.commit()
        return redirect(url_for("instructors.view_instructors"))
    
    instructors = Instructor.query.all()
    return render_template(
        'view_instructors.html',
        instructors = instructors,
        get_enum_display = get_enum_display
    ) 


@instructors_blueprint.route("/view_full_instructor_info/<string:instructor_id>")
@login_required 
def view_full_instructor_info(instructor_id):
    """
    Route for viewing detailed information about an instructor.

    This route retrieves the detailed information about the specified instructor from the database and renders the view_full_instructor_info.html template.

    Args:
        instructor_id (str): The ID of the instructor to be viewed.

    Returns:
        str: Rendered template for viewing detailed information about the instructor.
    """
    
    if current_user.user_type != UserType.instructor:
        return 'Unauthorized', 403
    
    instructor = Instructor.query.filter_by(instructor_id=instructor_id).first()

    if not instructor:
        return redirect(url_for('dashboard.instructor_dashboard'))

    return render_template(
        'view_full_instructor_info.html',
        instructor = instructor,
        get_enum_display = get_enum_display
    )


@instructors_blueprint.route("/view_instructor_courses/<string:instructor_id>")
@login_required
def view_instructor_courses(instructor_id):
    """
    Route for viewing courses assigned to an instructor.

    This route retrieves the courses assigned to the specified instructor from the database and renders the view_instructor_courses.html template.

    Args:
        instructor_id (str): The ID of the instructor whose courses are to be viewed.

    Returns:
        str: Rendered template for viewing courses assigned to the instructor.
    """
    
    if current_user.user_type != UserType.instructor:
        return 'Unauthorized', 403
    
    instructor_courses = (
        db.session.query(Course)
        .filter(Course.instructor_id == instructor_id)
        .all()
    )

    instructor = Instructor.query.filter_by(instructor_id = instructor_id).first()

    return render_template(
        'view_instructor_courses.html',
        instructor = instructor,
        instructor_courses = instructor_courses
    )


@instructors_blueprint.route("/view_enrolled_students/<string:course_code>", methods = ['GET', 'POST'])
@login_required
def view_enrolled_students(course_code):
    """
    Route for viewing students enrolled in a course and managing their grades.

    This route allows instructors to view the list of students enrolled in a course, update their grades, and add new grades.
 
    Args:
        course_code (str): The code of the course for which enrolled students are to be viewed.

    Returns:
        str: Rendered template for viewing enrolled students and managing their grades.
    """
    
    if current_user.user_type != UserType.instructor:
        return 'Unauthorized', 403
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        new_grade = request.form.get('grade')

        if new_grade in [g.value for g in Grades]:
            enrollment = Enrollment.query.filter_by(
                student_id=student_id,
                course_code = course_code
            ).first()
            if enrollment:
                grade = Grade.query.filter_by(enrollment_id = enrollment.enrollment_id).first()
                if grade:
                    # Update the grade
                    grade.grade = new_grade
                    db.session.commit()
                else:
                    grade = Grade(enrollment_id = enrollment.enrollment_id, grade = new_grade)
                    db.session.add(grade)
                    db.session.commit()
            
        return redirect(url_for("instructors.view_enrolled_students", course_code = course_code))

    # If it's a GET request
    enrolled_students = (
        db.session.query(
            Student.student_id,
            Student.first_name,
            Student.last_name,
            Student.sex,
            Student.email,
            Student.department_id,
            Department.department_name,
            Student.student_phoneno,
            Grade.grade
        )
        .join(Enrollment, Student.student_id == Enrollment.student_id)
        .outerjoin(Grade, Enrollment.enrollment_id == Grade.enrollment_id)
        .join(Department, Student.department_id == Department.department_id) 
        .filter(Enrollment.course_code == course_code)
        .all()
    )

    grades = Grade.query.all()
    course = Course.query.filter_by(course_code = course_code).first()

    if course:
        course_name = course.course_name
    else:
        return render_template('error.html', message = 'Course not found.')

    return render_template(
        'view_enrolled_students.html',
        enrolled_students = enrolled_students,
        grades = grades,
        course_name = course_name,
        course_code = course_code
    )
