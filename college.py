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
from models import Coupon, db  # Ensure 'db' is the instance of SQLAlchemy
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
@college_blueprint.route('/college_coupon')
@login_required
def college_coupon():
    return render_template('college_coupon.html')
@college_blueprint.route('/college_collab')
@login_required
def college_collab():
    return render_template('college_collab.html')
@college_blueprint.route('/endorse')
@login_required
def endorse():
    return render_template('endorse.html')
def generate_coupon_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Updating the generate_coupon route to include college_id
@college_blueprint.route('/generate_coupon', methods=['GET', 'POST'])
def generate_coupon():
    if request.method == 'POST':
        faculty_id = request.form['faculty_id']
        year = request.form['year']
        
        # Get the logged-in college's ID
        id = session.get('college_id')
        college = College.query.filter_by(id=id).first()
        
        if not college:
            print(id)
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
    
    # Fetch all active coupons from the database
    coupons = Coupon.query.all()
    return render_template('college_coupon.html', coupons=coupons)
