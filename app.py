from flask import Flask
from models.students import db
from routes.students_route import app as students_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/StudentManagementSystem?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Register routes from students_route.py
app.register_blueprint(students_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
