"""
Routes for managing departments in the application.

This module defines routes for adding and viewing departments.

Attributes:
    departments_blueprint (flask.Blueprint): Blueprint object for defining department routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from models.users import UserType
from models.departments import Department, db
from models.enrollments import Enrollment
from models.students import Student
from models.courses import Course
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc

departments_blueprint = Blueprint('departments', __name__)

@departments_blueprint.route("/add_department", methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Route for adding a new department.

    This route allows administrators to add a new department by submitting a form. If the form is submitted via POST method, it validates the input and adds the new department to the database.

    Returns:
        str: Rendered template for adding a department or a redirect to the add_department route.
    """
    if current_user.user_type != UserType.admin:
        return 'Unauthorized', 403
    
    if request.method == 'POST':
        department_id = request.form['department_id']
        department_name = request.form['department_name']
        
        existing_department = Department.query.filter_by(department_id = department_id).first()
        if existing_department:
            return redirect(url_for('departments.add_department'))
        
        new_department = Department(
            department_id = department_id,
            department_name = department_name,
        ) 

        try:
            db.session.add(new_department)
            db.session.commit()
            
            return redirect(url_for("departments.add_department"))
        
        except IntegrityError as e:
            db.session.rollback() 
            error_message = str(e.orig) if e.orig else "An error occurred. Please try again later."
            return render_template("error.html", message = error_message)

    return render_template("add_department.html")


@departments_blueprint.route('/view_departments', methods=['GET', 'POST'])
@login_required
def view_departments():
    """
    Route for viewing all departments.

    This route retrieves all departments from the database and renders the view_departments.html template.

    Returns:
        str: Rendered template for viewing departments.
    """
    
    if current_user.user_type != UserType.admin:
        return 'Unauthorized', 403
    
    error_message = None
    if request.method == 'POST':
        department_id = request.form.get('department_id')
        associated_students = Student.query.filter_by(department_id = department_id).all()
        associated_courses = Course.query.filter_by(department_id = department_id).all()

        if associated_students or associated_courses:
            error_message = "Cannot delete department because there are associated students or courses."
            session['error_message'] = error_message
             
        else:
            Enrollment.query.filter_by(department_id = department_id).delete()
            department = Department.query.filter_by(department_id=department_id).first()
            if department:
                db.session.delete(department)
                db.session.commit()
                
            session.pop('error_message', None)
            return redirect(url_for("departments.view_departments"))
        
    departments = Department.query.order_by(asc(Department.department_id)).all()
    return render_template(
        'view_departments.html', 
        departments = departments, 
        error_message = session.pop('error_message', None)
    )

