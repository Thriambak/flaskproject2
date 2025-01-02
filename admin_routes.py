from datetime import datetime
from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps
from flask import request, jsonify, render_template, flash, redirect, url_for

from models import Job, JobApplication, User

 # Assuming you have a Job model defined in models.py


admin_blueprint = Blueprint('admin_routes', __name__)

from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'].lower() != 'admin':
            flash('You are not authorized to access this page.', 'danger')
            return redirect(url_for('user.user_dashboard'))  # Redirect non-admin users
        return f(*args, **kwargs)
    return decorated_function


@admin_blueprint.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    if session.get('role') != 'admin':
        flash("You must be an admin to access this page.", "error")
        return redirect(url_for('auth.login'))
    
    # Fetch job applications (pending ones)
    pending_applications = JobApplication.query.filter_by(status='pending').all()
    

    # Fetch other stats (e.g., total jobs, users)
    total_jobs = Job.query.count()
    total_users = User.query.count()
    pending_reports = JobApplication.query.filter_by(status='pending').count()# You can add logic for pending reports if needed

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
        job_id = request.form.get('jobId')  # Hidden field for job ID
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

        if job_id:  # If jobId is provided, update the job
            job = Job.query.get(job_id)
            if job:
                job.title = title
                job.description = description
                job.job_type = job_type
                job.location = location
                job.salary = salary
                job.deadline = deadline
                db.session.commit()
                flash('Job updated successfully!', 'success')
            else:
                flash('Job not found.', 'danger')
        else:  # If jobId is not provided, add a new job
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

        return redirect(url_for('admin_routes.manage_jobs'))

    # Retrieve all jobs created by the admin
    jobs = Job.query.all()
    return render_template('adminmn.html', jobs=jobs)

@admin_blueprint.route('/delete_job/<int:job_id>', methods=['POST'])

def delete_job(job_id):
    from app import db
    from models import Job

    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')

    return redirect(url_for('admin_routes.manage_jobs'))


@admin_blueprint.route('/view_pending_applications')
def view_pending_applications():
    # Fetch all pending job applications
    pending_applications = JobApplication.query.filter_by(status='pending').all()

    # Pass the data to the new template
    return render_template('application.html', pending_applications=pending_applications)
@admin_blueprint.route('/accept_or_reject/<int:application_id>', methods=['POST'])
@admin_required

def accept_or_reject(application_id):
    from models import db
    action = request.form.get('action')
    application = JobApplication.query.get(application_id)  # Get the specific application by ID

    if not application:
        flash("Application not found.", 'error')
        return redirect(url_for('admin_routes.admin_dashboard'))

    if action == 'accept':
        application.status = 'accepted'
    elif action == 'reject':
        application.status = 'rejected'

    db.session.commit()
    flash(f"Application {action}ed successfully.", 'success')

    return redirect(url_for('admin_routes.admin_dashboard'))


# Admin dashboard route

@admin_blueprint.route('/adminmj')
@admin_required
def adminmj():
    return render_template('adminmj.html')
