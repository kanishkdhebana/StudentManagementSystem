from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from models.users import db, User

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/')
def index():
    return render_template('index.html')

@auth_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_password = request.form['user_password']
        user = User.query.filter_by(user_id = user_id).first()
        
        if user is not None and user.check_password(user_password):
            login_user(user)
            flash("Welcome")
            return redirect(url_for('auth.index'))
        
        else:
            flash('Invalid ID/Password', 'error')
            
    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    flash("Logged out successfully!!")
    return redirect(url_for("auth.login"))

@auth_blueprint.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_type = request.form['user_type']
        user_password = request.form['user_password']
        
        # check if user already exists
        existing_user = User.query.filter(User.user_id == user_id).first()
        if existing_user:
            flash('User already exists')
            return redirect(url_for('auth.register'))
        
        # create new user
        new_user = User(user_id = user_id, user_type = user_type)
        new_user.set_password(user_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration Successful. Please Login.')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')