from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.students import Student
from models.users import User, UserType, db
from sqlalchemy.exc import IntegrityError

students_blueprint = Blueprint('students', __name__)

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
