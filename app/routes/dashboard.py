"""
Routes for different user dashboards in the application.

This module defines routes for the admin, student, and instructor dashboards. Each dashboard displays specific information based on the user type.

Attributes:
    dashboard_blueprint (flask.Blueprint): Blueprint object for defining dashboard routes.
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.users import UserType
from models.students import Student
from models.instructors import Instructor
from models.courses import Course

# Blueprint object for defining dashboard routes
dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/admin')
@login_required
def admin_dashboard():
    """
    Route for displaying the admin dashboard.

    This route is accessible only to users with administrative privileges. It renders the admin_dashboard.html template.

    Returns:
        str: Rendered template for the admin dashboard.
    """
    if current_user.user_type != UserType.admin:
        return 'Unauthorized', 403
    
    return render_template('admin_dashboard.html')  


@dashboard_blueprint.route('/student')
@login_required
def student_dashboard():
    """
    Route for displaying the student dashboard.

    This route is accessible only to users with student privileges. It retrieves the student's data from the database and renders the student_dashboard.html template.

    Returns:
        str: Rendered template for the student dashboard.
    """
    if current_user.user_type != UserType.student:
        return 'Unauthorized', 403
    
    student = Student.query.filter_by(student_id = current_user.user_id).first()
    if student:
        return render_template('student_dashboard.html', student = student)
    else:
        return redirect(url_for('auth.login'))


@dashboard_blueprint.route('/instructor')
@login_required
def instructor_dashboard():
    """
    Route for displaying the instructor dashboard.

    This route is accessible only to users with instructor privileges. It retrieves the instructor's data from the database and renders the instructor_dashboard.html template.

    Returns:
        str: Rendered template for the instructor dashboard.
    """
    if current_user.user_type != UserType.instructor:
        return 'Unauthorized', 403
    
    instructor = Instructor.query.filter_by(instructor_id = current_user.user_id).first()
    if instructor:
        instructor_courses = Course.query.filter_by(instructor_id = current_user.user_id).all()
        return render_template(
            'instructor_dashboard.html',
            instructor = instructor,
            instructor_courses = instructor_courses
        )
    else:
        return redirect(url_for('auth.login'))
