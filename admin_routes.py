from datetime import datetime
from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from functools import wraps
from models import Job, User, Notification #, JobApplication

# Define the admin blueprint
admin_blueprint = Blueprint('admin_routes', __name__)

# Admin-required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'].lower() != 'admin':
            flash('You are not authorized to access this page.', 'danger')
            return redirect(url_for('user.user_dashboard'))  # Redirect non-admin users
        return f(*args, **kwargs)
    return decorated_function

# Admin dashboard route
@admin_blueprint.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    if session.get('role') != 'admin':
        flash("You must be an admin to access this page.", "error")
        return redirect(url_for('auth.login'))
    
    # Fetch job applications (pending ones)
    pending_applications = JobApplication.query.filter_by(status='pending').all()

    # Fetch other stats
    total_jobs = Job.query.count()
    total_users = User.query.filter_by(role='user').count()
    pending_reports = JobApplication.query.filter_by(status='pending').count()

    return render_template(
        'admin_dashboard.html', 
        total_jobs=total_jobs, 
        total_users=total_users, 
        pending_reports=pending_reports, 
        pending_applications=pending_applications
    )

# Manage jobs route
@admin_blueprint.route('/adminmn', methods=['GET', 'POST'])
def manage_jobs():
    from app import db

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))  # Ensure only admins can access

    if request.method == 'POST':
        # Get form data
        job_id = request.form.get('jobId')
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

        if job_id:  # Update the job
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
        else:  # Add a new job
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

    # Retrieve all jobs
    jobs = Job.query.all()
    return render_template('adminmn.html', jobs=jobs)

# Delete job route
@admin_blueprint.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    from app import db

    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')

    return redirect(url_for('admin_routes.manage_jobs'))

# View pending applications route
@admin_blueprint.route('/view_pending_applications')
def view_pending_applications():
    pending_applications = JobApplication.query.filter_by(status='pending').all()
    return render_template('application.html', pending_applications=pending_applications)

# Accept or reject application route
@admin_blueprint.route('/accept_or_reject/<int:application_id>', methods=['POST'])
@admin_required
def accept_or_reject(application_id):
    from app import db

    action = request.form.get('action')
    application = JobApplication.query.get(application_id)

    if not application:
        flash("Application not found.", "error")
        return redirect(url_for('admin_routes.admin_dashboard'))
    
    user = User.query.get(application.user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('admin_routes.admin_dashboard'))
    
    # Update application status
    if action == "accept":
        application.status = "accepted"
        message = f"Your application for the job '{application.job.title}' was accepted."
    elif action == "reject":
        application.status = "rejected"
        message = f"Your application for the job '{application.job.title}' was rejected."
    else:
        flash("Invalid action.", "error")
        return redirect(url_for('admin_routes.admin_dashboard'))
    
    # Create a notification
    notification = Notification(user_id=user.id, message=message)
    db.session.add(notification)
    db.session.commit()

    flash(f"Application {action}ed successfully!", "success")
    return redirect(url_for('admin_routes.admin_dashboard'))

# Manage users route
@admin_blueprint.route('/manage_users')
def manage_users():
    from models import ResumeCertification
    from app import db

    users_with_resumes = db.session.query(
        User.id, User.name, User.email, User.phone, User.role, ResumeCertification.resume_path
    ).join(ResumeCertification, User.id == ResumeCertification.user_id).filter(User.role == 'user').all()

    users_data = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "resume_path": user.resume_path,
        }
        for user in users_with_resumes
    ]

    return render_template('adminmj.html', users=users_data)

# Delete user route
@admin_blueprint.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    from models import User
    from app import db

    user_to_delete = User.query.get(user_id)

    if not user_to_delete:
        flash("User not found.", 'danger')
        return redirect(url_for('admin_routes.manage_users'))

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f"User {user_to_delete.name} has been deleted.", 'success')
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", 'danger')
        db.session.rollback()
    
    return redirect(url_for('admin_routes.manage_users'))
