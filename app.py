from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/StudentManagementSystem?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'students'  # Specify the table name explicitly
    student_id = db.Column(db.String(11), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)        

    def __repr__(self):
        return f"Student('{self.first_name}', '{self.last_name}')"


# Route to display all students
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Route to add a new student
@app.route('/add', methods=['POST'])
def add_student():
    # Get form data from request
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    
    # Create a new student object
    new_student = Student(first_name=first_name, last_name=last_name)
    
    # Add the new student to the database
    db.session.add(new_student)
    db.session.commit()
    
    # Redirect to the homepage
    return redirect(url_for('index'))

# Route to edit an existing student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    # Retrieve the student from the database
    student = Student.query.get_or_404(id)
    
    if request.method == 'POST':
        # Update student data with form data
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.roll_no = request.form['roll_no']
        student.division = request.form['division']
        
        # Commit changes to the database
        db.session.commit()
        
        # Redirect to the homepage
        return redirect(url_for('index'))
    
    # Render the edit form template
    return render_template('edit.html', student=student)

# Route to delete a student
@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    # Retrieve the student from the database
    student = Student.query.get_or_404(id)
    
    # Delete the student from the database
    db.session.delete(student)
    db.session.commit()
    
    # Redirect to the homepage
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)