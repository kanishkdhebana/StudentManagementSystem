from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app.models.users import User
from app.models.users import UserType

# Creating a Blueprint named 'auth' for authentication related routes
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
    """
    Route for handling user login.

    Accepts POST requests with user_id and user_password in the form data.
    If the user exists and the password is correct, logs the user in.
    Redirects to appropriate dashboard based on user type after successful login.
    Displays an error message if login fails.

    Returns:
        Renders the 'login.html' template with error message if login fails,
        otherwise redirects to the appropriate dashboard.
    """
    
    if current_user.is_authenticated:
        if current_user.user_type == UserType.admin:
            return redirect(url_for('dashboard.admin_dashboard'))
        
        elif current_user.user_type == UserType.student:
            return redirect(url_for('dashboard.student_dashboard'))
        
        elif current_user.user_type == UserType.instructor:
            return redirect(url_for('dashboard.instructor_dashboard'))
    
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
    """
    Route for handling user logout.

    Logs the user out and redirects to the login page.

    Returns:
        Redirects to the 'login' route.
    """
    
    logout_user()
    return redirect(url_for("auth.login"))

