"""
Routes for managing courses in the application.

This module defines routes for adding and viewing courses. These routes are accessible only to users with administrative privileges.

Attributes:
    courses_blueprint (flask.Blueprint): Blueprint object for defining course routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from models.users import UserType, db
from models.courses import Course
from models.enrollments import Enrollment 
from models.departments import Department
from models.instructors import Instructor
from sqlalchemy.exc import IntegrityError

# Blueprint object for defining course routes
courses_blueprint = Blueprint('courses', __name__)


@courses_blueprint.route("/add_course", methods = ['GET', 'POST'])
@login_required
def add_course():
    """
    Route for adding a new course.

    This route is accessible only to users with administrative privileges. It handles both GET and POST requests. For POST requests, it adds a new course to the database.

    Returns:
        str: Redirects to the add_course route if the course is successfully added. Renders an error template if an IntegrityError occurs during database operations.
    """
    if current_user.user_type != UserType.admin:
        return 'Unauthorized', 403
    
    departments = Department.query.all()
    
    if request.method == 'POST': 
        course_code   = request.form['course_code']
        course_name   = request.form['course_name']
        instructor_id = request.form['instructor_id']
        department_name = request.form['department_name']
        description   = request.form['description']
        credit_hours  = request.form['credit_hours']
        
        department = Department.query.filter_by(department_name = department_name).first()
        department_id = department.department_id if department else None

        new_course = Course( 
            course_code   = course_code,
            course_name   = course_name,
            instructor_id = instructor_id,
            department_id = department_id,
            description   = description,
            credit_hours  = credit_hours
        ) 

        try:
            db.session.add(new_course)
            db.session.commit()
            return redirect(url_for("courses.add_course"))
        
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig) if e.orig else "An error occurred. Please try again later."
            return render_template("error.html", message = error_message)

    # If the request method is not POST
    return render_template("add_course.html", departments = departments)


@courses_blueprint.route('/view_courses', methods = ['GET', 'POST'])
@login_required
def view_courses():
    """
    Route for viewing all courses.

    This route is accessible only to users with administrative privileges. It retrieves all courses from the database and renders a template to display them.

    Returns:
        str: Rendered template for viewing courses.
    """

    if current_user.user_type != UserType.admin:
        return 'Unauthorized', 403
    
    error_message = None
    
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        existing_enrollments = Enrollment.query.filter_by(course_code = course_code).all()
    
        if existing_enrollments:
            error_message = "Cannot delete course because there are existing enrollments."
            session['error_message'] = error_message
            
        else:
            course = Course.query.filter_by(course_code=course_code).first()
            if course:
                db.session.delete(course)
                db.session.commit()
            
            session['error_message'] = None
            return redirect(url_for("courses.view_courses"))
    
    available_instructors = Instructor.query.all()
    courses_with_department = []
    courses = Course.query.all()
    
    for course in courses:
        department = Department.query.filter_by(department_id = course.department_id).first()
        department_name = department.department_name if department else "Unknown Department"
        courses_with_department.append((course, department_name))

    return render_template(
        'view_courses.html',
        courses_with_department = courses_with_department,
        available_instructors = available_instructors,
        error_message = error_message
    )
    
    
@courses_blueprint.route('/assign_instructor', methods=['POST'])
@login_required
def assign_instructor():
    """
    Route for assigning an instructor to a course.

    This route handles the form submission for assigning an instructor to a course.
    It updates the instructor assigned to the course in the database.

    Returns:
        str: Redirects to the view_courses route after assigning the instructor.
    """
    if current_user.user_type != UserType.admin:
        return 'Unauthorized', 403
    
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        instructor_id = request.form.get('instructor_id')

        course = Course.query.filter_by(course_code = course_code).first()

        if course:
            course.instructor_id = instructor_id
            db.session.commit()
            
    return redirect(url_for("courses.view_courses"))