from datetime import datetime
#import pytz
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
from enum import Enum

class RoleEnum(Enum):
    user = "user"
    admin = "admin"
    company = "company"

"""
COMPANY
"""
class Job(db.Model):
    __tablename__ = 'jobs'

    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    # company_id = db.Column(db.Integer, nullable=False) done in 'created_by'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    job_type = db.Column(db.String(20), nullable=False)  # full-time, part-time, contract
    skills = db.Column(db.Text)
    certifications = db.Column(db.Text)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50), nullable=False)
    total_vacancy = db.Column(db.Integer, nullable=False)
    filled_vacancy = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    deadline = db.Column(db.Date)
    created_at = db.Column(db.DateTime,default=datetime.utcnow) #default=datetime.now(pytz.timezone('Asia/Kolkata')))
    created_by = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)

    # Relationship with User (if needed)
    user = db.relationship('Login', backref=db.backref('jobs', lazy=True))
    # creator = db.relationship('Login', backref='jobs')

    def __init__(self, title, description, job_type, skills, certifications, location, salary, total_vacancy,
    filled_vacancy, status, deadline, created_by, job_id=None):
        self.title = title
        self.description = description
        self.job_type = job_type
        self.skills = skills
        self.certifications = certifications
        self.location = location
        self.salary = salary
        self.total_vacancy = total_vacancy
        self.filled_vacancy = filled_vacancy
        self.status = status
        self.deadline = deadline
        self.created_by = created_by
        if job_id is not None:
            self.job_id = job_id


class Login(db.Model):
    __tablename__ = 'logins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('user', 'company', 'admin', 'college'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def _repr_(self):
        return f'<Login {self.username}>'

# User Table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15))
    age = db.Column(db.Integer)

    login = db.relationship('Login', backref=db.backref('user', uselist=False))

    def _repr_(self):
        return f'<User {self.email}>'

# Company Table
class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True) #, autoincrement=True
    login_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    website = db.Column(db.String(100))
    logo = db.Column(db.String(255))
    description = db.Column(db.String(500))

    login = db.relationship('Login', backref=db.backref('company', uselist=False))

    def _repr_(self):
        return f'<Company {self.company_name}>'

# Admin Table
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    login = db.relationship('Login', backref=db.backref('admin', uselist=False))

    def _repr_(self):
        return f'<Admin {self.name}>'

# ithil nammal kodukunna username aan company,college ,admin and username aayitt edkan ushesikunne, ath kurach changes koode und

class JobApplication(db.Model):
    __tablename__ = 'job_applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.job_id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected'
    resume_path = db.Column(db.String(200), nullable=True)  # Store path to the resume file
    certificate_path = db.Column(db.String(200), nullable=True)
    # Relationships
    user = db.relationship('User', backref='applications')
    job = db.relationship('Job', backref='applications')

    def __init__(self, user_id, job_id, status, resume_path,certificate_path):
        self.user_id = user_id
        self.job_id = job_id
        self.status = status
        self.resume_path = resume_path
        self.certificate_path=certificate_path


class Communication(db.Model):
    __tablename__ = 'communications'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('Login', foreign_keys=[company_id], backref='sent_messages')
    receiver = db.relationship('Login', foreign_keys=[user_id], backref='received_messages')
    
    def __init__(self, company_id, user_id, message):
        self.company_id = company_id
        self.user_id = user_id
        self.message = message


class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('Login', backref='notifications')
    
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message


class ResumeCertification(db.Model):
    __tablename__ = 'resume_certifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)
    resume_path = db.Column(db.String(255), nullable=True)  # Path to the resume file
    certification_path = db.Column(db.String(255), nullable=True)  # Path to the certification file
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Upload timestamp

    user = db.relationship('Login', backref=db.backref('resume_certifications', lazy=True))

    def __repr__(self):
        return f'<ResumeCertification User ID: {self.user_id}>'

'''class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('user', 'company', 'admin'), nullable=False)
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


'''
