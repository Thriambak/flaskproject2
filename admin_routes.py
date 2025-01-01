from datetime import datetime
from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps
from flask import request, jsonify, render_template, flash, redirect, url_for

from models import Job, JobApplication, User

 # Assuming you have a Job model defined in models.py


admin_blueprint = Blueprint('admin_routes', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_blueprint.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if session.get('role') != 'admin':
        flash("You must be an admin to access this page.", "error")
        return redirect(url_for('auth.login'))
    
    # Fetch job applications (pending ones)
    pending_applications = JobApplication.query.filter_by(status='pending').all()

    # Fetch other stats (e.g., total jobs, users)
    total_jobs = Job.query.count()
    total_users = User.query.count()
    pending_reports = 0  # You can add logic for pending reports if needed

    return render_template(
        'admin_dashboard.html', 
        total_jobs=total_jobs, 
        total_users=total_users, 
        pending_reports=pending_reports, 
        pending_applications=pending_applications
    )

@admin_blueprint.route('/adminmn', methods=['GET', 'POST'])
def manage_jobs():
    from app import db
    from models import Job
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))  # Ensure only admins can access

    if request.method == 'POST':
        # Get form data
        title = request.form['jobTitle']
        description = request.form['jobDescription']
        job_type = request.form['jobType']
        location = request.form['location']
        salary = request.form['salary']
        deadline_str = request.form['deadline']
        created_by = session['user_id']  # Get admin's user ID from session

        # Convert the deadline string to a Python date object
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format for the deadline. Please use YYYY-MM-DD.', 'danger')
            return redirect(url_for('admin_routes.manage_jobs'))

        # Save job to database
        new_job = Job(
            title=title,
            description=description,
            job_type=job_type,
            location=location,
            salary=salary,
            deadline=deadline,
            created_by=created_by
        )
        db.session.add(new_job)
        db.session.commit()
        flash('Job added successfully!', 'success')
        return redirect(url_for('admin_routes.manage_jobs'))  # Corrected redirect

    # Retrieve all jobs created by the admin
    jobs = Job.query.all()
    return render_template('adminmn.html', jobs=jobs)


@admin_blueprint.route('/adminmj')
@login_required
def adminmj():
    return render_template('adminmj.html')
