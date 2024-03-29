from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.students import Student, db
from models.users import User, UserType
from models.enrollments import Enrollment
from models.grades import Grade
from models.courses import Course
from sqlalchemy.exc import IntegrityError

students_blueprint = Blueprint('students', __name__)

""" Add Student """
@students_blueprint.route("/add_student", methods=['GET', 'POST'])
@login_required
def add_student():
    if current_user.user_type != UserType.admin:
        flash('You are not authorized to perform this action.', 'error')
        return redirect(url_for('users.login'))
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        
        existing_student = Student.query.filter_by(student_id=student_id).first()
        if existing_student:
            flash('Student already exists', 'error')
            return redirect(url_for('students.add_student'))
          
        first_name       = request.form['first_name']
        middle_name      = request.form['middle_name']
        last_name        = request.form['last_name']
        sex              = request.form['sex']
        email            = request.form['email']
        degree_name      = request.form['degree_name']
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
        student_phoneno  = request.form['student_phoneno']
        guardian_phoneno = request.form['guardian_phoneno']

        new_student = Student(
            student_id      = student_id,
            first_name      = first_name,
            middle_name     = middle_name,
            last_name       = last_name,
            sex             = sex,
            email           = email,
            degree_name     = degree_name,
            grad_level      = grad_level,
            address         = address,
            city            = city,
            state           = state,
            address_pin     = address_pin,
            father_name     = father_name,
            mother_name     = mother_name,
            dob             = dob,
            bloodgroup      = bloodgroup,
            doa             = doa,
            father_occ      = father_occ,
            mother_occ      = mother_occ,
            student_phoneno = student_phoneno,
            guardian_phoneno  = guardian_phoneno
        ) 

        try:
            db.session.add(new_student) 
            db.session.commit()
            
            user_password = f"{request.form['first_name'].lower()}{request.form['dob'].replace('-', '')}"
            new_user = User(user_id = student_id, user_type = UserType.student)
            new_user.set_password(user_password)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Student added successfully.', 'success')
            return redirect(url_for("students.add_student"))
        
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig) if e.orig else "An error occurred. Please try again later."
            flash(error_message, 'error')

    # If the request method is not POST, render the form for adding a student
    return render_template("add_student.html")


""" View Students """
# Define a mapping function for enum values
def get_enum_display(enum_value):
    if enum_value is None:
        return None
    if enum_value.__class__.__name__ == 'GradLevel':
        grad_level_mapping = {
            'B_Tech': 'B.Tech',
            'M_Tech': 'M.Tech',
            'PHD': 'PhD'
        }
        return grad_level_mapping.get(enum_value.value)
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
@students_blueprint.route('/view_students')
@login_required
def view_students():
    students = Student.query.all()
    return render_template('view_students.html', students = students, get_enum_display = get_enum_display)


""" Edit Student Information """
@students_blueprint.route("/edit_student_info/<string:student_id>", methods = ['GET', 'POST'])
@login_required
def edit_student(student_id):
    if request.method == 'POST':
        # Retrieve the student object from the database
        student = Student.query.filter_by(student_id = student_id).first()

        # Update student information with form data

        student.email = request.form['email']
        student.student_phoneno = request.form['student_phoneno']
        student.guardian_phoneno = request.form['guardian_phoneno']
        # Update other fields as needed

        # Commit changes to the database
        db.session.commit()

        flash('Student information updated successfully.', 'success')
        return redirect(url_for('dashboard.student_dashboard'))

    student = Student.query.filter_by(student_id = student_id).first()
    return render_template('edit_student_info.html', student=student)


""" View Student Information"""
@students_blueprint.route("/view_full_student_info/<string:student_id>")
@login_required
def view_full_student_info(student_id):
    # Retrieve the student object from the database
    student = Student.query.filter_by(student_id=student_id).first()

    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('dashboard.student_dashboard'))

    return render_template('view_full_student_info.html', student = student)


""" View Student Enrollments"""
@students_blueprint.route("/view_student_enrollments/<string:student_id>")
@login_required
def view_student_enrollments(student_id):
    student_enrollments = Enrollment.query.filter_by(student_id = student_id).all()
    
    return render_template("view_student_enrollments.html", student_enrollments = student_enrollments)


""" View Student Grades"""
@students_blueprint.route("/view_student_grades/<string:student_id>")
@login_required
def view_student_grades(student_id):
    student_grades = (
        db.session.query(Grade, Course.course_name)
        .join(Enrollment, Grade.enrollment_id == Enrollment.enrollment_id)
        .join(Course, Enrollment.course_id == Course.course_id)  
        .filter(Enrollment.student_id == student_id)
        .all()
    )

    return render_template("view_student_grades.html", student_grades = student_grades)



