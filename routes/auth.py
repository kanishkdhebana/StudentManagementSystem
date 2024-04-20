from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from models.users import User
from models.users import UserType

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_password = request.form['user_password']   
        user = User.query.filter_by(user_id = user_id).first()
        
        if user is not None and user.check_password(user_password):
            login_user(user)

            if user.user_type == UserType.admin:
                return redirect(url_for('dashboard.admin_dashboard'))
            
            elif user.user_type == UserType.student:
                return redirect(url_for('dashboard.student_dashboard'))
            
            elif user.user_type == UserType.instructor:
                return redirect(url_for('dashboard.instructor_dashboard'))
        
        else: 
            error = 'Invalid user ID or password. Please try again.'
            
    return render_template('login.html', error = error)


@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

