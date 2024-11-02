"""
Student Management System

This Flask application manages students, instructors, courses, departments, and authentication.

Attributes:
    app (Flask): The Flask application instance.
    login_manager (LoginManager): The Flask-Login manager instance.
"""

from flask import Flask, redirect, url_for
import os
import pymysql
from flask_login import LoginManager
from models.users import User, db as user_db
from routes.students_route import students_blueprint
from routes.instructors_route import instructors_blueprint
from routes.courses_route import courses_blueprint
from routes.auth import auth_blueprint
from routes.departments_route import departments_blueprint
from routes.dashboard import dashboard_blueprint

pymysql.install_as_MySQLdb()

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DATABASE_USER', 'root')}:" \
                                        f"{os.getenv('DATABASE_PASSWORD', '1324')}@" \
                                        f"{os.getenv('DATABASE_HOST', 'db')}/" \
                                        f"{os.getenv('DATABASE_NAME', 'studentmanagementsystem')}"

# 'mysql+pymysql://root:@localhost/StudentManagementSystem?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Initialize SQLAlchemy
user_db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """
    Load a user given the user ID.

    Args:
        user_id (str): The ID of the user to load.

    Returns:
        User: The user object corresponding to the user ID.
    """
    return User.query.get(user_id)

# Register Blueprints
app.register_blueprint(students_blueprint)
app.register_blueprint(courses_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(departments_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(instructors_blueprint)

@app.route('/')
def index():
    """
    Redirect to the login page.

    Returns:
        Redirect: Redirects to the login page.
    """
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
