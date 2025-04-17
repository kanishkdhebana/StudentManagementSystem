# Student Management System

This project is a web-based Student Management System developed using Flask, HTML, CSS, and JavaScript. It allows administrators to manage student information such as enrollment, grades, and personal details.

## Features

- Student Management: Add, view, edit, and delete student records.
- Course Management: View enrolled students in courses and manage their grades.
- Role-Based Access Control: Authentication and authorization system with distinct roles for admins, students, and instructors.
- Dashboards: Separate dashboard views for administrators, students, and instructors.
- Responsive Design: Accessible and functional across devices of various screen sizes.

## Technologies Used

- Flask: Python web framework for backend development.
- HTML: Markup language for structuring web pages.
- CSS: Stylesheet language for styling web pages.
- JavaScript: For front-end interactivity.
- SQLAlchemy: Python SQL toolkit and Object-Relational Mapping (ORM) library.
- Docker: For containerizing the application for easy deployment.

## Project Set-up on Localhost

1. Clone the repository:
   ```bash
   git clone https://github.com/kanishkdhebana/StudentManagementSystem
   cd StudentManagementSystem
   ```

2. Install Docker (if not already installed):

   - For macOS and Windows, download Docker Desktop.
   - On Linux:
   
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose

   ```

3. Run the application:
    ```bash
    docker-compose up --build
    ```

    This command will build and start the application in Docker containers. The backend Flask server and the database (MariaDB) will be containerized and networked for seamless integration.

4. Access the application:

   - Open a web browser and go to http://localhost:5000.
   - Log in with your credentials to access your dashboard.

## Usage

Once logged in, use the platform to manage student records, view dashboard statistics, and navigate between different functionalities based on your role:
- Admin: Manage students, instructors, courses, and other settings.
- Instructor: View and update student grades, track progress, and communicate with students.
- Student: Register for courses, view grades, and update personal information.
