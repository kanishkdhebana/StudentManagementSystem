from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models.courses import Course, db
from models.departments import Department
from sqlalchemy.exc import IntegrityError

courses_blueprint = Blueprint('courses', __name__)

@courses_blueprint.route("/add_course", methods=['GET', 'POST'])
@login_required
def add_course():
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
            return render_template("error.html", message = error_message)

    # If the request method is not POST, render the form for adding a course
    return render_template("add_course.html")


# Pass the mapped values to the template
@courses_blueprint.route('/view_courses')
@login_required
def view_courses():
    courses = Course.query.all()
    return render_template('view_courses.html', courses = courses)

