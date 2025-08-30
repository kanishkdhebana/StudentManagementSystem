# Student Management System

A web-based Student Management System built with Flask and MariaDB. The system supports three roles (Admin, Instructor, Student) with separate dashboards and permissions.  

The system has been tested in a production-like setup on AWS (EC2 + RDS + Nginx). While not currently hosted to avoid costs, the deployment was validated with load testing (~100 concurrent users on t2.micro).

---

## Features

- **Role-Based Access Control** — Admin, Instructor, and Student dashboards  
- **Student Records** — Add, view, update, and delete student details  
- **Course & Grade Management** — Enrollments and grade tracking  
- **Custom Views** — Dashboards tailored to each user role  
- **Dockerized Deployment** — Run locally with Docker Compose, optionally deploy to AWS

## Architecture

```mermaid
%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'background': '#1a1b26',
      'primaryColor': '#1a1b26',
      'primaryTextColor': '#a9b1d6',
      'primaryBorderColor': '#414868',
      'lineColor': '#414868',
      'fontFamily': 'sans-serif',
      'fontSize': '16px'
    }
  }
}%%
graph TD
    %% Node Definitions (with trailing spaces for padding)
    User([User&nbsp;]) -->|HTTP : 80 &nbsp;| Nginx80["NGINX (Port 80) &nbsp;"]
    Nginx80 -->|301 Redirect &nbsp;| Nginx443["NGINX (Port 443, SSL Termination) &nbsp;"]
    User  -->|HTTPS : 443 &nbsp;| Nginx443

    %% Reverse Proxy Link
    Nginx443 -->|Forward : 5001 &nbsp;| FlaskApp["Flask App (Gunicorn, Docker, EC2) &nbsp;"]

    %% DB Communication Link
    FlaskApp -->|SQL Queries &nbsp;| RDS["AWS RDS (MariaDB) &nbsp; &nbsp;"]

    %% Styling with Classes for a handcrafted, dark-theme look
    classDef user fill:#7aa2f7,stroke:#293b58,stroke-width:2px,color:#0e0e11
    classDef proxy fill:#bb9af7,stroke:#4b3d63,stroke-width:2px,color:#0e0e11
    classDef application fill:#e0af68,stroke:#5e482b,stroke-width:2px,color:#0e0e11
    classDef database fill:#73daca,stroke:#315c55,stroke-width:2px,color:#0e0e11

    %% Apply Classes to Nodes
    class User user
    class Nginx80,Nginx443 proxy
    class FlaskApp application
    class RDS database

```

---

## Technologies

- **Flask** — Backend framework  
- **MariaDB** — Database (local via Docker, or RDS in AWS deployment)  
- **Docker & Docker Compose** — Containerization and orchestration  
- **Nginx** — Reverse proxy (used in AWS deployment)  
- **SQLAlchemy** — ORM for database access  
- **Locust & Gunicorn** — Load testing and production server testing  

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

## Cloud Deployment (Optional, Tested)

Although not hosted live due to cost, this system has been deployed and tested on AWS with:

- EC2 for containerized app hosting

- RDS (MariaDB) for managed database

- Nginx as a reverse proxy

- Locust load testing showing stable performance up to ~100 concurrent users on t2.micro

## How to Use It

Once you log in, your dashboard will change based on your role:

* **Admin:** Manage all students, instructors, courses, and system settings.
* **Instructor:** View and update student grades, track progress, and communicate with students.
* **Student:** Sign up for courses, check your grades, and update your personal information.
