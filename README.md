# Student Management System

This project is a web-based **Student Management System** that lets users manage student information, courses, and grades. It's built with **Flask** for the backend and **HTML, CSS, and JavaScript** for the frontend.

---

## What It Does

* **Student Records:** Easily add, view, change, and remove student details.
* **Course & Grade Management:** View students enrolled in courses and update their grades.
* **User Roles:** Different levels of access for administrators, students, and instructors.
* **Custom Views:** Separate dashboards for each user type.

---

## Technologies Used

* **Flask:** A Python tool for building the web server.
* **HTML:** For structuring the web pages.
* **CSS:** For styling how the web pages look.
* **JavaScript:** For interactive elements on the web pages.
* **SQLAlchemy:** A Python library that helps the Flask app talk to the database.
* **Docker:** Used to package the application and its database, making it easy to run.

---

## How to Set It Up (Localhost)

Follow these steps to get the system running on your computer:

1.  **Get the Code:**
    ```bash
    git clone https://github.com/kanishkdhebana1/StudentManagementSystem
    cd StudentManagementSystem
    ```

2.  **Install Docker:**
    * **macOS and Windows:** Download and install Docker Desktop.
    * **Linux:**
        ```bash
        sudo apt update
        sudo apt install docker.io docker-compose
        ```

3.  **Run the Application:**
    ```bash
    docker-compose up --build
    ```
    This command will build and start the system using Docker. It sets up the Flask server and a MariaDB database, connecting them automatically.

4.  **Access the System:**
    * Open your web browser and go to: `http://localhost:5000`
    * Log in with your credentials to see your dashboard.

---

## How to Use It

Once you log in, your dashboard will change based on your role:

* **Admin:** Manage all students, instructors, courses, and system settings.
* **Instructor:** View and update student grades, track progress, and communicate with students.
* **Student:** Sign up for courses, check your grades, and update your personal information.
