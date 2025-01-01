from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('user', 'admin'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    job_type = db.Column(db.String(20), nullable=False)  # full-time, part-time, contract
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship with User (if needed)
    user = db.relationship('User', backref=db.backref('jobs', lazy=True))

    def __init__(self, title, description, job_type, location, salary, deadline, created_by):
        self.title = title
        self.description = description
        self.job_type = job_type
        self.location = location
        self.salary = salary
        self.deadline = deadline
        self.created_by = created_by


class ResumeCertification(db.Model):
    __tablename__ = 'resume_certifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_path = db.Column(db.String(255), nullable=True)  # Path to the resume file
    certification_path = db.Column(db.String(255), nullable=True)  # Path to the certification file
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Upload timestamp

    user = db.relationship('User', backref=db.backref('resume_certifications', lazy=True))

    def __repr__(self):
        return f'<ResumeCertification User ID: {self.user_id}>'
class JobApplication(db.Model):
    __tablename__ = 'job_applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected'
    resume_path = db.Column(db.String(200), nullable=True)  # Store path to the resume file

    # Relationships
    user = db.relationship('User', backref='applications')
    job = db.relationship('Job', backref='applications')

    def __init__(self, user_id, job_id, status, resume_path):
        self.user_id = user_id
        self.job_id = job_id
        self.status = status
        self.resume_path = resume_path
