from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import speech_recognition as sr
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import bcrypt
import re
import numpy as np
from flask_migrate import Migrate
import io

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize the secret key
app.secret_key = np.random.bytes(32).hex().upper()

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher_name = db.Column(db.String(80), nullable=False)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_name = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(10), nullable=False)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        new_user = User(username=data['username'], password=hashed_password, role=data['role'])
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', error="Username already exists.")
        except SQLAlchemyError as e:
            db.session.rollback()
            return render_template('register.html', error="Database error: " + str(e))
    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        user = User.query.filter_by(username=data["username"]).first()
        if user and bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("ascii")):
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    role = session.get('role')
    return render_template('dashboard.html', role=role)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/enroll_course', methods=['GET', 'POST'])
def enroll_course():
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = request.form
        # Fetch teacher name based on session user_id
        teacher = User.query.filter_by(id=session['user_id']).first()
        if teacher:
            new_course = Course(name=data['course_name'], teacher_id=session['user_id'], teacher_name=teacher.username)
            db.session.add(new_course)
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            return jsonify({"message": "Teacher not found"}), 404
    return render_template('enroll_course.html')


@app.route('/submit_attendance', methods=['GET', 'POST'])
def submit_attendance():
    if 'user_id' not in session or session['role'] != 'student':
        print('Unauthorized access')
        return jsonify({"message": "Unauthorized access"}), 403

    if request.method == 'POST':
        text = request.form.get('text', '').strip().lower()  # Corrected method name
        subject = request.form.get('subject')

        print('Received text:', text)  # Debug log
        print('Subject:', subject)  # Debug log

        # Check if the processed text matches 'yes' or 'yes.'
        if text == 'yes' or text == 'yes.':
            student_id = session.get('user_id')
            student = User.query.filter_by(id=student_id).first()  # Fetch student details
            print('Student ID from session:', student_id)  # Debug log
            if student_id:
                try:
                    new_attendance = Attendance(student_id=student_id, student_name=student.username, subject=subject, status='present')
                    db.session.add(new_attendance)
                    db.session.commit()
                    print('Attendance recorded successfully')  # Debug log
                    return jsonify({"message": "Attendance recorded successfully"}), 201
                except Exception as e:
                    print('Error committing to the database:', e)  # Debug log
                    db.session.rollback()
                    return jsonify({"message": "Database error"}), 500
            print('Student not found in session')  # Debug log
            return jsonify({"message": "Student not found"}), 404
        print('Incorrect speech input')  # Debug log
        return jsonify({"message": "Please say 'yes' to mark attendance"}), 400

    return render_template('submit_attendance.html')




@app.route('/view_attendance')
def view_attendance():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    attendances = Attendance.query.all()
    return render_template('view_attendance.html', attendances=attendances)

@app.route('/view_courses')
def view_courses():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    courses = Course.query.all()
    return render_template('view_courses.html', courses=courses)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
