from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.users import UserType
from models.students import Student
from models.instructors import Instructor
from models.courses import Course

dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/admin')
@login_required
def admin_dashboard():
    if current_user.user_type != UserType.admin:
        return 'Unauthorized', 403
    
    return render_template('admin_dashboard.html')  


@dashboard_blueprint.route('/student')
@login_required
def student_dashboard():
    if current_user.user_type != UserType.student:
        return 'Unauthorized', 403
    
    student = Student.query.filter_by(student_id = current_user.user_id).first()
    if student:
        return render_template('student_dashboard.html', student = student)
    else:
        flash('Student data not found', 'error')
        return redirect(url_for('auth.login'))


@dashboard_blueprint.route('/instructor')
@login_required
def instructor_dashboard():
    if current_user.user_type != UserType.instructor:
        return 'Unauthorized', 403
    
    instructor = Instructor.query.filter_by(instructor_id=current_user.user_id).first()
    if instructor:
        # Fetch courses associated with the instructor
        instructor_courses = Course.query.filter_by(instructor_id=current_user.user_id).all()
        return render_template('instructor_dashboard.html', instructor=instructor, instructor_courses=instructor_courses)
    else:
        flash('Instructor data not found', 'error')
        return redirect(url_for('auth.login'))
