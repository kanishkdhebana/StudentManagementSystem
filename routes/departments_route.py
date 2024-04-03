from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from models.departments import Department, db
from sqlalchemy.exc import IntegrityError

departments_blueprint = Blueprint('departments', __name__)

@departments_blueprint.route("/add_department", methods=['GET', 'POST'])
@login_required
def add_department():
    if request.method == 'POST':
        department_id   = request.form['department_id']
        department_name = request.form['department_name']
        
        new_department = Department(
            department_id   = department_id,
            department_name = department_name,
        ) 

        try:
            db.session.add(new_department)
            db.session.commit()
            
            flash('Department added successfully.', 'success')
            return redirect(url_for("departments.add_department"))
        
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig) if e.orig else "An error occurred. Please try again later."
            return render_template("error.html", message = error_message)

    # If the request method is not POST, render the form for adding a department
    return render_template("add_department.html")

# Pass the mapped values to the template
@departments_blueprint.route('/view_departments')
@login_required
def view_departments():
    departments = Department.query.all()
    return render_template('view_departments.html', departments = departments)

