from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import current_user
from config import Config
from functools import wraps
import os
from werkzeug.utils import secure_filename
from models import Job, JobApplication, db,User,ResumeCertification
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models import db  # Ensure 'db' is the instance of SQLAlchemy
  # Assuming your model is in 'models.py'
from config import Config
from utils import allowed_file  # Assuming your config file is named config.py


user_blueprint = Blueprint('user', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# Display the user dashboard


@user_blueprint.route('/user_dashboard')
@login_required
def user_dashboard():
    user_id = session.get('user_id')
    
    # Ensure the user_id is in session
    if not user_id:
        flash("User is not logged in.", "error")
        return redirect(url_for('auth.login'))

    # Query to fetch all jobs (or filter by user_id for jobs posted by the user)
    jobs = Job.query.all()  # If you want to show all jobs. If you need jobs posted by the user, filter by created_by
    # jobs = Job.query.filter_by(created_by=user_id).all()  # Uncomment this to only show jobs posted by the user
    print(jobs)  # Debugging line

    # Ensure the user is not an admin (or redirect to the admin dashboard)
    if session.get('role') != 'user':
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('user_dashboard.html', jobs=jobs)

# Handle job application
@user_blueprint.route('/apply_for_job/<int:job_id>', methods=['POST'])
@login_required
def apply_for_job(job_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)  # Fetch the user details from the database
    
    if not user:
        flash("User not found.", 'error')
        return redirect(url_for('user.user_dashboard'))

    # Fetch the job that the user is applying for
    job = Job.query.get(job_id)
    if not job:
        flash("Job not found.", 'error')
        return redirect(url_for('user.user_dashboard'))
    
    # Fetch the user's resume from the ResumeCertification table
    resume_certification = ResumeCertification.query.filter_by(user_id=user.id).first()
    if resume_certification:
        print("Debugging: resume_certification.resume_path:", resume_certification.resume_path)
    if not resume_certification or not resume_certification.resume_path:
        flash("You must upload a resume to apply for a job.", 'error')
        return redirect(url_for('user.resume_certifications'))

    # Prepare the application
    new_application = JobApplication(
        user_id=user.id,
        job_id=job.id,
        status='pending',  # You can modify the status later (e.g., 'accepted', 'rejected')
        resume_path=resume_certification.resume_path  # Store the resume path
    )

    # Add the application to the database
    db.session.add(new_application)
    db.session.commit()

    flash(f"Application for {job.title} submitted successfully!", 'success')

    # Redirect to the user dashboard
    return redirect(url_for('user.user_dashboard'))

@user_blueprint.route('/notifications')
@login_required
def notifications():
    # Replace with actual database query
    mock_notifications = [
        {"id": 1, "message": "Your application for the Software Engineer position was accepted.", "read": False, "timestamp": datetime(2024, 12, 15, 10, 0)},
        {"id": 2, "message": "The deadline for 'Project Manager' has been extended.", "read": True, "timestamp": datetime(2024, 12, 12, 15, 45)},
        {"id": 3, "message": "Your resume has been viewed by the recruiter.", "read": False, "timestamp": datetime(2024, 12, 10, 9, 30)}
    ]
    return render_template('notification.html', notifications=mock_notifications)
@user_blueprint.route('/mark_notification_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    # Placeholder for database update logic
    print(f"Mark notification {notification_id} as read.")
    return redirect(url_for('user.notifications'))
@user_blueprint.route('/delete_notification/<int:notification_id>', methods=['POST'])
@login_required
def delete_notification(notification_id):
    # Placeholder for database delete logic
    print(f"Deleted notification {notification_id}.")
    return redirect(url_for('user.notifications'))



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}

@user_blueprint.route('/resume_certifications', methods=['GET', 'POST'])
def resume_certifications():
    # Ensure the user is logged in by checking session
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to access this page.', 'error')
        return redirect(url_for('login'))  # Adjust as needed

    # Fetch user data and related certifications
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))  # Adjust as needed

    if request.method == 'POST':
        # Ensure that files are provided
        if 'resume' not in request.files and 'certification' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('user.resume_certifications'))

        resume = request.files.get('resume')
        certification = request.files.get('certification')

        # Ensure the upload folder exists
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        # Handle Resume Upload
        if resume and allowed_file(resume.filename):
            resume_filename = secure_filename(resume.filename)
            resume_path = os.path.join('uploads', f"resume_{user.username}_{resume_filename}")
            resume.save(resume_path)
        else:
            resume_path = None

        # Handle Certification Upload
        if certification and allowed_file(certification.filename):
            cert_filename = secure_filename(certification.filename)
            certification_path = os.path.join('uploads', f"certification_{user.username}_{cert_filename}")
            certification.save(certification_path)
        else:
            certification_path = None

        # Save to Database
        resume_certification = ResumeCertification(
            user_id=user.id,
            resume_path=resume_path,
            certification_path=certification_path
        )
        db.session.add(resume_certification)
        db.session.commit()

        flash('Files uploaded successfully!', 'success')
        return redirect(url_for('user.resume_certifications'))

    # Retrieve all resume/certifications for the user
    resume_certifications = ResumeCertification.query.filter_by(user_id=user_id).all()

    return render_template(
        'resume_certifications.html',
        resume_certifications=resume_certifications
    )
@user_blueprint.route('/profile')
@login_required
def profile():
    username = session.get('username')
    user_info = session.get(username)

    if user_info:
        return render_template('profile.html', user=user_info)
    else:
        flash('User not found', 'error')
        return redirect(url_for('user.user_dashboard'))


@user_blueprint.route('/load_application_history')
@login_required
def load_application_history():
    return render_template('applicationhistory.html')

@user_blueprint.route('/jobsearch')
@login_required
def jobsearch():
    # Render the job search page
    return render_template('jobsearch.html')
