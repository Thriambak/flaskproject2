from datetime import datetime, date
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from functools import wraps
import os
from werkzeug.utils import secure_filename
#from models import Job, JobApplication, db,User,ResumeCertification, Notification
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db  # Ensure 'db' is the instance of SQLAlchemy
# Assuming your model is in 'models.py'
from config import Config
from utils import allowed_file  # Assuming your config file is named config.py
from models import Job, Company, Login, JobApplication, User, Communication


company_blueprint = Blueprint('company', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# Display the user dashboard

@company_blueprint.route('/company_dashboard')
@login_required
def company_dashboard():
    user_id = session.get('login_id')
    
    # Ensure the user_id is in session
    if not user_id:
        flash("User is not logged in.", "error")
        return redirect(url_for('auth.login'))
    
    print("\n\n",session['login_id'],session['username'],session['role'],"\n\n")

    # Query to fetch all jobs (or filter by user_id for jobs posted by the user)
    
    # jobs = Job.query.all()  # If you want to show all jobs. If you need jobs posted by the user, filter by created_by 
    
    jobs = Job.query.filter_by(created_by=user_id).all()  # Uncomment this to only show jobs posted by the user

    # Ensure the user is not an admin (or redirect to the admin dashboard)
    if session.get('role') != 'company':
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('company_dashboard.html', jobs=jobs)

# Job Posting
@company_blueprint.route('/company_jobposting')
@login_required
def company_jobposting():
    from app import db
    user_id = session.get('login_id')
    # Retrieve all jobs
    jobs = Job.query.filter_by(created_by=user_id).all()
    return render_template('company_job_posting.html', jobs=jobs)

# Post New Job
@company_blueprint.route('/company_post_new_job', methods=['GET','POST'])
@login_required
def company_post_new_job():
    from app import db

    if 'login_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.login'))  # Ensure only admins can access

    if request.method == 'POST':
        # Get form data
        job_id = request.form.get('jobId')
        title = request.form['job-title']
        description = request.form['description']
        skills = request.form['skill-sets']
        certifications = request.form['certifications']
        job_type = request.form['job-type']
        locations = request.form['locations']
        salary = request.form['salary']
        total_vacancy = request.form['vacancy']
        deadline_str = request.form['deadline']
        created_by = session['login_id']  # Get admin's user ID from session
        total_vacancy = int(total_vacancy)
        filled_vacancy = 3
        if total_vacancy > filled_vacancy:
            status = "open" 
        else:
            status = "closed"

        # Convert the deadline string to a Python date object
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format for the deadline. Please use YYYY-MM-DD.', 'danger')
            return redirect(url_for('company.company_post_new_job'))

        if job_id:  # Update the job
            job = Job.query.get(job_id)
            if job:
                job.title = title
                job.description = description
                job.job_type = job_type
                job.skills = skills
                job.certifications = certifications
                job.locations = locations
                job.salary = salary
                job.total_vacancy = total_vacancy
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
                skills = skills,
                certifications = certifications,
                location=locations,
                salary=salary,
                total_vacancy=total_vacancy,
                filled_vacancy=filled_vacancy,
                status=status,
                deadline=deadline,
                created_by=created_by
            )
            print(title)
            db.session.add(new_job)
            db.session.commit()
            flash('Job added successfully!', 'success')

        return redirect(url_for('company.company_jobposting'))

    # Retrieve all jobs
    # jobs = Job.query.all()
    current_date = date.today().strftime('%d-%m-%Y')   # Get today's date in 'DD-MM-YYYY' format
    return render_template('company_post_new_job.html',current_date=current_date)

# Application Review
@company_blueprint.route('/company_application_review', methods=['GET', 'POST'])
@login_required
def company_application_review():
    user_id = session.get('login_id')
    
    if 'login_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.login'))  # Ensure only company can access
    
    if request.method == 'POST':
        # Handle the status update
        application_id = request.form.get('application_id')
        new_status = request.form.get('status')
 
        # print('\n',application_id,new_status,'\n')   # debug
        # Update the application status in the database
        application = JobApplication.query.get(application_id)
        if application:
            application.status = new_status
            db.session.commit()
            flash('Application status updated successfully!', 'success')
        else:
            flash('Application not found!', 'danger')

    # Get all jobs created by the company
    jobs = Job.query.filter_by(created_by=user_id).all()
    
    # Get all job applications for the jobs created by the company
    job_applications = JobApplication.query.join(Job).filter(Job.created_by == user_id).all()
    
    # Create a list of applications with details for rendering
    applications_data = []
    for application in job_applications:
        applications_data.append({
            'candidate_name': application.user.name,
            'job_post': application.job.title,
            'status': application.status,
            'application_id': application.id,  # Include application ID
            'resume_path': application.resume_path,
            'certificate_path': application.certificate_path,
        })

    return render_template('company_application_review.html', applications=applications_data)

# Hiring Communication
'''@company_blueprint.route('/company_hiring_communication')
@login_required
def company_hiring_communication():
    user_id = session.get('login_id')
    
    if 'login_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.login'))  # Ensure only company can access
    
    if request.method == 'POST':
        application_id = request.form.get('application_id')

        msg = Notification.query.filter_by(user_id=application_id).all()
        
    return render_template('company_hiring_message.html')'''

# Hiring Communication
@company_blueprint.route('/company_hiring_communication', methods=['GET', 'POST'])
@login_required
def company_hiring_communication():
    user_id = session.get('login_id')
    
    if 'login_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.login'))  # Ensure only company can access

    # Fetch all users who applied for the company's jobs
    applied_users = (
        db.session.query(User.id, User.name)
        .join(JobApplication, JobApplication.user_id == User.id)
        .join(Job, JobApplication.job_id == Job.job_id)
        .filter(Job.created_by == user_id)
        .all()
    )

    # Fetch communication history
    messages = (
        db.session.query(Communication, User.name)
        .join(User, User.id == Communication.user_id)
        .filter(Communication.company_id == user_id)
        .order_by(Communication.timestamp.desc())
        .all()
    )

    if request.method == 'POST':
        # Get data from form
        selected_user_id = request.form.get('user_id')
        message_content = request.form.get('message')

        print(f"Selected User ID: {selected_user_id}")
        print(f"Message Content: {message_content}")

        # Add message to the database
        if selected_user_id and message_content:
            new_message = Communication(company_id=user_id, user_id=selected_user_id, message=message_content)
            db.session.add(new_message)
            db.session.commit()
            flash('Message sent successfully!', 'success')

        return redirect(url_for('company.company_hiring_communication'))

    return render_template('company_hiring_message.html', applied_users=applied_users, messages=messages)


# Profile
@company_blueprint.route('/company_profile', methods=['GET', 'POST'])
@login_required
def company_profile():
    user_id = session.get('login_id')

    if 'login_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.login'))  # Ensure only companies can access

    if request.method == 'POST':
        # Get form data
        company_id = request.form.get('logId')  # Hidden input for company ID
        company_name = request.form['company-name']
        description = request.form['company-description']
        email = request.form['contact-email']
        address = request.form['company-address']
        website = request.form['company-website']
        logo = request.form['company-logo']

        # Fetch the company profile by ID and update its fields
        profile = Company.query.filter_by(id=company_id, login_id=user_id).first()
        if profile:
            profile.company_name = company_name
            profile.description = description
            profile.email = email
            profile.address = address
            profile.website = website
            profile.logo = logo
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        else:
            flash('Profile not found or unauthorized access.', 'danger')

    # Fetch the company profile to display in the form
    companies = Company.query.filter_by(login_id=user_id).first()

    return render_template('company_profile.html', companies=companies, login_id=user_id)






'''
# Handle job application
@company_blueprint.route('/apply_for_job/<int:job_id>', methods=['POST'])
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
        flash("Application Successfull")
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
    from models import Notification  # Import the Notification model

    # Fetch notifications for the logged-in user
    user_id = session.get('user_id')
    if not user_id:
        flash("You need to log in to view your notifications.", "error")
        return redirect(url_for('auth.login'))

    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
    return render_template('notification.html', notifications=notifications)

# Helper function to check file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}

@user_blueprint.route('/resume_certifications', methods=['GET', 'POST'])
def resume_certifications():
    # Ensure the user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to access this page.', 'error')
        return redirect(url_for('login'))  # Adjust as needed

    # Fetch user data
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))  # Adjust as needed

    if request.method == 'POST':
        # Ensure the upload folder exists
        upload_folder = os.path.join('static', 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Get files from the form
        resume = request.files.get('resume')
        certification = request.files.get('certification')

        # Initialize paths
        resume_path = None
        certification_path = None

        # Handle Resume Upload
        if resume and allowed_file(resume.filename):
            resume_filename = secure_filename(resume.filename)
            resume_path = os.path.join(upload_folder, f"resume_{user.username}_{resume_filename}")
            resume.save(resume_path)
            resume_path = resume_path.replace('\\', '/')  # Normalize path for web use

        # Handle Certification Upload
        if certification and allowed_file(certification.filename):
            cert_filename = secure_filename(certification.filename)
            certification_path = os.path.join(upload_folder, f"certification_{user.username}_{cert_filename}")
            certification.save(certification_path)
            certification_path = certification_path.replace('\\', '/')  # Normalize path for web use

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
    from app import db
    from models import User

    # Get the current user's ID from the session
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to access your profile.', 'error')
        return redirect(url_for('auth.login'))

    # Query the database for the user's information
    user = User.query.filter_by(id=user_id, role='user').first()

    if user:
        return render_template(
            'profile.html',
            user={
                'name': user.name,
                'role': user.role,
                'email': user.email,
                
            }
        )
    else:
        flash('User not found.', 'error')
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

@user_blueprint.route('/mark_notification_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    from models import Notification

    # Fetch the notification
    notification = Notification.query.get(notification_id)
    user_id = session.get('user_id')

    if notification and notification.user_id == user_id:
        notification.read = True
        db.session.commit()
        flash("Notification marked as read.", "success")
    else:
        flash("Notification not found or unauthorized.", "error")
    return redirect(url_for('user.notifications'))


@user_blueprint.route('/delete_notification/<int:notification_id>', methods=['POST'])
@login_required
def delete_notification(notification_id):
    from models import Notification

    # Fetch the notification
    notification = Notification.query.get(notification_id)
    user_id = session.get('user_id')

    if notification and notification.user_id == user_id:
        db.session.delete(notification)
        db.session.commit()
        flash("Notification deleted successfully.", "success")
    else:
        flash("Notification not found or unauthorized.", "error")
    return redirect(url_for('user.notifications'))
'''