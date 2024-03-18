from flask import Flask
from routes.students_route import students_blueprint
from routes.courses_route import courses_blueprint
from models.students import db

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(students_blueprint)
app.register_blueprint(courses_blueprint)


# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/StudentManagementSystem?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
