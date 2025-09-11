# 🏥 Hospital Management System (HMS)
### 📋 Project Overview

The Hospital Management System (HMS) is a web-based application designed to streamline and automate hospital operations. It provides separate portals for Admin, Doctors, Patients, and Pharmacy Staff to manage appointments, prescriptions, and medicine dispensing efficiently.

This project is built using Python Flask as the backend framework, and SQLite as the database.

⚡ Features

Multi-role Authentication (Admin, Doctor, Patient, Pharmacy).

Patient Registration and Appointment Booking.

Doctor Dashboard: View & update appointments, prescribe medicines.

Admin Dashboard: Manage and delete appointments.

Pharmacy Dashboard: View prescriptions and patient details.

Secure Login & Session Management.

Simple and user-friendly web interface (HTML/CSS with Jinja2).

💻 Technologies Used

Backend: Python 3.x, Flask

Database: SQLite

Frontend: HTML, CSS, Jinja2 Templates

Tools: Flask Development Server

🚀 Setup Instructions
1️⃣ Prerequisites

Python 3.x installed

pip (Python package installer)

2️⃣ Clone the Repository
```git clone https://github.com/yourusername/hospital-management-system.git```
```cd hospital-management-system ```

3️⃣ Install Dependencies
```pip install -r requirements.txt```

4️⃣ Database Initialization

The project uses a pre-configured SQLite database.
The following tables exist:

Admins

Doctors

Patients

Appointments

Prescriptions

5️⃣ Running the Application
`python app.py`


Then open your browser and go to:

```http://127.0.0.1:5000/```

✅ Default Credentials

Pharmacy Account

Username: pharmacy

Password: pharmacy123

Other accounts (Admin, Doctor, Patient) must be created through the registration system or pre-configured in the database.

⚙️ System Architecture

Client-Server Architecture:

Frontend: HTML/CSS (Jinja2 templates)

Backend: Flask handles routing, session management, and business logic

Database: SQLite stores all user, appointment, and prescription data
