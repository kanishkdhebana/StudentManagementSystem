from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum as EnumSQL
from enum import Enum

db = SQLAlchemy()

class UserType(Enum):
    admin = 'admin'
    student = 'student'

class User(UserMixin, db.Model):
    __tablename__      = 'users'
    user_id            = db.Column(db.Integer, primary_key = True)
    user_type          = db.Column(EnumSQL(UserType), nullable = False)
    user_password_hash = db.Column(db.String(50), nullable = False)
    
    def set_password(self, password):
        self.user_password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.user_password_hash, password)
    
    def is_authenticated(self):
        # Implement your authentication logic here
        return True  # For demonstration, always return True

    def is_active(self):
        # Implement your active status logic here
        return True  # For demonstration, always return True

    def is_anonymous(self):
        # Implement your anonymous logic here
        return False  # For demonstration, always return False

    def get_id(self):
        # Implement method to return user ID
        return str(self.user_id)

    
