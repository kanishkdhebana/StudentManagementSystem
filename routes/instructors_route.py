from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.instructors import Instructor, db
from models.users import User, UserType
from models.students import Student
from models.enrollments import Enrollment
from models.courses import Course
from sqlalchemy.exc import IntegrityError

instructors_blueprint = Blueprint('instructors', __name__)

@instructors_blueprint.route("/add_instructor", methods=['GET', 'POST'])
@login_required
def add_instructor():
    if current_user.user_type != UserType.admin:
        flash('You are not authorized to perform this action.', 'error')
        return redirect(url_for('users.login'))
    
    if request.method == 'POST':
        instructor_id = request.form['instructor_id']
        
        existing_instructor = Instructor.query.filter_by(instructor_id = instructor_id).first()
        if existing_instructor:
            flash('Instructor already exists', 'error')
            return redirect(url_for('instructors.add_instructor'))
        
        first_name   = request.form['first_name']
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
            
            flash('Instructor added successfully.', 'success')
            return redirect(url_for("dashboard.admin_dashboard"))
        
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig) if e.orig else "An error occurred. Please try again later."
            return render_template("error.html", message = error_message)

    return render_template("add_instructor.html")


# Define a mapping function for enum values
def get_enum_display(enum_value):
    if enum_value is None:
        return None

    elif enum_value.__class__.__name__ == 'BloodGroup':
        blood_group_mapping = {
            'A_plus': 'A+',
            'A_minus': 'A-',
            'B_plus': 'B+',
            'B_minus': 'B-',
            'AB_plus': 'AB+',
            'AB_minus': 'AB-',
            'O_plus': 'O+',
            'O_minus': 'O-'
        }
        
        return blood_group_mapping.get(enum_value.value)
    
    return str(enum_value).replace('_', ' ')

# Pass the mapped values to the template
@instructors_blueprint.route('/view_instructors')
@login_required
def view_instructors():
    instructors = Instructor.query.all()
    return render_template('view_instructors.html', instructors = instructors, get_enum_display = get_enum_display)


@instructors_blueprint.route("/view_full_instructor_info/<string:instructor_id>")
@login_required
def view_full_instructor_info(instructor_id):
    # Retrieve the instructor object from the database
    instructor = Instructor.query.filter_by(instructor_id = instructor_id).first()

    if not instructor:
        flash('Instructor not found.', 'error')
        return redirect(url_for('dashboard.instructor_dashboard'))

    return render_template('view_full_instructor_info.html', instructor = instructor, get_enum_display = get_enum_display)


@instructors_blueprint.route("/view_instructor_courses/<string:instructor_id>")
@login_required
def view_instructor_courses(instructor_id):
    instructor_courses = (
        db.session.query(Course)
        .filter(Course.instructor_id == instructor_id)
        .all()
    )

    return render_template('instructor_dashboard.html', instructor_courses = instructor_courses)


@instructors_blueprint.route("/view_enrolled_students/<string:course_code>")
@login_required
def view_enrolled_students(course_code):
    enrolled_students = (
        db.session.query(Student.student_id, Student.first_name, Student.last_name)
        .join(Enrollment, Student.student_id == Enrollment.student_id)
        .filter(Enrollment.course_code == course_code)
        .all()
    )

    course = Course.query.filter_by(course_code = course_code).first()
    
    if course:
        course_name = course.course_name
        
    else:
        # Redirect to an error page or handle the situation as needed
        return render_template('error.html', message = 'Course not found.')

    # Render the template with enrolled students and course name
    return render_template('enrolled_students.html', enrolled_students = enrolled_students, course_name = course_name, course_code = course_code)


