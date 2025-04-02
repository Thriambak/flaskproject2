from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from functools import wraps
import os
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
# from models import Job, JobApplication, db,User,ResumeCertification, Notification
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db  # Ensure 'db' is the instance of SQLAlchemy
# Assuming your model is in 'models.py'
from config import Config
from utils import allowed_file  # Assuming your config file is named config.py
from models import Job, Company, Login, JobApplication, User, Communication, Notification, College, Certification, ResumeCertification


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
    
    # print("\n\n",session['login_id'],session['username'],session['role'],"\n\n")

    # Query to fetch all jobs (or filter by user_id for jobs posted by the user)
    # jobs = Job.query.all()  # If you want to show all jobs. If you need jobs posted by the user, filter by created_by 
    
    jobs = Job.query.filter_by(created_by=user_id).all()  # Uncomment this to only show jobs posted by the user
    profile = Company.query.filter_by(login_id=user_id).first()
    
    pending_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Pending')\
        .scalar()

    interviewed_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Interviewed')\
        .scalar()

    '''print("Pending count:",pending_applications_count)
    print("Interviewed count:",interviewed_applications_count)'''

    # Fetch the application data
    applications = db.session.query(
    Job.title,
    db.func.count(JobApplication.id).label('total_applications'),
    db.func.sum(db.case(
                (JobApplication.status == 'Hired', 1),
                else_=0
            )).label('shortlisted_applications')
        ).join(JobApplication, Job.job_id == JobApplication.job_id).filter(Job.created_by == user_id).group_by(Job.title).all()



    # Process data for the bar graph
    labels = [job.title for job in jobs]
    total_applications = []
    shortlisted_applications = []

    for job in jobs:
        total_count = db.session.query(db.func.count(JobApplication.id)).filter_by(job_id=job.job_id).scalar() # or 0
        shortlisted_count = db.session.query(db.func.count(JobApplication.id)).filter_by(job_id=job.job_id, status='Hired').scalar() # or 0

        total_applications.append(total_count)
        shortlisted_applications.append(shortlisted_count)
    
    # Process data for the pie chart
    total_successful = sum(app.shortlisted_applications for app in applications)
    total_unsuccessful = sum(app.total_applications - app.shortlisted_applications for app in applications)

    # Ensure the user is not an admin (or redirect to the admin dashboard)
    if session.get('role') != 'company':
        return redirect(url_for('admin.admin_dashboard'))

    # Fetch notifications within the past day for the live feed
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    live_feed_notifications = Notification.query.filter(
        Notification.company_id == user_id,
        Notification.hidden == False,
        Notification.timestamp >= one_day_ago
    ).order_by(Notification.timestamp.desc()).all()
    
    return render_template('/company/dashboard.html', jobs=jobs, profile=profile, labels=labels,
        total_applications=total_applications, shortlisted_applications=shortlisted_applications,
        total_successful=total_successful, total_unsuccessful=total_unsuccessful,
        pending_applications_count=pending_applications_count, live_feed_notifications=live_feed_notifications,
        interviewed_applications_count=interviewed_applications_count)

# Job Posting
@company_blueprint.route('/company_jobposting')
@login_required
def company_jobposting():
    from app import db
    user_id = session.get('login_id')
    # Retrieve all jobs
    jobs = Job.query.filter_by(created_by=user_id).order_by(Job.created_at.desc()).all()
    profile = Company.query.filter_by(login_id=user_id).first()


    applications = db.session.query(
    Job.title,
    db.func.count(JobApplication.id).label('total_applications'),
    db.func.sum(db.case(
                (JobApplication.status == 'Hired', 1), else_=0
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

    pending_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Pending')\
        .scalar()

    interviewed_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Interviewed')\
        .scalar()
    
    # Fetch notifications within the past day for the live feed
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    live_feed_notifications = Notification.query.filter(
        Notification.company_id == user_id,
        Notification.hidden == False,
        Notification.timestamp >= one_day_ago
    ).order_by(Notification.timestamp.desc()).all()

    return render_template('/company/job_posting.html', jobs=jobs, profile=profile,
        total_successful=total_successful, total_unsuccessful=total_unsuccessful,
        pending_applications_count=pending_applications_count, live_feed_notifications=live_feed_notifications,
        interviewed_applications_count=interviewed_applications_count)

# Post New Job
@company_blueprint.route('/company_post_new_job', methods=['GET','POST'])
@login_required
def company_post_new_job():
    from app import db
    user_id = session.get('login_id')

    if 'login_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.login'))  # Ensure only admins can access

    if request.method == 'POST':
        # Get form data
        job_id = request.form.get('jobId')
        title = request.form['job-title']
        description = request.form['description']
        skills = request.form['skill-sets']
        exp = request.form['exp']
        certifications = request.form['certifications']
        job_type = request.form['job-type']
        locations = request.form['locations']
        salary = request.form['salary']
        total_vacancy = request.form['vacancy']
        form_url = request.form.get('form-url')
        deadline_str = request.form['deadline']
        created_by = session['login_id']  # Get admin's user ID from session
        total_vacancy = int(total_vacancy)
        filled_vacancy = 0

        status = "open" if total_vacancy > filled_vacancy else "closed"

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
                job.years_of_exp = exp
                job.certifications = certifications
                job.locations = locations
                job.salary = salary
                job.total_vacancy = total_vacancy
                job.deadline = deadline
                job.form_url = form_url
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
                years_of_exp = exp,
                certifications = certifications,
                location=locations,
                salary=salary,
                total_vacancy=total_vacancy,
                filled_vacancy=filled_vacancy,
                status=status,
                form_url=form_url,
                deadline=deadline,
                created_by=created_by
            )
            print(title)
            db.session.add(new_job)
            db.session.commit()
            flash('Job added successfully!', 'success')

        return redirect(url_for('company.company_jobposting'))

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

    pending_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Pending')\
        .scalar()

    interviewed_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Interviewed')\
        .scalar()
    
    # Fetch notifications within the past day for the live feed
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    live_feed_notifications = Notification.query.filter(
        Notification.company_id == user_id,
        Notification.hidden == False,
        Notification.timestamp >= one_day_ago
    ).order_by(Notification.timestamp.desc()).all()

    # Retrieve all jobs
    # jobs = Job.query.all()
    current_date = date.today().strftime('%Y-%m-%d')   # Get today's date in 'DD-MM-YYYY' format
    profile = Company.query.filter_by(login_id=user_id).first()
    return render_template('/company/post_new_job.html',current_date=current_date, profile=profile,
        total_successful=total_successful, total_unsuccessful=total_unsuccessful,
        pending_applications_count=pending_applications_count, live_feed_notifications=live_feed_notifications,
        interviewed_applications_count=interviewed_applications_count)

# Application Review
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

    search_name = request.args.get('search_name', '').strip()  # Get the search name
    selected_status = request.args.getlist('status')  # Get selected status filters
    selected_jobs = request.args.getlist('job_post')  # Get selected job filters

    # Get all jobs created by the company
    jobs = Job.query.filter_by(created_by=user_id).all()
    
    # Query all job applications for the company's jobs
    query = JobApplication.query.join(Job).filter(Job.created_by == user_id)

    # Apply search filters
    if search_name:
        query = query.join(User).filter(User.name.ilike(f'%{search_name}%'))
    if selected_status:
        query = query.filter(JobApplication.status.in_(selected_status))
    if selected_jobs:
        query = query.filter(Job.title.in_(selected_jobs))

    # Get all job applications for the jobs created by the company
    job_applications = query.all()
    
    # Create a list of applications with details for rendering (including user_id)
    applications_data = []
    for application in job_applications:
        # Fetch the latest resume for this user from ResumeCertification
        resume = ResumeCertification.query.filter_by(user_id=application.user_id).order_by(ResumeCertification.id.desc()).first()
        resume_path = resume.resume_path if resume else None
        
        applications_data.append({
            'candidate_name': application.user.name,
            'job_post': application.job.title,
            'status': application.status,
            'application_id': application.id,  # Include application ID
            'resume_path': resume_path,        # Use resume_path from ResumeCertification
            'user_id': application.user_id     # Include user_id for certifications lookup
        })
    
    applications = db.session.query(
        Job.title,
        db.func.count(JobApplication.id).label('total_applications'),
        db.func.sum(db.case(
                (JobApplication.status == 'Hired', 1),
                else_=0
            )).label('shortlisted_applications')
    ).join(JobApplication, Job.job_id == JobApplication.job_id)\
     .filter(Job.created_by == user_id)\
     .group_by(Job.title).all()

    total_successful = sum(app.shortlisted_applications for app in applications)
    total_unsuccessful = sum(app.total_applications - app.shortlisted_applications for app in applications)

    pending_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Pending')\
        .scalar()

    interviewed_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Interviewed')\
        .scalar()
    
    # Fetch certifications for each candidate application
    user_certifications = {}
    for application in job_applications:
        if application.user_id not in user_certifications:
            certifications = Certification.query.filter_by(user_id=application.user_id).all()
            cert_data = []
            for cert in certifications:
                cert_data.append({
                    'certification_name': cert.certification_name,
                    'verified': cert.verification_status
                })
            user_certifications[application.user_id] = cert_data

    # Fetch notifications within the past day for the live feed
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    live_feed_notifications = Notification.query.filter(
        Notification.company_id == user_id,
        Notification.hidden == False,
        Notification.timestamp >= one_day_ago
    ).order_by(Notification.timestamp.desc()).all()

    profile = Company.query.filter_by(login_id=user_id).first()
    return render_template('/company/application_review.html', 
                           applications=applications_data, 
                           profile=profile, 
                           search_name=search_name, 
                           selected_status=selected_status, 
                           jobs=jobs,
                           selected_jobs=selected_jobs, 
                           total_successful=total_successful, 
                           total_unsuccessful=total_unsuccessful,
                           pending_applications_count=pending_applications_count, 
                           live_feed_notifications=live_feed_notifications,
                           interviewed_applications_count=interviewed_applications_count,
                           user_certifications=user_certifications)


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
        db.session.query(
            Communication, 
            db.case(
                (Communication.user_id.isnot(None), User.name),  # Fixed argument passing
                else_=College.college_name
            ).label("recipient_name")
        )
        .outerjoin(User, Communication.user_id == User.login_id)
        .outerjoin(College, Communication.college_id == College.login_id)
        .filter(Communication.company_id == user_id)
        .order_by(Communication.timestamp.desc())
        .all()
    )

    colleges = College.query.all()

    if request.method == 'POST':
        # Get data from form
        selected_user_id = request.form.get('user_id')
        selected_college_id = request.form.get('college_id')
        message_content = request.form.get('message')
        # print("\nId conflicts:",selected_user_id,selected_college_id,message_content,"\n")

        # Fetch recipient and sender email
        if selected_college_id == None:
            recipient_email = db.session.query(User.email).filter_by(id=selected_user_id).scalar()
            new_user_id = db.session.query(User.login_id).filter_by(id=selected_user_id).scalar()
        elif selected_user_id == None:
            recipient_email = db.session.query(College.email).filter_by(id=selected_college_id).scalar()
            new_user_id = db.session.query(College.login_id).filter_by(id=selected_college_id).scalar()
        sender_email = db.session.query(Company.email).filter_by(login_id=user_id).scalar()

        
        # Debug
        '''
        print("User:",new_user_id)
        print(f"Company ID: {user_id}")
        print(f"Selected User ID: {selected_user_id}")
        print(f"New User ID: {new_user_id}")
        print(f"Message Content: {message_content}")'''

        # Add message to the database
        if selected_user_id and message_content:
            new_message = Communication(company_id=user_id, user_id=new_user_id, college_id=None, message=message_content)
            db.session.add(new_message)
            db.session.commit()

            # Send email notification
            try:
                subject = "New Message from Company"
                body = f"Dear Candidate,\n\nYou have received a new message from {sender_email}:\n\n{message_content}\n\nBest regards,\nYour Job Portal"
                msg = Message(subject=subject, recipients=[recipient_email])
                msg.body = body
                mail.send(msg)
            except Exception as e:
                print(f"Failed to send email: {e}")

            flash('Message sent successfully!', 'success')

        elif selected_college_id and message_content:
            new_message = Communication(company_id=user_id, user_id=None, college_id=new_user_id, message=message_content)
            db.session.add(new_message)
            db.session.commit()

            # Send email notification
            try:
                subject = "New Message from Company"
                body = f"Dear Candidate,\n\nYou have received a new message from {sender_email}:\n\n{message_content}\n\nBest regards,\nYour Job Portal"
                msg = Message(subject=subject, recipients=[recipient_email])
                msg.body = body
                mail.send(msg)
            except Exception as e:
                print(f"Failed to send email: {e}")

            flash('Message sent successfully!', 'success')

        return redirect(url_for('company.company_hiring_communication'))


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

    pending_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Pending')\
        .scalar()

    interviewed_applications_count = db.session.query(db.func.count(JobApplication.id))\
        .join(Job, JobApplication.job_id == Job.job_id)\
        .filter(Job.created_by == user_id, JobApplication.status == 'Interviewed')\
        .scalar()
    
    # Fetch notifications within the past day for the live feed
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    live_feed_notifications = Notification.query.filter(
        Notification.company_id == user_id,
        Notification.hidden == False,
        Notification.timestamp >= one_day_ago
    ).order_by(Notification.timestamp.desc()).all()

    profile = Company.query.filter_by(login_id=user_id).first()
    return render_template('/company/hiring_message.html', applied_users=applied_users, messages=messages, 
    profile=profile, total_successful=total_successful, total_unsuccessful=total_unsuccessful,
    pending_applications_count=pending_applications_count, live_feed_notifications=live_feed_notifications,
    interviewed_applications_count=interviewed_applications_count, colleges=colleges)

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

    return render_template('/company/profile.html', companies=companies, login_id=user_id, profile=profile,
        pending_applications_count=pending_applications_count, total_successful=total_successful, 
        total_unsuccessful=total_unsuccessful, interviewed_applications_count=interviewed_applications_count,
        live_feed_notifications=live_feed_notifications)

