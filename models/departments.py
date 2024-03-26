from flask_sqlalchemy import SQLAlchemy
from models.users import db

class Department(db.Model):
    __tablename__   = 'departments'
    department_id   = db.Column(db.String(11), primary_key = True)
    department_name = db.Column(db.String(100), nullable = False)

    def __repr__(self) -> str:
        return f"{self.department_name}"
