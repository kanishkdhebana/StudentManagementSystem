from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Enum as EnumSQL
from sqlalchemy import Date
from enum import Enum


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/StudentManagementSystem?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Sex(Enum):
    Male = 'Male'
    Female = 'Female'
    Other = 'Other'

class GradLevel(Enum):
    B_Tech = 'B_Tech'
    M_Tech = 'M_Tech'
    PHD = 'PHD'
    
class BloodGroup(Enum):
    A_plus = "A+"
    A_minus = "A-"
    B_plus = "B+"
    B_minus = "B-"
    AB_plus = "AB+"
    AB_minus = "AB-"
    O_plus = "O+"
    O_minus = "O-"

class Student(db.Model):
    __tablename__ = 'students'
    student_id       = db.Column(db.String(11), primary_key = True)
    first_name       = db.Column(db.String(45), nullable = False)
    middle_name      = db.Column(db.String(45), nullable = True)
    last_name        = db.Column(db.String(45), nullable = False)
    sex              = db.Column(EnumSQL(Sex), nullable = False)
    email            = db.Column(db.String(50), nullable = False)
    degree_name      = db.Column(db.String(100), nullable = False)
    grad_level       = db.Column(EnumSQL(GradLevel), nullable = False)
    address          = db.Column(db.String(400), nullable = False)
    city             = db.Column(db.String(50), nullable = False)
    state            = db.Column(db.String(50), nullable = False)
    address_pin      = db.Column(db.Integer, nullable = False)
    father_name      = db.Column(db.String(100), nullable = False)
    mother_name      = db.Column(db.String(100), nullable = False)
    dob              = db.Column(Date, nullable = False)
    bloodgroup       = db.Column(EnumSQL(BloodGroup), nullable = False)
    doa              = db.Column(Date, nullable = False)
    father_occ       = db.Column(db.String(100), nullable = False)
    mother_occ       = db.Column(db.String(100), nullable = False)
    student_phoneno  = db.Column(db.BigInteger, nullable = False)
    guardian_phoneno = db.Column(db.BigInteger, nullable = False)
    
    def __repr__(self) -> str:
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    
    
    
# Route to display all students
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/add_student", methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_id      = request.form['student_id']
        first_name      = request.form['first_name']
        middle_name     = request.form['middle_name']
        last_name       = request.form['last_name']
        sex             = request.form['sex']
        email           = request.form['email']
        degree_name     = request.form['degree_name']
        grad_level      = request.form['grad_level']
        address         = request.form['address']
        city            = request.form['city']
        state           = request.form['state']
        address_pin     = int(request.form['address_pin'])
        father_name     = request.form['father_name']
        mother_name     = request.form['mother_name']
        dob             = request.form['dob']
        bloodgroup      = request.form['bloodgroup'] 
        doa             = request.form['doa']
        father_occ      = request.form['father_occ']
        mother_occ      = request.form['mother_occ']
        student_phoneno = request.form['student_phoneno']
        guardian_phoneno  = request.form['guardian_phoneno']

        new_student = Student(
            student_id      = student_id,
            first_name      = first_name,
            middle_name     = middle_name,
            last_name       = last_name,
            sex             = sex,
            email           = email,
            degree_name     = degree_name,
            grad_level      = grad_level,
            address         = address,
            city            = city,
            state           = state,
            address_pin     = address_pin,
            father_name     = father_name,
            mother_name     = mother_name,
            dob             = dob,
            bloodgroup      = bloodgroup,
            doa             = doa,
            father_occ      = father_occ,
            mother_occ      = mother_occ,
            student_phoneno = student_phoneno,
            guardian_phoneno  = guardian_phoneno
        ) 

        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for("index"))
        
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig) if e.orig else "An error occurred. Please try again later."
            return render_template("error.html", message=error_message)


    # If the request method is not POST, render the form for adding a student
    return render_template("add_student.html")

    
@app.route('/students')
def view_students():
    students = Student.query.all()          
    return render_template('students.html', students = students)
    
    
if __name__ == '__main__':
    app.run(debug=True)