from datetime import datetime, date
import random
import string
from flask import Blueprint, render_template, request, session, redirect
from flask import url_for, flash
from functools import wraps
import os
from werkzeug.utils import secure_filename
#from models import Job, JobApplication, db,User,ResumeCertification, Notification
from flask_login import login_required, current_user
from models import Certification, Company, Coupon, Couponuser, Job, JobApplication, User, db  # Ensure 'db' is the instance of SQLAlchemy
from config import Config
from utils import allowed_file  # Assuming your config file is named config.py
from models import College, Login


college_blueprint = Blueprint('college', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# Display the user dashboard

@college_blueprint.route('/college_dashboard')
@login_required
def college_dashboard():
    college_id = session.get('college_id')
    
    # Ensure the college_id is in session
    if not college_id:
        flash("College is not logged in.", "error")
        return redirect(url_for('auth.login'))
    
    print("\n\n", session['college_id'], session['username'], session['role'], "\n\n")

    # Query to count the number of students registered for coupons for the current college
    registered_students_count = db.session.query(Couponuser).join(Coupon).filter(Coupon.college_id == college_id).count()

    # Ensure the user is a college
    if session.get('role') != 'college':
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('college_dashboard.html', registered_students_count=registered_students_count)
@college_blueprint.route('/college_studenttracking')
@login_required
def college_studenttracking():
    college_id = session.get('college_id')
    
    if not college_id:
        flash("College is not logged in.", "error")
        return redirect(url_for('auth.login'))

    # Query to join the tables and filter by the logged-in college's ID
    student_activity = db.session.query(
        User.name.label('student_name'),
        Company.company_name.label('company_name'),
        JobApplication.status.label('job_application_status')
    ).join(Couponuser, Couponuser.user_id == User.id)\
     .join(Coupon, Coupon.id == Couponuser.coupon_id)\
     .join(JobApplication, JobApplication.user_id == User.id)\
     .join(Job, Job.job_id == JobApplication.job_id)\
     .join(Company, Company.login_id == Job.created_by)\
     .filter(Coupon.college_id == college_id)\
     .all()

    return render_template('college_studenttracking.html', student_activity=student_activity)
@college_blueprint.route('/college_referall')
@login_required
def college_referall():
    return render_template('college_referall.html')
@college_blueprint.route('/college_collab')
@login_required
def college_collab():
    college_id = session.get('college_id')
    
    if not college_id:
        flash("College is not logged in.", "error")
        return redirect(url_for('auth.login'))

    # Get total students from this college
    total_students = db.session.query(Couponuser).join(Coupon).filter(Coupon.college_id == college_id).count()

    # Get partnered companies (distinct companies that have hired students from this college)
    partnered_companies = db.session.query(
        Company.company_name
    ).join(Job, Job.created_by == Company.login_id)\
     .join(JobApplication, JobApplication.job_id == Job.job_id)\
     .join(User, User.id == JobApplication.user_id)\
     .join(Couponuser, Couponuser.user_id == User.id)\
     .join(Coupon, Coupon.id == Couponuser.coupon_id)\
     .filter(
         Coupon.college_id == college_id,
         JobApplication.status == 'accepted'  # Assuming 'accepted' means hired
     ).distinct().all()

    # Count placed students from this college
    placed_students = db.session.query(JobApplication)\
        .join(User, User.id == JobApplication.user_id)\
        .join(Couponuser, Couponuser.user_id == User.id)\
        .join(Coupon, Coupon.id == Couponuser.coupon_id)\
        .filter(
            Coupon.college_id == college_id,
            JobApplication.status == 'accepted'
        ).count()

    # Calculate placement percentage
    placed_percentage = 0
    if total_students > 0:
        placed_percentage = round((placed_students / total_students) * 100, 2)

    return render_template('college_collab.html',
                         partnered_companies=partnered_companies,
                         total_students=total_students,
                         placed_percentage=placed_percentage)

def generate_coupon_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Updating the generate_coupon route to include college_id
@college_blueprint.route('/generate_coupon', methods=['GET', 'POST'])
@login_required
def generate_coupon():
    # Fetch all active coupons from the database
    college_id = session.get('college_id')
    coupons = Coupon.query.filter_by(college_id=college_id).all()

    if request.method == 'POST':
        faculty_id = request.form['faculty_id']
        year = request.form['year']
        
        # Get the logged-in college's ID
        college = College.query.filter_by(id=college_id).first()
        
        if not college:
            flash("College not found!", "error")
            return redirect(url_for('college.generate_coupon'))
        
        # Generate a unique coupon code
        coupon_code = generate_coupon_code()
        while Coupon.query.filter_by(code=coupon_code).first():
            coupon_code = generate_coupon_code()
        
        # Add the coupon to the database
        new_coupon = Coupon(code=coupon_code, faculty_id=faculty_id, year=year, college_id=college.id)
        db.session.add(new_coupon)
        db.session.commit()
        
        flash('Coupon generated successfully!', 'success')
        return redirect(url_for('college.generate_coupon'))
    
    # Render the template with the coupons data for both GET and POST requests
    return render_template('college_coupon.html', coupons=coupons)
@college_blueprint.route('/user_details/<int:user_id>')
@login_required
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    certifications = Certification.query.filter_by(user_id=user_id).all()
    return render_template('user_details.html', user=user, certifications=certifications)
@college_blueprint.route('/verify_certification/<int:cert_id>', methods=['POST'])
@login_required
def verify_certification(cert_id):
    certification = Certification.query.get_or_404(cert_id)
    certification.verification_status = True
    db.session.commit()
    flash('Certification verified successfully!', 'success')
    return redirect(url_for('college.user_details', user_id=certification.user_id))
@college_blueprint.route('/college_endorsement')
@login_required
def college_endorsement():
    # Fetch the necessary data from the database
    coupon_users = db.session.query(
        Coupon.code.label('coupon_code'),
        User.name.label('user_name'),
        Coupon.faculty_id,
        Coupon.year,
        User.id.label('user_id')
    ).join(Couponuser, Couponuser.coupon_id == Coupon.id)\
     .join(User, Couponuser.user_id == User.id)\
     .filter(Coupon.college_id == session.get('college_id'))\
     .all()

    return render_template('endorse.html', coupon_users=coupon_users)