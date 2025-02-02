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
    college="college"
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
    form_url = db.Column(db.String(255))  # To store the Google Form link
    deadline = db.Column(db.Date)
    created_at = db.Column(db.DateTime,default=datetime.utcnow) #default=datetime.now(pytz.timezone('Asia/Kolkata')))
    created_by = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)

    # Relationship with User (if needed)
    user = db.relationship('Login', backref=db.backref('jobs', lazy=True))
    # creator = db.relationship('Login', backref='jobs')

    def __init__(self, title, description, job_type, skills, certifications, location, salary, total_vacancy,
    filled_vacancy, status, form_url, deadline, created_by, job_id=None):
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
        self.form_url = form_url
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
class College(db.Model):
    __tablename__ = 'college'
    id = db.Column(db.Integer, primary_key=True) #, autoincrement=True
    login_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)
    college_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    website = db.Column(db.String(100))
    logo = db.Column(db.String(255))
    description = db.Column(db.String(500))

    login = db.relationship('Login', backref=db.backref('college', uselist=False))

    def _repr_(self):
        return f'<College {self.college_name}>'
# User Table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15))
    age = db.Column(db.Integer)
    about_me = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))  # New field for storing the picture path
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.login_id'))
    college_id = db.Column(db.Integer, db.ForeignKey('college.login_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.login_id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read_status = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship('User', backref=db.backref('communications', lazy=True))
    company = db.relationship('Company', backref=db.backref('communications', lazy=True))

    def __init__(self, user_id, college_id, company_id, message):
        self.user_id = user_id
        self.college_id = college_id
        self.company_id = company_id
        self.message = message



class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('companies.login_id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    read_status = db.Column(db.Boolean, nullable=False, default=False)
    hidden = db.Column(db.Boolean, nullable=False, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('Company', backref='notifications')
    
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message


class ResumeCertification(db.Model):
    __tablename__ = 'resume_certifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_path = db.Column(db.String(255), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    certifications = db.relationship('Certification', backref='resume_cert', lazy=True)

    def __repr__(self):
        return f'<ResumeCertification User ID: {self.user_id}>'

class Certification(db.Model):
    __tablename__ = 'certifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_cert_id = db.Column(db.Integer, db.ForeignKey('resume_certifications.id'), nullable=True)
    certification_name = db.Column(db.String(255), nullable=False)
    verification_status = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Certification {self.certification_name} for User ID: {self.user_id}>'
class Coupon(db.Model):
    __tablename__ = 'coupons'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    faculty_id = db.Column(db.String(20), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)  # Foreign key added

    college = db.relationship('College', backref=db.backref('coupons', lazy=True))

    def __repr__(self):
        return f"<Coupon {self.code}>"
class Couponuser(db.Model):
    __tablename__ = 'couponuser'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'), nullable=False)  # Foreign key added

    college = db.relationship('Coupon', backref=db.backref('couponuser', lazy=True))
    user = db.relationship('User', backref=db.backref('couponuser', lazy=True))
    def __repr__(self):
        return f"<Coupon {self.code}>"
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
