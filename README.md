# Student Management System

This project is a web-based Student Management System developed using Flask, HTML, CSS, and JavaScript. It allows administrators to manage student information such as enrollment, grades, and personal details.

## Features

- Add, view, edit, and delete student records
- View enrolled students in courses and manage their grades
- Authentication and authorization system for different user roles (admin, student, instructor)
- Dashboard views for administrators, students and instructors
- Responsive design for seamless usage across devices

## Technologies Used

- Flask: Python web framework for backend development
- HTML: Markup language for creating web pages
- CSS: Stylesheet language for styling web pages
- JavaScript: Programming language for frontend interactivity
- SQLAlchemy: Python SQL toolkit and Object-Relational Mapping (ORM) library

## Project Set-up

1. Clone the repository:
   ```bash
    git clone https://github.com/kanishkdhebana/StudentManagementSystem
   ```

2. Install dependencies: 
    - First create a python virtual environment
    - After activating the virtual environment
        ```bash
        pip install pymysql
        pip install flask
        pip install flask-login
        pip install flask_sqlalchemy
        pip install SQLAlchemy
        ```

3. Set up the database:

   - If you have a MySQL database server installed locally, you can import the database schema and data from the provided .sql file(in SQL directory). Here's how:

     ```bash
     mysql -u username -p database_name < StudentManagementSystem.sql
     ```

   - Replace `username` with your MySQL username, `database_name` with the name of the database you want to import the data into, and `database.sql` with the path to your .sql file.

4. Run the application:
    ```bash
    python3 app.py
    ```

## Usage

1. Navigate to `http://localhost:5000` in your web browser.
2. Log in with your credentials.
3. Use the provided functionality to manage student records, view dashboards, and perform other tasks.

