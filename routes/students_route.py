"""
Routes for managing students in the application.

This module defines routes for adding, viewing, editing, and managing students.

Attributes:
    students_blueprint (flask.Blueprint): Blueprint object for defining student routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from models.students import Student, db
from models.users import User, UserType
from models.enrollments import Enrollment
from models.grades import Grade
from models.courses import Course
from models.instructors import Instructor
from models.departments import Department
from sqlalchemy.exc import IntegrityError

students_blueprint = Blueprint('students', __name__)

@students_blueprint.route("/add_student", methods=['GET', 'POST'])
@login_required
def add_student():
    """
    Route for adding a new student.

    This route allows administrators to add a new student by submitting a form. If the form is submitted via POST method, it validates the input and adds the new student to the database.

    Returns:
        str: Rendered template for adding a student or a redirect to the student dashboard.
    """
    if current_user.user_type != UserType.admin:
        return 'Unauthorized', 403
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        department_id = request.form.get('department_id')
        if not department_id:
            return redirect(url_for('students.add_student'))
        
        existing_student = Student.query.filter_by(student_id = student_id).first()
        if existing_student:
            return redirect(url_for('students.add_student'))
          
        first_name       = request.form['first_name']
        middle_name      = request.form['middle_name']
        last_name        = request.form['last_name']
        sex              = request.form['sex']
        email            = request.form['email']
        grad_level       = request.form['grad_level']
        address          = request.form['address']
        city             = request.form['city']
        state            = request.form['state']
        address_pin      = int(request.form['address_pin'])
        father_name      = request.form['father_name']
        mother_name      = request.form['mother_name']
        dob              = request.form['dob']
        bloodgroup       = request.form['bloodgroup'] 
        doa              = request.form['doa']
        father_occ       = request.form['father_occ']
        mother_occ       = request.form['mother_occ']
        student_phoneno  = int(request.form['student_phoneno'])
        guardian_phoneno = int(request.form['guardian_phoneno'])

        new_student = Student(
            student_id       = student_id,
            first_name       = first_name,
            middle_name      = middle_name,
            last_name        = last_name,
            sex              = sex,
            email            = email,
            grad_level       = grad_level,
            address          = address,
            city             = city,
            state            = state,
            address_pin      = address_pin,
            father_name      = father_name,
            mother_name      = mother_name,
            dob              = dob,
            bloodgroup       = bloodgroup,
            doa              = doa,
            father_occ       = father_occ,
            mother_occ       = mother_occ,
            student_phoneno  = student_phoneno,
            guardian_phoneno = guardian_phoneno,
            department_id    = department_id
        ) 

        try:
            db.session.add(new_student) 
            db.session.commit()
            
            user_password = f"{request.form['first_name'].lower()}{request.form['dob'].replace('-', '')}"
            new_user = User(user_id = student_id, user_type = UserType.student)
            new_user.set_password(user_password)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for("students.add_student"))
        
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig) if e.orig else "An error occurred. Please try again later."

    # if not POST
    departments = Department.query.all()
    return render_template("add_student.html", departments = departments)



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
    if enum_value.__class__.__name__ == 'GradLevel':
        grad_level_mapping = {
            'B_Tech': 'B.Tech',
            'M_Tech': 'M.Tech',
            'PHD'   : 'PhD'
        }
        return grad_level_mapping.get(enum_value.value)
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


@students_blueprint.route('/view_students', methods = ['GET', 'POST'])
@login_required
def view_students():
    """
    Route for viewing all students.

    This route retrieves all students from the database and renders the view_students.html template.

    Returns:
        str: Rendered template for viewing students.
    """
    if current_user.user_type != UserType.admin:
        return 'Unauthorized', 403
     
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        
        try:
            with db.session.begin_nested():     
                student = Student.query.filter_by(student_id = student_id).first()
                if student:
                    Enrollment.query.filter_by(student_id = student_id).delete()
                    User.query.filter_by(user_id = student_id).delete()
                    db.session.delete(student)
                    db.session.commit()
                    
        except SQLAlchemyError as e:
            db.session.rollback()
            
        return redirect(url_for("students.view_students"))
      
    students = Student.query.all()
    department_names = {}
    for student in students:
        department = Department.query.filter_by(department_id = student.department_id).first()
        if department:
            department_names[student.student_id] = department.department_name
        else:
            department_names[student.student_id] = "Unknown Department"

    
    return render_template(
        'view_students.html',
        students = students,
        department_names = department_names,
        get_enum_display = get_enum_display
    )


@students_blueprint.route("/edit_student_info/<string:student_id>", methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    """
    Route for editing student information.

    This route allows administrators to edit student information. If the form is submitted via POST method, it updates the student information in the database.

    Args:
        student_id (str): The ID of the student to be edited.

    Returns:
        str: Rendered template for editing student information or a redirect to the student dashboard.
    """
    
    if current_user.user_type != UserType.student or current_user.user_id != student_id:
        return 'Unauthorized', 403
    
    if request.method == 'POST':
        student = Student.query.filter_by(student_id = student_id).first()
        
        # Validate phone numbers
        if not is_valid_phone_number(request.form['student_phoneno']) or not is_valid_phone_number(request.form['guardian_phoneno']):
            return redirect(url_for('students.edit_student', student_id = student_id))

        student.email = request.form['email']
        student.student_phoneno = request.form['student_phoneno']
        student.guardian_phoneno = request.form['guardian_phoneno']

        db.session.commit()

        return redirect(url_for('dashboard.student_dashboard'))

    student = Student.query.filter_by(student_id = student_id).first()
    return render_template('edit_student_info.html', student = student)

def is_valid_phone_number(phone_number):
    """
    Check if the phone number consists of exactly 10 digits.

    Args:
        phone_number (str): Phone number to validate.

    Returns:
        bool: True if the phone number consists of exactly 10 digits, False otherwise.
    """
    return len(phone_number) == 10 and phone_number.isdigit()
    

@students_blueprint.route("/view_full_student_info/<string:student_id>")
@login_required
def view_full_student_info(student_id):
    """
    Route for viewing detailed information about a student.

    This route retrieves the detailed information about the specified student from the database and renders the view_full_student_info.html template.

    Args:
        student_id (str): The ID of the student whose information is to be viewed.

    Returns:
        str: Rendered template for viewing detailed student information or a redirect to the student dashboard.
    """
    
    if current_user.user_type != UserType.student or current_user.user_id != student_id:
        return 'Unauthorized', 403
    
    student = Student.query.filter_by(student_id = student_id).first()
    department = Department.query.filter_by(department_id=student.department_id).first()
    department_name = department.department_name if department else "Unknown Department"
    
    if not student:
        return redirect(url_for('dashboard.student_dashboard'))

    return render_template('view_full_student_info.html', student = student, department_name = department_name)


@students_blueprint.route("/view_student_enrollments/<string:student_id>")
@login_required
def view_student_enrollments(student_id):
    """
    Route for viewing a student's course enrollments.

    This route retrieves all course enrollments of the specified student from the database and renders the view_student_enrollments.html template.

    Args:
        student_id (str): The ID of the student whose enrollments are to be viewed.

    Returns:
        str: Rendered template for viewing student enrollments.
    """
    
    if current_user.user_type != UserType.student or current_user.user_id != student_id:
        return 'Unauthorized', 403
    
    student_enrollments = Enrollment.query.filter_by(student_id = student_id).all()
    enrollment_details = []
    
    for enrollment in student_enrollments:
        joined_data = db.session.query(
            Enrollment,
            Course,
            Instructor
        ).join(
            Course,
            Enrollment.course_code == Course.course_code
        ).join(
            Instructor,
            Course.instructor_id == Instructor.instructor_id
        ).filter(
            Enrollment.student_id == student_id,
            Enrollment.course_code == enrollment.course_code
        ).first()

        if joined_data:
            course_name = joined_data.Course.course_name
            instructor_name = joined_data.Instructor.first_name + ' ' + joined_data.Instructor.last_name

            enrollment_details.append({
                'course_name': course_name,
                'instructor_name': instructor_name,
                'course_code': enrollment.course_code,
                'enrollment_date': enrollment.enrollment_date
            })
    
    return render_template("view_student_enrollments.html", enrollment_details = enrollment_details)


@students_blueprint.route("/view_student_grades/<string:student_id>")
@login_required
def view_student_grades(student_id):
    """
    Route for viewing a student's grades.

    This route retrieves all grades of the specified student from the database and renders the view_student_grades.html template.

    Args:
        student_id (str): The ID of the student whose grades are to be viewed.

    Returns:
        str: Rendered template for viewing student grades.
    """
    
    if current_user.user_type != UserType.student or current_user.user_id != student_id:
        return 'Unauthorized', 403
    
    student_grades = (
        db.session.query(Grade, Course.course_name, Course.course_code)
        .join(Enrollment, Grade.enrollment_id == Enrollment.enrollment_id)
        .join(Course, Enrollment.course_code == Course.course_code)  
        .filter(Enrollment.student_id == student_id)
        .all()
    )

    return render_template("view_student_grades.html", student_grades = student_grades)


@students_blueprint.route("/enroll_course", methods=['GET', 'POST'])
@login_required
def enroll_course():
    """
    Route for enrolling in a course.

    This route allows students to enroll in a course. If the form is submitted via POST method, it validates the input and adds the enrollment record to the database.

    Returns:
        str: Rendered template for enrolling in a course or a redirect to the student dashboard.
    """
    
    if current_user.user_type != UserType.student:
        return 'Unauthorized', 403
    
    student_id = current_user.user_id
    
    if request.method == 'POST':
        course_code = request.form['course_code']
        
        existing_enrollment = Enrollment.query.filter_by(
            student_id = student_id,
            course_code = course_code
            ).first()
        if existing_enrollment:
            return redirect(url_for('students.enroll_course'))
        
        new_enrollment = Enrollment(
            student_id = student_id,    
            course_code = course_code,
            enrollment_date = datetime.now()  
        )
        
        try:
            db.session.add(new_enrollment)
            db.session.commit()    
            return redirect(url_for('dashboard.student_dashboard'))  
        
        except IntegrityError:
            db.session.rollback()
    
    student_department_id = Student.query.filter_by(student_id = student_id).first().department_id
    available_courses = Course.query.filter_by(department_id = student_department_id).all()
    
    for course in available_courses:
        instructor = Instructor.query.filter_by(instructor_id = course.instructor_id).first()
        if instructor:
            course.instructor_name = instructor.first_name + ' ' +  instructor.last_name
    
    return render_template("enroll_in_course.html", available_courses = available_courses)
