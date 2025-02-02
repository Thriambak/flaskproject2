from datetime import datetime, date
import random
import string
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from functools import wraps
import os
from werkzeug.utils import secure_filename
#from models import Job, JobApplication, db,User,ResumeCertification, Notification
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import Certification, Coupon, Couponuser, User, db  # Ensure 'db' is the instance of SQLAlchemy
# Assuming your model is in 'models.py'
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
    user_id = session.get('login_id')
    
    # Ensure the user_id is in session
    if not user_id:
        flash("User is not logged in.", "error")
        return redirect(url_for('auth.login'))
    
    print("\n\n",session['login_id'],session['username'],session['role'],"\n\n")

    # Query to fetch all jobs (or filter by user_id for jobs posted by the user)
    
    # jobs = Job.query.all()  # If you want to show all jobs. If you need jobs posted by the user, filter by created_by 
    
# Uncomment this to only show jobs posted by the user

    # Ensure the user is not an admin (or redirect to the admin dashboard)
    if session.get('role') != 'college':
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('college_dashboard.html')
@college_blueprint.route('/college_studenttraking')
@login_required
def college_studenttraking():
    return render_template('college_studenttracking.html')
@college_blueprint.route('/college_referall')
@login_required
def college_referall():
    return render_template('college_referall.html')
@college_blueprint.route('/college_collab')
@login_required
def college_collab():
    return render_template('college_collab.html')

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