# Voice-Based Attendance System

This is a simple voice-based attendance system built with Flask, SQLAlchemy, and Speech Recognition. The system allows students to mark attendance using voice commands, and it includes a teacher portal to enroll courses. Admin users can view attendance records and courses.

## Features
- **User Authentication**: Sign up and log in functionality for different roles (teacher, student, admin).
- **Course Enrollment**: Teachers can enroll courses.
- **Attendance**: Students can mark attendance by saying 'yes' using speech recognition.
- **Admin Dashboard**: Admin users can view attendance records and courses.

## Technologies Used
- **Flask**: Web framework to build the backend.
- **SQLAlchemy**: ORM for database interactions.
- **SpeechRecognition**: Library for handling voice commands.
- **MySQL**: Relational database to store user, course, and attendance data.
- **bcrypt**: For password hashing and security.
- **Flask-Migrate**: For handling database migrations.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/IbrarArif/Voice-based-attendance-system.git
   cd Voice-based-attendance-system
```
Install the required dependencies:

pip install -r requirements.txt

Set up the database. Make sure you have MySQL installed and running. Then, update the SQLALCHEMY_DATABASE_URI in the config.py file to match your database credentials:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yourpassword@localhost/attendance_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

Run the application:

```bash

python app.py

```
The application will be running locally at http://localhost:5000.

Directory Structure
```perl

/Voice-based-attendance-system
├── app.py                # Main Flask app file
├── config.py             # Configuration file for database URL
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates for rendering views
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── enroll_course.html
│   ├── submit_attendance.html
│   └── view_attendance.html
└── models.py            # Contains the models for User, Course, and Attendance

```

License
This project is licensed under the MIT License - see the LICENSE file for details.

Repository Link
https://github.com/IbrarArif/Voice-based-attendance-system.git
