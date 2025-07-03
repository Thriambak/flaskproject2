from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for, flash
from flask_login import current_user
from config import Config
from functools import wraps
import os
from werkzeug.utils import secure_filename
from models import Certification, Company, Coupon, Couponuser, Job, JobApplication, Login,User,ResumeCertification, Notification #, JobApplication
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os, uuid
from models import db  # Ensure 'db' is the instance of SQLAlchemy
  # Assuming your model is in 'models.py'
from config import Config
from utils import allowed_file  # Assuming your config file is named config.py
from datetime import datetime

user_blueprint = Blueprint('user', __name__)
from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
from flask import request  # Ensure this is imported at the top

@user_blueprint.route('/user_dashboard')
@login_required
def user_dashboard():
    login_id = session.get('login_id')  # Use 'login_id' instead of 'user_id'
    if not login_id:
        flash("User not logged in", "error")
        return redirect(url_for('auth.login'))
   
    # Ensure that only regular users access this page
    if session.get('role') != 'user':
        return redirect(url_for('auth.login'))
   
    # Get the User object using login_id from the Login table
    user = User.query.filter_by(login_id=login_id).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for('auth.login'))
    user_id = user.id  # This is the User table's id, used for job application queries
   
    db.session.commit()
    db.session.expire_all()  # Forces fresh query results
    
    # Paginate the jobs query with filters
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Adjust as needed
    
    # Query jobs with filters:
    # 1. Exclude jobs where vacancy is full (filled_vacancy >= total_vacancy)
    # 2. Exclude jobs from banned companies
    # 3. Only show active jobs
    jobs_query = Job.query.join(Login, Job.created_by == Login.id)\
        .join(Company, Login.id == Company.login_id)\
        .filter(
            Job.filled_vacancy < Job.total_vacancy,  # Not fully filled
            Company.is_banned == False,  # Company not banned
            Job.status == 'open'  # Job is active
        )\
        .order_by(Job.created_at.desc())
    
    jobs_pagination = jobs_query.paginate(page=page, per_page=per_page, error_out=False)
    jobs = jobs_pagination.items
    total_pages = jobs_pagination.pages
    
    # Get user's applied jobs
    applied_jobs = db.session.query(JobApplication.job_id)\
        .filter(JobApplication.user_id == user_id)\
        .subquery()
    
    # Get user's saved jobs
    saved_jobs = db.session.query(Favorite.job_id)\
        .filter(Favorite.user_id == user_id)\
        .subquery()
    
    # Create sets for easier lookup in template
    applied_job_ids = {str(app.job_id) for app in JobApplication.query.filter_by(user_id=user_id).all()}
    saved_job_ids = {str(saved.job_id) for saved in Favorite.query.filter_by(user_id=user_id).all()}
    
    # Remove chart data; only upcoming events and notifications remain
    current_date = datetime.utcnow()
    upcoming_events = db.session.query(Job.title, Job.deadline)\
        .join(JobApplication, Job.job_id == JobApplication.job_id)\
        .filter(JobApplication.user_id == user_id, Job.deadline > current_date)\
        .order_by(Job.deadline.asc()).all()
    recent_notifications = Notification.query.filter_by(user_id=user_id, hidden=False)\
        .order_by(Notification.timestamp.desc()).limit(5).all()
   
    return render_template('/user/user_dashboard.html',
                           jobs=jobs,
                           upcoming_events=upcoming_events,
                           recent_notifications=recent_notifications,
                           page=page,
                           total_pages=total_pages,
                           applied_job_ids=applied_job_ids,
                           saved_job_ids=saved_job_ids)
from datetime import datetime

from models import db, User, Job, JobApplication, ResumeCertification, Notification

@user_blueprint.route('/apply_for_job/<uuid:job_id>', methods=['POST'])

def apply_for_job(job_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)  

    if not user:
        flash("User not found.", 'error')
        return redirect(url_for('user.user_dashboard'))

    # Fetch the job that the user is applying for
    job = Job.query.get(job_id)

    if not job:
        flash("Job not found.", 'error')
        return redirect(url_for('user.user_dashboard'))
    
    if job.status=='closed':
        flash("Applications have been closed for this job.", 'error')
        return redirect(url_for('user.user_dashboard'))

    # Fetch the user's resume from the ResumeCertification table
    resume_certification = ResumeCertification.query.filter_by(user_id=user.id).first()
    
    if not resume_certification or not resume_certification.resume_path:
        flash("You must upload a resume to apply for a job.", 'error')
        return redirect(url_for('user.resume_certifications'))

    print("Debugging: Resume Path:", resume_certification.resume_path)  # ✅ Debugging Output

    # Check if the user has already applied for this job
    existing_application = JobApplication.query.filter_by(user_id=user.id, job_id=job_id).first()
    if existing_application:
        flash(f"You have already applied for the job {job.title}.", 'error')
        return redirect(url_for('user.user_dashboard'))

    # ✅ Ensure date_applied and status_updated_at are set properly
    new_application = JobApplication(
        user_id=user.id,
        job_id=job.job_id,
        status='Pending',  
        resume_path=resume_certification.resume_path,
        
    )

    # ✅ Send notification to company
    message = f"{user.name} has applied for the job: {job.title}"
    new_notification = Notification(
        user_id=user.login_id,
        company_id=job.created_by,
        message=message
    )

    # Add and commit changes to the database
    db.session.add(new_application)
    db.session.add(new_notification)
    db.session.commit()

    flash(f"Application for {job.title} submitted successfully!", 'success')

    return redirect(url_for('user.user_dashboard'))

@user_blueprint.route('/apply1_for_job/<uuid:job_id>', methods=['POST'])

def apply1_for_job(job_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)  

    if not user:
        flash("User not found.", 'error')
        return redirect(url_for('user.user_dashboard'))

    # Fetch the job that the user is applying for
    job = Job.query.get(job_id)

    if not job:
        flash("Job not found.", 'error')
        return redirect(url_for('user.job_search'))
    
    # Fetch the user's resume from the ResumeCertification table
    resume_certification = ResumeCertification.query.filter_by(user_id=user.id).first()
    
    if not resume_certification or not resume_certification.resume_path:
        flash("You must upload a resume to apply for a job.", 'error')
        return redirect(url_for('user.resume_certifications'))

    print("Debugging: Resume Path:", resume_certification.resume_path)  # ✅ Debugging Output

    # Check if the user has already applied for this job
    existing_application = JobApplication.query.filter_by(user_id=user.id, job_id=job_id).first()
    if existing_application:
        flash(f"You have already applied for the job {job.title}.", 'danger')
        return redirect(url_for('user.job_search'))

    # ✅ Ensure date_applied and status_updated_at are set properly
    new_application = JobApplication(
        user_id=user.id,
        job_id=job.job_id,
        status='Pending',  
        resume_path=resume_certification.resume_path,
        
    )

    # ✅ Send notification to company
    message = f"{user.name} has applied for the job: {job.title}"
    new_notification = Notification(
        user_id=user.login_id,
        company_id=job.created_by,
        message=message
    )

    # Add and commit changes to the database
    db.session.add(new_application)
    db.session.add(new_notification)
    db.session.commit()

    flash(f"Application for {job.title} submitted successfully!", 'success')

    return redirect(url_for('user.job_search'))
from datetime import datetime, timedelta
import pytz
def get_chart_data_for_user(user_id):
    """
    Retrieves dynamic chart data, recent activities, and live feed for the given user.
    Returns four items:
      - user_success_rate: counts of applications by status (hired, rejected, pending, interviewed)
      - application_trends: daily count of applications (as a trend over time) - LIMITED TO LAST 5 DAYS
      - recent_activities: list of user's recent job applications
      - live_feed: list of recent job postings
    """
    # Define IST timezone
    ist_timezone = pytz.timezone('Asia/Kolkata')
    
    # Chart data: User success rate
    hired = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'Hired').scalar() or 0
    rejected = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'Rejected').scalar() or 0
    pending = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'Pending').scalar() or 0
    interviewed = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'Interviewed').scalar() or 0
    
    user_success_rate = {"hired": hired, "rejected": rejected, "pending": pending, "interviewed": interviewed}
    
    # Chart data: Application trends (daily count) - LIMITED TO LAST 5 DAYS
    # Calculate the date 5 days ago from today
    today = datetime.now(ist_timezone).date()
    five_days_ago = today - timedelta(days=4)  # 4 days ago + today = 5 days total
    
    # Query for application trends in the last 5 days
    trend_data = db.session.query(
        db.func.date(JobApplication.date_applied).label('date'),
        db.func.count(JobApplication.id).label('count')
    ).filter(
        JobApplication.user_id == user_id,
        db.func.date(JobApplication.date_applied) >= five_days_ago
    ).group_by(db.func.date(JobApplication.date_applied))\
     .order_by(db.func.date(JobApplication.date_applied)).all()
    
    # Create a complete list of the last 5 days (including days with 0 applications)
    date_range = []
    count_range = []
    
    for i in range(5):
        current_date = five_days_ago + timedelta(days=i)
        date_range.append(current_date.strftime('%Y-%m-%d'))
        
        # Find if there's data for this date
        count_for_date = 0
        for row in trend_data:
            if row.date == current_date:
                count_for_date = row.count
                break
        count_range.append(count_for_date)
    
    application_trends = {"labels": date_range, "counts": count_range}
    
    # Recent activities: Last 5 job applications by the user
    recent_activities = db.session.query(JobApplication, Job.title)\
        .join(Job, Job.job_id == JobApplication.job_id)\
        .filter(JobApplication.user_id == user_id)\
        .order_by(JobApplication.id.desc())\
        .limit(5).all()
    recent_activities_list = [
        {'job_title': job_title, 'status': app.status}
        for app, job_title in recent_activities
    ]
    
    # Live feed: Last 5 job postings - Pass UTC timestamps for frontend conversion
    live_feed = db.session.query(Job)\
        .order_by(Job.created_at.desc())\
        .limit(5).all()
    
    live_feed_list = []
    for job in live_feed:
        if job.created_at:
            # Ensure we have a UTC datetime for consistent frontend conversion
            if job.created_at.tzinfo is None:
                # If datetime is naive, assume it's UTC
                utc_datetime = pytz.utc.localize(job.created_at)
            else:
                # If datetime is aware, convert to UTC
                utc_datetime = job.created_at.astimezone(pytz.utc)
            
            # Pass the UTC datetime to frontend for conversion
            live_feed_list.append({
                'job_title': job.title, 
                'posted_at': utc_datetime
            })
        else:
            live_feed_list.append({
                'job_title': job.title, 
                'posted_at': None
            })
    
    return user_success_rate, application_trends, recent_activities_list, live_feed_list

@user_blueprint.route('/analytics')
@login_required
def analytics():
    user_id = session.get('user_id')
    user_success_rate, application_trends, recent_activities, live_feed = get_chart_data_for_user(user_id)
    return render_template(
        '/user/analytics.html',
        user_success_rate=user_success_rate,
        application_trends=application_trends,
        recent_activities=recent_activities,
        live_feed=live_feed
    )
from flask import session, render_template, flash, redirect, url_for
from models import Communication, User, db  # make sure db is imported from your app

@user_blueprint.route('/notifications', methods=['GET'])
def notifications():
    # Retrieve the primary key from the session (User.id)
    user_pk = session.get('user_id')
    if not user_pk:
        flash("Please log in to view notifications.", "danger")
        return redirect(url_for('auth.login'))

    # Retrieve the user record to get the user's login_id (which is stored in the Communication table)
    user = User.query.get(user_pk)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Use the user's login_id for querying communications and filter out hidden ones if needed.
    notifications = Communication.query.filter_by(user_id=user.login_id, hidden=False)\
        .order_by(Communication.timestamp.desc()).all()
    unread_count = Communication.query.filter_by(user_id=user.login_id, read_status=False, hidden=False).count()

    return render_template(
        '/user/notification.html',
        notifications=notifications,
        unread_count=unread_count
    )
@user_blueprint.route('/mark_notification_read/<uuid:notification_id>', methods=['POST'], endpoint='mark_single_notification_read')
def mark_notification_read(notification_id):
    # Your code for marking a single notification as read...


    user_pk = session.get('user_id')
    if not user_pk:
        flash("Please log in.", "danger")
        return redirect(url_for('auth.login'))
    
    # Retrieve user record to get the correct login_id
    user = User.query.get(user_pk)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Retrieve the specific notification and verify ownership using user.login_id
    notification = Communication.query.filter_by(
        id=notification_id, 
        user_id=user.login_id, 
        hidden=False
    ).first()
    
    if notification:
        notification.read_status = True
        db.session.commit()
        
    else:
        flash("Notification not found.", "danger")
    
    return redirect(url_for('user.notifications'))

@user_blueprint.route('/delete_notification/<uuid:notification_id>', methods=['POST'])
def delete_notification(notification_id):
    user_pk = session.get('user_id')
    if not user_pk:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_pk)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Retrieve the specific notification belonging to this user that is not already hidden
    notification = Communication.query.filter_by(
        id=notification_id, 
        user_id=user.login_id, 
        hidden=False
    ).first()
    
    if notification:
        notification.hidden = True  # Soft-delete by marking as hidden
        db.session.commit()
        flash("Notification removed.", "success")
    else:
        flash("Notification not found.", "danger")
    
    return redirect(url_for('user.notifications'))

@user_blueprint.route('/resume_certifications', methods=['GET', 'POST'])
@login_required
def resume_certifications():
    # Ensure the user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to access this page.', 'error')
        return redirect(url_for('auth.login'))

    # Fetch user data
    user = User.query.get(user_id)
    print(user_id, user)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Check if the form submission is for a resume or a certification
        if 'resume' in request.files:
            # Handle Resume Upload
            upload_folder = os.path.join('static', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            resume = request.files.get('resume')
            if resume and allowed_file(resume.filename):
                resume_filename = secure_filename(resume.filename)
                resume_path = os.path.join(upload_folder, f"resume_{user.name}_{resume_filename}")
                resume.save(resume_path)
                resume_path = resume_path.replace('\\', '/')  # Normalize path for web use

                # Save Resume Entry
                resume_entry = ResumeCertification(user_id=user.id, resume_path=resume_path)
                db.session.add(resume_entry)
                db.session.commit()
                flash('Resume uploaded successfully!', 'success')

        elif 'certification_name' in request.form:
            # Handle Certification/Skill Additions
            certification_name = request.form.get('certification_name').strip()
            if certification_name:
                certification = Certification(
                    user_id=user.id,
                    certification_name=certification_name,
                    verification_status=False
                )
                db.session.add(certification)
                db.session.commit()
                flash(f'Certification "{certification_name}" added successfully!', 'success')

        return redirect(url_for('user.resume_certifications'))

    # Retrieve dynamic chart data, recent activities, and live feed using the helper function
    user_success_rate, applications_overview, recent_activities, live_feed = get_chart_data_for_user(user_id)

    # Retrieve data for display
    resumes = ResumeCertification.query.filter_by(user_id=user_id).all()
    certifications = Certification.query.filter_by(user_id=user_id).all()

    return render_template(
        '/user/resume_certifications.html',
        resume_certifications=resumes,
        certifications=certifications,
        user_success_rate=user_success_rate,
        applications_overview=applications_overview,
        recent_activities=recent_activities,
        live_feed=live_feed
    )
@user_blueprint.route('/application_history', methods=['GET'])
@login_required
def application_history():
    user_id = session.get('user_id')
    
    if not user_id:
        flash("User is not logged in.", "error")
        return redirect(url_for('auth.login'))

    # Fetch all applications for the logged-in user
    applications = JobApplication.query.filter_by(user_id=user_id).all()
    
    # Retrieve chart data, recent activities, and live feed using the common helper function
    user_success_rate, applications_overview, recent_activities, live_feed = get_chart_data_for_user(user_id)

    # Render the template with the application data, chart data, recent activities, and live feed
    return render_template('/user/applicationhistory.html',
        applications=applications,
        user_success_rate=user_success_rate,
        applications_overview=applications_overview,
        recent_activities=recent_activities,
        live_feed=live_feed
    )

from sqlalchemy import or_

from sqlalchemy import or_

from sqlalchemy import or_

from sqlalchemy import or_
@user_blueprint.route('/job_search', methods=['GET', 'POST'])
def job_search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        location = request.form.get('location')
        job_type = request.form.get('job_type')
        years_of_exp = request.form.get('years_of_exp')
        salary = request.form.get('salary')
        deadline = request.form.get('deadline')
       
        query = Job.query
       
        if keyword:
            query = query.filter(
                or_(
                    Job.title.ilike(f'%{keyword}%'),
                    Job.description.ilike(f'%{keyword}%'),
                    Job.skills.ilike(f'%{keyword}%'),
                    Job.certifications.ilike(f'%{keyword}%')
                )
            )
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))
        if job_type:
            # Using ilike ensures "full-time" (or variations) match the stored value.
            query = query.filter(Job.job_type.ilike(f'%{job_type}%'))
        if years_of_exp:
            query = query.filter(Job.years_of_exp == int(years_of_exp))
        if salary:
            query = query.filter(Job.salary <= salary)
        if deadline:
            query = query.filter(Job.deadline <= deadline)
       
        jobs = query.order_by(Job.created_at.desc()).all()
        
        # Get current user's ID from session
        current_user_id = session.get('user_id')
        
        # Get jobs the user has already applied to
        applied_applications = JobApplication.query.filter_by(user_id=current_user_id).all()
        applied_jobs = {app.job_id for app in applied_applications}
        
        # Get jobs the user has already saved (assuming Favorite table exists)
        # You'll need to import the Favorite model at the top of your file
        saved_favorites = Favorite.query.filter_by(user_id=current_user_id).all()
        saved_jobs = {fav.job_id for fav in saved_favorites}
        
        return render_template('/user/jobresults.html', 
                             jobs=jobs, 
                             applied_jobs=applied_jobs, 
                             saved_jobs=saved_jobs)
    else:
        return render_template('/user/jobsearch.html')

@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to access your profile.', 'error')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('user.user_dashboard'))
    
    resumes = ResumeCertification.query.filter_by(user_id=user_id).all()
    certifications = Certification.query.filter_by(user_id=user_id).all()
    
    # Get user's coupon information if they have one
    user_coupon_mapping = Couponuser.query.filter_by(user_id=user_id).first()
    user_coupon = None
    if user_coupon_mapping:
        user_coupon = Coupon.query.filter_by(id=user_coupon_mapping.coupon_id).first()
    
    # Other data for charts, etc.
    edit_mode = request.args.get('edit', 'false').lower() == 'true'
    
    if request.method == 'POST':
        # Handle college name and coupon code FIRST
        manual_college = request.form.get('college_name', '').strip()
        coupon_code = request.form.get('coupon_code', "").strip()
        
        # Only process new coupon codes if user doesn't already have one
        if coupon_code and not user_coupon:
            coupon = Coupon.query.filter_by(code=coupon_code).first()
            if not coupon:
                # Invalid coupon - don't save profile and stay in edit mode
                flash("Invalid coupon code provided.", "error")
                return render_template('/user/profile.html',
                                       user=user,
                                       resumes=resumes,
                                       certifications=certifications,
                                       user_coupon=user_coupon,
                                       edit_mode=True)
            else:
                # Valid coupon - proceed with coupon logic
                existing_mapping = Couponuser.query.filter_by(user_id=user_id, coupon_id=coupon.id).first()
                if not existing_mapping:
                    new_mapping = Couponuser(user_id=user_id, coupon_id=coupon.id)
                    db.session.add(new_mapping)
                    
                # Set college name from coupon if available
                if coupon.college:
                    user.college_name = coupon.college.college_name
                else:
                    user.college_name = manual_college or user.college_name
                    
                flash("Coupon code applied successfully!", "success")
        elif user_coupon:
            # User already has a coupon, don't allow changes to coupon-controlled fields
            if user_coupon.college:
                # College is controlled by coupon, don't change it
                user.college_name = user_coupon.college.college_name
            else:
                # College can still be manually set if coupon doesn't specify it
                user.college_name = manual_college or user.college_name
        else:
            # No coupon code provided and user doesn't have one, use manual college
            user.college_name = manual_college or user.college_name
        
        # Update other fields only if coupon validation passed
        user.phone = request.form.get('phone', user.phone)
        age_input = request.form.get('age', '')
        if age_input:
            try:
                user.age = int(age_input)
            except ValueError:
                flash("Invalid age provided.", "error")
                return redirect(url_for('user.profile', edit='true'))
        user.about_me = request.form.get('about_me', user.about_me)
        
        # Profile picture URL update
        profile_pic_url = request.form.get('profile_pic_url')
        if profile_pic_url:
            user.profile_picture = profile_pic_url
        
        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for('user.profile'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating profile: {str(e)}", "error")
            return redirect(url_for('user.profile', edit='true'))
    
    return render_template('/user/profile.html',
                           user=user,
                           resumes=resumes,
                           certifications=certifications,
                           user_coupon=user_coupon,
                           edit_mode=edit_mode)
from flask import jsonify

@user_blueprint.route('/get_application_details/<uuid:application_id>', methods=['GET'])
def get_application_details(application_id):
    application = JobApplication.query.get(application_id)
    
    if not application:
        return jsonify({"error": "Application not found"}), 404

    print("Debug - Application Found:", application)  # ✅ Debugging Output
    print("Debug - Date Applied:", application.date_applied)
    print("Debug - Status Updated:", application.status_updated_at)

    application_data = {
        "jobTitle": application.job.title,
        "company": application.job.company_name,
        "status": application.status,
        "resumePath": application.resume_path if application.resume_path else None,
        "dateApplied": application.date_applied.strftime('%Y-%m-%d %H:%M:%S') if application.date_applied else None,
        "dateStatusChanged": application.status_updated_at.strftime('%Y-%m-%d %H:%M:%S') if application.status_updated_at else None
    }

    print("Debug - JSON Response:", application_data)  # ✅ Debugging Output

    return jsonify(application_data)

from models import User, Job, Favorite
from datetime import datetime



# Save Job Route
@user_blueprint.route('/save_job1/<uuid:job_id>', methods=['POST'])

def save_job1(job_id):
    login_id = session.get('login_id')
    if not login_id:
        flash("User not logged in", "error")
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(login_id=login_id).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for('auth.login'))
    
    # Check if job is already saved
    existing_favorite = Favorite.query.filter_by(user_id=user.id, job_id=job_id).first()
    if existing_favorite:
        flash("Job already saved", "info")
        return redirect(url_for('user.user_dashboard'))
    
    # Create new favorite entry
    new_favorite = Favorite(user_id=user.id, job_id=job_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    flash("Job saved to favorites", "success")
    return redirect(url_for('user.job_search'))

@user_blueprint.route('/save_job/<uuid:job_id>', methods=['POST'])

def save_job(job_id):
    login_id = session.get('login_id')
    if not login_id:
        flash("User not logged in", "error")
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(login_id=login_id).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for('auth.login'))
    
    # Check if job is already saved
    existing_favorite = Favorite.query.filter_by(user_id=user.id, job_id=job_id).first()
    if existing_favorite:
        flash("Job already saved", "info")
        return redirect(url_for('user.user_dashboard'))
    
    # Create new favorite entry
    new_favorite = Favorite(user_id=user.id, job_id=job_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    flash("Job saved to favorites", "success")
    return redirect(url_for('user.user_dashboard'))
# Favorites Page Route with Pagination
from flask import request
@user_blueprint.route('/favorites')
@login_required
def favorites():
    login_id = session.get('login_id')
    if not login_id:
        flash("User not logged in", "error")
        return redirect(url_for('auth.login'))
    
    # Ensure that only regular users access this page
    if session.get('role') != 'user':
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(login_id=login_id).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for('auth.login'))
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of favorites per page, adjust as needed
    
    # Join Favorite with Job and include company information like in user_dashboard
    favorites_query = (
        db.session.query(Job)
        .join(Favorite, Job.job_id == Favorite.job_id)
        .join(Login, Job.created_by == Login.id)
        .join(Company, Login.id == Company.login_id)
        .filter(
            Favorite.user_id == user.id,
            Job.filled_vacancy < Job.total_vacancy,  # Not fully filled
            Company.is_banned == False,  # Company not banned
            Job.status == 'open'  # Job is active
        )
        .order_by(Favorite.saved_at.desc())
    )
    
    # Apply pagination
    favorites_pagination = favorites_query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    # Get the Job objects
    favorites = favorites_pagination.items
    
    # Get list of job IDs that the user has already applied to
    applied_job_ids = set()
    if favorites:
        job_ids = [job.job_id for job in favorites]
        applied_jobs = (
            db.session.query(JobApplication.job_id)
            .filter(
                JobApplication.user_id == user.id,
                JobApplication.job_id.in_(job_ids)
            )
            .all()
        )
        applied_job_ids = {job_id for (job_id,) in applied_jobs}
    
    return render_template(
        '/user/favorites.html',
        favorites=favorites,
        page=favorites_pagination.page,
        total_pages=favorites_pagination.pages,
        has_prev=favorites_pagination.has_prev,
        has_next=favorites_pagination.has_next,
        prev_num=favorites_pagination.prev_num,
        next_num=favorites_pagination.next_num,
        applied_job_ids=applied_job_ids
    )
@user_blueprint.route('/remove_favorite/<uuid:job_id>', methods=['POST'])
def remove_favorite(job_id):
    login_id = session.get('login_id')
    if not login_id:
        flash("User not logged in", "error")
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(login_id=login_id).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for('auth.login'))
    
    # Look for the favorite entry matching the user and job
    favorite = Favorite.query.filter_by(user_id=user.id, job_id=job_id).first()
    if not favorite:
        flash("Favorite not found", "error")
        return redirect(url_for('user.favorites'))
    
    db.session.delete(favorite)
    db.session.commit()
    
    flash("Job removed from favorites", "success")
    return redirect(url_for('user.favorites'))
@user_blueprint.route('/delete_resume/<uuid:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    # Check if user is logged in
    if 'username' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        username = session['username']
        
        # Get the login record first
        login = Login.query.filter_by(username=username).first()
        if not login:
            flash('Login not found!', 'error')
            return redirect(url_for('user.resume_certifications'))
        
        # Get the user record using the login_id
        user = User.query.filter_by(login_id=login.id).first()
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('user.resume_certifications'))
        
        # Find the resume for this specific user
        resume = ResumeCertification.query.filter_by(
            id=resume_id, 
            user_id=user.id
        ).first()
        
        if resume:
            # Delete the file from filesystem
            import os
            if resume.resume_path and os.path.exists(resume.resume_path):
                os.remove(resume.resume_path)
            
            # Delete the record from database
            db.session.delete(resume)
            db.session.commit()
            
            flash('Resume deleted successfully!', 'success')
        else:
            flash('Resume not found or you do not have permission to delete it!', 'error')
            
    except Exception as e:
        print(f"Error deleting resume: {str(e)}")
        flash('Error deleting resume!', 'error')
        
    return redirect(url_for('user.resume_certifications'))

@user_blueprint.route('/delete_certification/<uuid:certification_id>', methods=['POST'])
def delete_certification(certification_id):
    # Check if user is logged in
    if 'username' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))
   
    try:
        username = session['username']
       
        # Get the login record first
        login = Login.query.filter_by(username=username).first()
        if not login:
            flash('Login not found!', 'error')
            return redirect(url_for('user.resume_certifications'))
       
        # Get the user record using the login_id
        user = User.query.filter_by(login_id=login.id).first()
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('user.resume_certifications'))
       
        # Find the certification for this specific user
        # Assuming Certification model has user_id field
        certification = Certification.query.filter_by(
            id=certification_id,
            user_id=user.id
        ).first()
       
        if certification:
            # Delete the certification record from database
            db.session.delete(certification)
            db.session.commit()
           
            flash('Skill/Certification deleted successfully!', 'success')
        else:
            flash('Skill/Certification not found or you do not have permission to delete it!', 'error')
           
    except Exception as e:
        print(f"Error deleting certification: {str(e)}")
        flash('Error deleting skill/certification!', 'error')
       
    return redirect(url_for('user.resume_certifications'))