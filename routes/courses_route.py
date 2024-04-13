"""
Routes for managing courses in the application.

This module defines routes for adding and viewing courses. These routes are accessible only to users with administrative privileges.

Attributes:
    courses_blueprint (flask.Blueprint): Blueprint object for defining course routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.users import UserType
from models.courses import Course, db
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
    
    if request.method == 'POST': 
        course_code   = request.form['course_code']
        course_name   = request.form['course_name']
        instructor_id = request.form['instructor_id']
        department_id = request.form['department_id']
        description   = request.form['description']
        credit_hours  = request.form['credit_hours']

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
            return render_template("error.html", message=error_message)

    # If the request method is not POST, render the form for adding a course
    return render_template("add_course.html")


@courses_blueprint.route('/view_courses')
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
    
    courses = Course.query.all()
    return render_template('view_courses.html', courses = courses)
