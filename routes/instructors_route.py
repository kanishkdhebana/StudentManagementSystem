from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.instructors import Instructor
from models.users import User, UserType, db
from sqlalchemy.exc import IntegrityError

instructors_blueprint = Blueprint('instructors', __name__)

@instructors_blueprint.route('/')
@login_required
def index():
    return render_template('index.html')

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


    # If the request method is not POST, render the form for adding a student
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

