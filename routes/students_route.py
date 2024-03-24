from flask import Blueprint, render_template, request, redirect, url_for
from models.students import Student, db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required

students_blueprint = Blueprint('students', __name__)

@students_blueprint.route('/')
@login_required
def index():
    return render_template('index.html')

@students_blueprint.route("/add_student", methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        student_id      = request.form['student_id']
        first_name      = request.form['first_name']
        middle_name     = request.form['middle_name']
        last_name       = request.form['last_name']
        sex             = request.form['sex']
        email           = request.form['email']
        degree_name     = request.form['degree_name']
        grad_level      = request.form['grad_level']
        address         = request.form['address']
        city            = request.form['city']
        state           = request.form['state']
        address_pin     = int(request.form['address_pin'])
        father_name     = request.form['father_name']
        mother_name     = request.form['mother_name']
        dob             = request.form['dob']
        bloodgroup      = request.form['bloodgroup'] 
        doa             = request.form['doa']
        father_occ      = request.form['father_occ']
        mother_occ      = request.form['mother_occ']
        student_phoneno = request.form['student_phoneno']
        guardian_phoneno  = request.form['guardian_phoneno']

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
            return redirect(url_for("students.index"))
        
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig) if e.orig else "An error occurred. Please try again later."
            return render_template("error.html", message = error_message)


    # If the request method is not POST, render the form for adding a student
    return render_template("add_student.html")

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
    return render_template('view_students.html', students=students, get_enum_display=get_enum_display)

