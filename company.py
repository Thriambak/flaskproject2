from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from functools import wraps
import os
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db  # Ensure 'db' is the instance of SQLAlchemy, assuming your model is in 'models.py'
from config import Config
from utils import allowed_file  # Assuming your config file is named config.py
from models import Job, Company, Login, JobApplication, User, Communication, Notification, College, Certification, ResumeCertification
import re


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
    
    # Get the selected year from query parameters or use current year as default
    selected_year = request.args.get('year', datetime.now().year)
    try:
        selected_year = int(selected_year)
    except ValueError:
        selected_year = datetime.now().year
    
    # Query to fetch all jobs posted by the user
    jobs = Job.query.filter_by(created_by=user_id).all()
    profile = Company.query.filter_by(login_id=user_id).first()
    
    # Get all applications for jobs created by this company
    applications = db.session.query(JobApplication)\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id).all()
    
    # Get years with applications for the year selector
    application_years = db.session.query(
        db.func.extract('year', JobApplication.date_applied).label('year')
    ).join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id)\
        .group_by('year')\
        .order_by('year')\
        .all()
    
    available_years = [int(year.year) for year in application_years]
    
    # If no applications found, include current year
    if not available_years:
        available_years = [datetime.now().year]
    
    # If selected year is not in available years, use the most recent available year
    if selected_year not in available_years:
        selected_year = available_years[-1]
    
    # Calculate monthly application rates for the selected year
    monthly_application_rates = [0] * 12  # Initialize with 0 for all 12 months
    
    # Process monthly data
    for month in range(1, 13):
        # Total applications in this month of the selected year
        total_applications = db.session.query(db.func.count(JobApplication.id))\
            .join(Job, JobApplication.job_id == Job.job_id)\
            .filter(
                Job.created_by == user_id,
                db.func.extract('year', JobApplication.date_applied) == selected_year,
                db.func.extract('month', JobApplication.date_applied) == month
            ).scalar() or 0
        
        # Hired applications in this month of the selected year
        hired_applications = db.session.query(db.func.count(JobApplication.id))\
            .join(Job, JobApplication.job_id == Job.job_id)\
            .filter(
                Job.created_by == user_id,
                db.func.extract('year', JobApplication.date_applied) == selected_year,
                db.func.extract('month', JobApplication.date_applied) == month,
                JobApplication.status == 'Hired'
            ).scalar() or 0
        
        # Calculate the application rate (percentage) for this month
        if total_applications > 0:
            monthly_application_rates[month-1] = (hired_applications / total_applications) * 100
    
    # Calculate overall metrics
    total_applications_count = len(applications)
    total_successful = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Hired')\
        .scalar() or 0
    
    total_unsuccessful = total_applications_count - total_successful
    
    # Calculate overall hiring rate
    overall_hiring_rate = 0
    if total_applications_count > 0:
        overall_hiring_rate = round((total_successful / total_applications_count) * 100, 1)
    
    # Ensure the user is not an admin
    if session.get('role') != 'company':
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('/company/dashboard.html', 
        jobs=jobs, 
        profile=profile,
        monthly_application_rates=monthly_application_rates,
        total_successful=total_successful, 
        total_unsuccessful=total_unsuccessful,
        overall_hiring_rate=overall_hiring_rate,
        available_years=available_years,
        selected_year=selected_year)

# Job Posting
@company_blueprint.route('/company_jobposting')
@login_required
def company_jobposting():
    from app import db
    user_id = session.get('login_id')
    
    if 'login_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.login'))  # Ensure only companies can access
    
    # Retrieve all jobs ordered by most recent
    jobs = Job.query.filter_by(created_by=user_id).order_by(Job.created_at.desc()).all()
    profile = Company.query.filter_by(login_id=user_id).first()

    return render_template('/company/job_posting.html', jobs=jobs, profile=profile,)

# Post New Job
@company_blueprint.route('/company_post_new_job', methods=['GET','POST'])
@login_required
def company_post_new_job():
    from app import db
    user_id = session.get('login_id')

    if 'login_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.login'))  # Ensure only companies can access

    message = None
    message_type = None
    form_data = {}  # Initialize form_data dictionary
    
    # Check if we're editing an existing job
    job = None
    job_id = request.args.get('job_id')
    
    if request.method == 'POST':
        # Get form data
        job_id = request.form.get('jobId')
        title = request.form.get('job-title', '').strip()
        description = request.form.get('description', '').strip()
        skills = request.form.get('skill-sets', '').strip()
        exp_str = request.form.get('exp', '').strip()
        certifications = request.form.get('certifications', '').strip()
        job_type = request.form.get('job-type', '').strip()
        locations = request.form.get('locations', '').strip()
        salary_str = request.form.get('salary', '').strip()
        vacancy_str = request.form.get('vacancy', '').strip()
        form_url = request.form.get('form-url', '').strip()
        deadline_str = request.form.get('deadline', '').strip()
        created_by = session['login_id']
        
        # Store form data to preserve it in case of validation errors
        form_data = {
            'title': title,
            'description': description,
            'skills': skills,
            'exp': exp_str,
            'certifications': certifications,
            'job_type': job_type,
            'locations': locations,
            'salary': salary_str,
            'vacancy': vacancy_str,
            'form_url': form_url,
            'deadline': deadline_str
        }
        
        # Validate inputs
        if len(title) < 3 or len(title) > 255:
            message = "Job Title must be between 3-255 characters!"
            message_type = "error"
        elif len(description) < 10 or len(description) > 2000:
            message = "Job Description must be between 10-2000 characters!"
            message_type = "error"
        elif not exp_str or not exp_str.isdigit():
            message = "Years of Experience must be a valid number!"
            message_type = "error"
        elif not vacancy_str or not vacancy_str.isdigit():
            message = "Vacancy must be a valid number!"
            message_type = "error"
        elif not deadline_str:
            message = "Application deadline is required!"
            message_type = "error"
        elif form_url and not is_valid_url(form_url):
            message = "Please enter a valid URL for the questionnaire form!"
            message_type = "error"
        else:
            try:
                # Convert string values to appropriate types
                exp = int(exp_str)
                total_vacancy = int(vacancy_str)
                salary = int(salary_str) if salary_str else None
                
                # Additional validations
                if exp < 0 or exp > 50:
                    message = "Years of Experience must be between 0-50!"
                    message_type = "error"
                elif total_vacancy < 1 or total_vacancy > 1000:
                    message = "Vacancy must be between 1-1000!"
                    message_type = "error"
                else:
                    # Convert the deadline string to a Python date object
                    try:
                        deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
                        current_date = date.today()
                        
                        if deadline < current_date:
                            message = "Deadline cannot be in the past!"
                            message_type = "error"
                        else:
                            filled_vacancy = 0
                            status = "open" if total_vacancy > filled_vacancy else "closed"
                            
                            if job_id:  # Update the job
                                job = Job.query.get(job_id)
                                if job and job.created_by == user_id:  # Security check
                                    # Save current filled_vacancy
                                    filled_vacancy = job.filled_vacancy
                                    
                                    job.title = title
                                    job.description = description
                                    job.job_type = job_type
                                    job.skills = skills
                                    job.years_of_exp = exp
                                    job.certifications = certifications
                                    job.location = locations
                                    job.salary = salary
                                    job.total_vacancy = total_vacancy
                                    job.deadline = deadline
                                    job.form_url = form_url
                                    
                                    # Update status based on vacancies
                                    job.status = "open" if total_vacancy > filled_vacancy else "closed"
                                    
                                    db.session.commit()
                                    message = "Job updated successfully!"
                                    message_type = "success"
                                else:
                                    message = "Job not found or you don't have permission to edit it."
                                    message_type = "error"
                            else:  # Add a new job
                                new_job = Job(
                                    title=title,
                                    description=description,
                                    job_type=job_type,
                                    skills=skills,
                                    years_of_exp=exp,
                                    certifications=certifications,
                                    location=locations,
                                    salary=salary,
                                    total_vacancy=total_vacancy,
                                    filled_vacancy=filled_vacancy,
                                    status=status,
                                    form_url=form_url,
                                    deadline=deadline,
                                    created_by=created_by
                                )
                                db.session.add(new_job)
                                db.session.commit()
                                message = "Job added successfully!"
                                message_type = "success"
                            
                            if message_type == "success":
                                return redirect(url_for('company.company_jobposting'))
                    except ValueError:
                        message = "Invalid date format for the deadline. Please use YYYY-MM-DD."
                        message_type = "error"
            except ValueError:
                message = "Please ensure all numeric fields contain valid numbers!"
                message_type = "error"
    else:  # GET request
        if job_id:
            job = Job.query.get(job_id)
            if job and job.created_by == user_id:  # Security check
                # Prefill form_data from existing job
                form_data = {
                    'title': job.title,
                    'description': job.description,
                    'skills': job.skills,
                    'exp': job.years_of_exp,
                    'certifications': job.certifications,
                    'job_type': job.job_type,
                    'locations': job.location,
                    'salary': job.salary if job.salary else '',
                    'vacancy': job.total_vacancy,
                    'form_url': job.form_url if job.form_url else '',
                    'deadline': job.deadline.strftime('%Y-%m-%d') if job.deadline else ''
                }
            else:
                return redirect(url_for('company.company_jobposting'))

    # Get jobs and application statistics
    jobs = Job.query.filter_by(created_by=user_id).all()

    # Calculate statistics for the dashboard/sidebar
    total_successful = db.session.query(db.func.count(JobApplication.id)).filter(
        JobApplication.job_id.in_([j.job_id for j in jobs]) if jobs else False, 
        JobApplication.status == 'Hired'
    ).scalar() or 0

    total_unsuccessful = db.session.query(db.func.count(JobApplication.id)).filter(
        JobApplication.job_id.in_([j.job_id for j in jobs]) if jobs else False, 
        JobApplication.status == 'Rejected'
    ).scalar() or 0

    pending_applications_count = db.session.query(db.func.count(JobApplication.id)).filter(
        JobApplication.job_id.in_([j.job_id for j in jobs]) if jobs else False, 
        JobApplication.status == 'Pending'
    ).scalar() or 0

    interviewed_applications_count = db.session.query(db.func.count(JobApplication.id)).filter(
        JobApplication.job_id.in_([j.job_id for j in jobs]) if jobs else False, 
        JobApplication.status == 'Interviewed'
    ).scalar() or 0

    # You'd need to define live_feed_notifications based on your app's requirements
    live_feed_notifications = []  # Replace with appropriate query

    # Get today's date in 'YYYY-MM-DD' format
    current_date = date.today().strftime('%Y-%m-%d')
    profile = Company.query.filter_by(login_id=user_id).first()
    
    return render_template('/company/post_new_job.html', 
                           current_date=current_date, 
                           profile=profile,
                           job_id=job_id,
                           form_data=form_data,  # Pass form data for populating fields
                           total_successful=total_successful, 
                           total_unsuccessful=total_unsuccessful,
                           pending_applications_count=pending_applications_count, 
                           live_feed_notifications=live_feed_notifications,
                           interviewed_applications_count=interviewed_applications_count,
                           message=message,
                           message_type=message_type)

# Helper function to validate URLs
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

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
 
        application = JobApplication.query.get(application_id)
        if application:
            if new_status == 'Rejected' and application.status == 'Hired':
                job = application.job
                job.filled_vacancy -= 1
                db.session.commit()

            application.status = new_status
            db.session.commit()
            flash('Application status updated successfully!', 'success')

            # If the application is hired, increment the filled_vacancy in Job table
            if new_status == 'Hired':
                job = application.job  # Get the related job
                if job.filled_vacancy < job.total_vacancy:  # Ensure filled_vacancy does not exceed total_vacancy
                    job.filled_vacancy += 1
                    db.session.commit()
                if job.filled_vacancy == job.total_vacancy:
                    job.status = 'closed'
                    db.session.commit()
        else:
            flash('Application not found!', 'danger')

    # Get filter parameters from request
    # For the filter dropdown
    selected_status = request.args.getlist('status')  # Get selected status filters
    selected_jobs = request.args.getlist('job_post')  # Get selected job filters
    
    # For the search functionality
    search_query = request.args.get('search_query', '').strip()

    # Get all jobs created by the company
    jobs = Job.query.filter_by(created_by=user_id).all()
    
    # Query all job applications for the company's jobs
    query = JobApplication.query.join(Job).filter(Job.created_by == user_id)

    # Apply filters based on dropdown selections
    if selected_status:
        query = query.filter(JobApplication.status.in_(selected_status))
    if selected_jobs:
        query = query.filter(Job.title.in_(selected_jobs))

    # Apply search filter - search across candidate name, job title, and status
    if search_query:
        query = query.join(User).filter(
            or_(
                User.name.ilike(f'%{search_query}%'),
                Job.title.ilike(f'%{search_query}%'),
                JobApplication.status.ilike(f'%{search_query}%')
            )
        )

    # Get all filtered job applications
    job_applications = query.all()
    
    # Create a list of applications with details for rendering
    applications_data = []
    for application in job_applications:
        # Fetch the latest resume for this user from ResumeCertification
        resume = ResumeCertification.query.filter_by(user_id=application.user_id).order_by(ResumeCertification.id.desc()).first()
        resume_path = resume.resume_path if resume else None
        
        applications_data.append({
            'candidate_name': application.user.name,
            'job_post': application.job.title,
            'status': application.status,
            'application_id': application.id,
            'resume_path': resume_path,
            'user_id': application.user_id
        })
    
    # Fetch certifications for each candidate
    user_certifications = {}
    user_ids = [app['user_id'] for app in applications_data]
    
    # Using a single query to get all certifications for all relevant users
    all_certifications = Certification.query.filter(Certification.user_id.in_(user_ids)).all()
    
    # Organize certifications by user_id
    for cert in all_certifications:
        if cert.user_id not in user_certifications:
            user_certifications[cert.user_id] = []
        
        user_certifications[cert.user_id].append({
            'certification_name': cert.certification_name,
            'verified': cert.verification_status
        })

    profile = Company.query.filter_by(login_id=user_id).first()
    
    return render_template(
        '/company/application_review.html',
        applications=applications_data,
        profile=profile,
        selected_status=selected_status,
        jobs=jobs,
        selected_jobs=selected_jobs,
        user_certifications=user_certifications
    )


# Hiring Communication
from flask_mail import Message
from flask import current_app
@company_blueprint.route('/company_hiring_communication', methods=['GET', 'POST'])
@login_required
def company_hiring_communication():
    mail = current_app.extensions['mail']
    user_id = session.get('login_id')
    
    if 'login_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.login'))  # Ensure only company can access

    # For the filter dropdown
    selected_status = request.args.getlist('status')  # Get selected status filters
    selected_jobs = request.args.getlist('job_post')  # Get selected job filters
    
    # For the search functionality
    search_query = request.args.get('search_query', '').strip()

    # Get all jobs created by the company
    jobs = Job.query.filter_by(created_by=user_id).all()

    # Fetch all users who applied for the company's jobs
    applied_users = (
        db.session.query(
            User.id, 
            User.name,
            User.login_id,  # Add this line to include login_id
            Job.title.label('job_title'), 
            JobApplication.status
        )
        .join(JobApplication, JobApplication.user_id == User.id)
        .join(Job, JobApplication.job_id == Job.job_id)
        .filter(Job.created_by == user_id)
        .order_by(User.id, JobApplication.id.desc())
        .distinct(User.id)
        .all()
    )
    
    if selected_status or selected_jobs or search_query:
        filtered_query = (
            db.session.query(User.id, User.name, User.login_id, Job.title.label('job_title'), JobApplication.status)
            .join(JobApplication, JobApplication.user_id == User.id)
            .join(Job, JobApplication.job_id == Job.job_id)
            .filter(Job.created_by == user_id)
        )
        
        if selected_status:
            filtered_query = filtered_query.filter(JobApplication.status.in_(selected_status))
        if selected_jobs:
            filtered_query = filtered_query.filter(Job.title.in_(selected_jobs))
        if search_query:
            filtered_query = filtered_query.filter(
                or_(
                    User.name.ilike(f'%{search_query}%'),
                    Job.title.ilike(f'%{search_query}%'),
                    JobApplication.status.ilike(f'%{search_query}%')
                )
            )

        applied_users = filtered_query.all()

    # Fetch communication history with structured data for JavaScript
    messages_query = (
        db.session.query(
            Communication, 
            db.case(
                (Communication.user_id.isnot(None), User.name),
                else_=College.college_name
            ).label("recipient_name"),
            db.case(
                (Communication.user_id.isnot(None), 'candidate'),
                else_='college'
            ).label("recipient_type"),
            db.case(
                (Communication.user_id.isnot(None), Communication.user_id),  # Change from User.login_id
                else_=Communication.college_id  # Change from College.login_id
            ).label("recipient_id")
        )
        .outerjoin(User, Communication.user_id == User.login_id)
        .outerjoin(College, Communication.college_id == College.login_id)
        .filter(Communication.company_id == user_id)
        .order_by(Communication.timestamp.desc())
    )
    
    messages = messages_query.all()

    colleges = College.query.all()

    # Message sending logic
    if request.method == 'POST':
        # Get data from form
        message_content = request.form.get('message')
        recipient_type = request.form.get('recipient_type')
        recipient_id = request.form.get('recipient_id')
        
        # Determine which ID to use based on recipient type
        if recipient_type == 'candidate':
            selected_user_id = recipient_id  # This is already the login_id
            selected_college_id = None
            
            # Get email directly using login_id
            recipient_email = db.session.query(User.email).filter_by(login_id=selected_user_id).scalar()
            new_user_id = selected_user_id  # Use login_id directly
            new_college_id = None
        else:
            selected_college_id = recipient_id
            selected_user_id = None
            
            # Get college email using login_id
            recipient_email = db.session.query(College.email).filter_by(login_id=selected_college_id).scalar()
            new_college_id = selected_college_id
            new_user_id = None
        
            
        sender_email = db.session.query(Company.email).filter_by(login_id=user_id).scalar()

        # Add message to the database
        if message_content:
            new_message = Communication(company_id=user_id, user_id=new_user_id, college_id=new_college_id, message=message_content)
            db.session.add(new_message)
            db.session.commit()

            # Send email notification
            try:
                subject = "New Message from Company"
                body = f"Dear Recipient,\n\nYou have received a new message from {sender_email}:\n\n{message_content}\n\nBest regards,\nYour Job Portal"
                msg = Message(subject=subject, recipients=[recipient_email])
                msg.body = body
                mail.send(msg)
            except Exception as e:
                print(f"Failed to send email: {e}")

            flash('Message sent successfully!', 'success')

        return redirect(url_for('company.company_hiring_communication'))
    
    message_history = {"candidates": {}}
    for msg, recipient_name, recipient_type, recipient_id in messages:
        if recipient_type == 'candidate':
            if recipient_id not in message_history["candidates"]:
                message_history["candidates"][recipient_id] = []
            
            # Format the message with necessary details
            message_entry = {
                "name": "Company" if msg.company_id == user_id else recipient_name,
                "message": msg.message,
                "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M")
            }
            message_history["candidates"][recipient_id].append(message_entry)


    profile = Company.query.filter_by(login_id=user_id).first()

    return render_template('/company/hiring_message.html', 
        applied_users=applied_users, 
        messages=messages, 
        profile=profile, 
        colleges=colleges,
        jobs=jobs,
        selected_status=selected_status,
        selected_jobs=selected_jobs,
        message_history=message_history
    )

# Notifications
@company_blueprint.route('/company_notification', methods=['GET', 'POST'])
@login_required
def company_notification():
    user_id = session.get('login_id')

    if 'login_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.login'))  # Ensure only companies can access

    if request.method == 'POST':
        notification_id = request.form.get('notification_id')
        action = request.form.get('action')

        if notification_id and action:
            notification = Notification.query.filter_by(id=notification_id, company_id=user_id).first()
            if notification:
                if action == 'mark_read':
                    notification.read_status = True
                    db.session.commit()
                    flash('Notification marked as read.', 'success')
                elif action == 'delete':
                    notification.hidden = True  # Soft delete
                    db.session.commit()
                    flash('Notification hidden successfully.', 'success')


    # Fetch notifications for the company
    notifications = Notification.query.filter_by(company_id=user_id,hidden=False).order_by(Notification.timestamp.desc()).all()
    
    pending_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Pending')\
        .scalar()

    interviewed_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Interviewed')\
        .scalar()

    jobs = Job.query.filter_by(created_by=user_id).all()

    applications = db.session.query(
    Job.title,
    db.func.count(JobApplication.id).label('total_applications'),
    db.func.sum(db.case(
                (JobApplication.status == 'Hired', 1),
                else_=0
            )).label('shortlisted_applications')
        ).join(JobApplication, Job.job_id == JobApplication.job_id).filter(Job.created_by == user_id).group_by(Job.title).all()

    total_applications = []
    shortlisted_applications = []
    for job in jobs:
        total_count = db.session.query(db.func.count(JobApplication.id)).filter_by(job_id=job.job_id).scalar() or 0
        shortlisted_count = db.session.query(db.func.count(JobApplication.id)).filter_by(job_id=job.job_id, status='shortlisted').scalar() or 0

        total_applications.append(total_count)
        shortlisted_applications.append(shortlisted_count)
    
    # Process data for the pie chart
    total_successful = sum(app.shortlisted_applications for app in applications)
    total_unsuccessful = sum(app.total_applications - app.shortlisted_applications for app in applications)

    # Fetch the company profile to display in the form
    companies = Company.query.filter_by(login_id=user_id).first()
    profile = Company.query.filter_by(login_id=user_id).first()

    # Fetch notifications within the past day for the live feed
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    live_feed_notifications = Notification.query.filter(
        Notification.company_id == user_id,
        Notification.hidden == False,
        Notification.timestamp >= one_day_ago
    ).order_by(Notification.timestamp.desc()).all()

    return render_template('/company/notification.html', notifications=notifications, profile=profile,
        pending_applications_count=pending_applications_count, total_successful=total_successful, 
        total_unsuccessful=total_unsuccessful, interviewed_applications_count=interviewed_applications_count,
        live_feed_notifications=live_feed_notifications)

# Profile
@company_blueprint.route('/company_profile', methods=['GET', 'POST'])
@login_required
def company_profile():
    user_id = session.get('login_id')

    if 'login_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.login'))  # Ensure only companies can access

    companies = Company.query.filter_by(login_id=user_id).first()

    message = None
    message_type = None

    if request.method == 'POST' and companies:
        # Get form data
        company_id = request.form.get('logId')  # Hidden input for company ID
        company_name = request.form['company-name'].strip()
        email = request.form['contact-email'].strip()
        description = request.form['company-description'].strip()
        address = request.form['company-address'].strip()
        website = request.form['company-website'].strip()
        logo = request.form['company-logo'].strip()
        industry = request.form['industries'].strip()

        # Check if any change is made
        if (
            company_name == companies.company_name and
            email == companies.email and
            description == companies.description and
            address == companies.address and
            website == companies.website and
            logo == companies.logo and
            industry == companies.industry
        ):
            return redirect(url_for('company.company_profile'))  # No changes, just reload page silently

        # Validate Data
        if not (3 <= len(company_name) <= 255):
            message = "Company Name must be between 3-255 characters!"
            message_type = "error"
        elif not re.match(r"^\S+@\S+\.\S+$", email):
            message = "Invalid email format!"
            message_type = "error"
        elif len(description) > 1000:
            message = "Description must be under 1000 characters!"
            message_type = "error"
        elif len(address) > 500:
            message = "Address must be under 500 characters!"
            message_type = "error"
        else:
            # Update the company profile
            companies.company_name = company_name
            companies.description = description
            companies.email = email
            companies.address = address
            companies.website = website
            companies.logo = logo
            companies.industry = industry
            db.session.commit()
            message = "Profile updated successfully!"
            message_type = "success"

    pending_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Pending')\
        .scalar()

    interviewed_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Interviewed')\
        .scalar()

    jobs = Job.query.filter_by(created_by=user_id).all()

    applications = db.session.query(
        Job.title,
        db.func.count(JobApplication.id).label('total_applications'),
        db.func.sum(db.case(
            (JobApplication.status == 'Hired', 1),
            else_=0
        )).label('shortlisted_applications')
    ).join(JobApplication, Job.job_id == JobApplication.job_id).filter(Job.created_by == user_id).group_by(Job.title).all()

    total_successful = sum(app.shortlisted_applications for app in applications)
    total_unsuccessful = sum(app.total_applications - app.shortlisted_applications for app in applications)

    # Fetch notifications within the past day for the live feed
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    live_feed_notifications = Notification.query.filter(
        Notification.company_id == user_id,
        Notification.hidden == False,
        Notification.timestamp >= one_day_ago
    ).order_by(Notification.timestamp.desc()).all()

    industries = [
        "Agriculture, Forestry, and Fishing",
        "Mining and Quarrying",
        "Manufacturing",
        "Electricity, Gas, Steam, and Air Conditioning Supply",
        "Water Supply; Sewerage, Waste Management, and Remediation Activities",
        "Construction",
        "Wholesale and Retail Trade; Repair of Motor Vehicles and Motorcycles",
        "Transportation and Storage",
        "Accommodation and Food Service Activities",
        "Information and Communication",
        "Financial and Insurance Activities",
        "Real Estate Activities",
        "Professional, Scientific, and Technical Activities",
        "Administrative and Support Service Activities",
        "Public Administration and Defence; Compulsory Social Security",
        "Education",
        "Human Health and Social Work Activities",
        "Arts, Entertainment, and Recreation",
        "Other Service Activities",
        "Activities of Households as Employers",
        "Activities of Extraterritorial Organizations and Bodies"
    ]

    return render_template('/company/profile.html', companies=companies, profile=companies, login_id=user_id,
        pending_applications_count=pending_applications_count, total_successful=total_successful, 
        total_unsuccessful=total_unsuccessful, interviewed_applications_count=interviewed_applications_count,
        live_feed_notifications=live_feed_notifications, industries=industries, message=message, 
        message_type=message_type)
