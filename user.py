from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for, flash, make_response
from flask_login import current_user
from config import Config
from functools import wraps
import os
from werkzeug.utils import secure_filename
from models import Certification, Company, Coupon, Couponuser, Job, JobApplication, Login,User,ResumeCertification, Notification,Favorite #, JobApplication
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os, uuid
from models import db  # Ensure 'db' is the instance of SQLAlchemy
  # Assuming your model is in 'models.py'
from config import Config
from utils import allowed_file  # Assuming your config file is named config.py
from datetime import datetime
from flask import request  # Ensure this is imported at the top
from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required

user_blueprint = Blueprint('user', __name__)

def no_cache(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
        return resp
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
@user_blueprint.route('/user_dashboard')
@no_cache
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
    per_page = 5  # Changed from 10 to 5
   
    # Get current date for deadline comparison
    current_date = datetime.utcnow().date()
    print(current_date)
    # Query jobs with filters:
    # 1. Exclude jobs where vacancy is full (filled_vacancy >= total_vacancy)
    # 2. Exclude jobs from banned companies
    # 3. Only show active jobs
    # 4. Exclude jobs where deadline has passed
    jobs_query = Job.query.join(Login, Job.created_by == Login.id)\
        .join(Company, Login.id == Company.login_id)\
        .filter(
            Job.filled_vacancy < Job.total_vacancy,  # Not fully filled
            Company.is_banned == False,  # Company not banned
            Job.status == 'open',  # Job is active
            Job.deadline > current_date  # Deadline has not passed
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
@no_cache
@login_required
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

from datetime import datetime, timedelta
import pytz

def get_chart_data_for_user(user_id):
    """
    Retrieves dynamic chart data, recent activities, and live feed for the given user.
    Returns four items:
      - user_success_rate: counts of applications by status (hired, rejected, pending, interviewed)
      - application_trends: daily count of applications (as a trend over time) - LIMITED TO LAST 5 DAYS
      - recent_activities: list of user's recent job applications with company names
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
    # Calculate the date 5 days ago from today in IST
    today = datetime.now(ist_timezone).date()
    five_days_ago = today - timedelta(days=4)  # 4 days ago + today = 5 days total
    
    # Convert IST dates to UTC for database comparison
    five_days_ago_utc = ist_timezone.localize(datetime.combine(five_days_ago, datetime.min.time())).astimezone(pytz.utc)
    today_end_utc = ist_timezone.localize(datetime.combine(today, datetime.max.time())).astimezone(pytz.utc)
    
    # Query for applications in the last 5 days (in UTC range)
    applications = db.session.query(JobApplication)\
        .filter(
            JobApplication.user_id == user_id,
            JobApplication.date_applied >= five_days_ago_utc,
            JobApplication.date_applied <= today_end_utc
        ).all()
    
    # Group applications by IST date
    date_counts = {}
    for app in applications:
        # Convert UTC datetime to IST
        if app.date_applied.tzinfo is None:
            # If datetime is naive, assume it's UTC
            utc_datetime = pytz.utc.localize(app.date_applied)
        else:
            utc_datetime = app.date_applied.astimezone(pytz.utc)
        
        # Convert to IST
        ist_datetime = utc_datetime.astimezone(ist_timezone)
        ist_date = ist_datetime.date()
        
        # Count applications per IST date
        if ist_date in date_counts:
            date_counts[ist_date] += 1
        else:
            date_counts[ist_date] = 1
    
    # Create a complete list of the last 5 days (including days with 0 applications)
    date_range = []
    count_range = []
    
    for i in range(5):
        current_date = five_days_ago + timedelta(days=i)
        date_range.append(current_date.strftime('%Y-%m-%d'))
        
        # Get count for this date
        count_for_date = date_counts.get(current_date, 0)
        count_range.append(count_for_date)
    
    application_trends = {"labels": date_range, "counts": count_range}
    
    # Recent activities: Last 5 job applications with job title and company name
    recent_activities = db.session.query(JobApplication, Job.title, Company.company_name)\
        .join(Job, Job.job_id == JobApplication.job_id)\
        .join(Login, Login.id == Job.created_by)\
        .join(Company, Company.login_id == Login.id)\
        .filter(JobApplication.user_id == user_id)\
        .order_by(JobApplication.date_applied.desc())\
        .limit(5).all()
    
    recent_activities_list = [
        {
            'job_title': f"{job_title} ({company_name})",
            'status': app.status
        }
        for app, job_title, company_name in recent_activities
    ]
    
    # Live feed: Last 5 job postings with company name
    live_feed = db.session.query(Job.title, Job.created_at, Company.company_name)\
        .join(Login, Login.id == Job.created_by)\
        .join(Company, Company.login_id == Login.id)\
        .filter(Job.deadline >= current_date)\
        .order_by(Job.created_at.desc())\
        .limit(5).all()
    
    live_feed_list = []
    for job_title, created_at, company_name in live_feed:
        if created_at:
            # Ensure we have a UTC datetime for consistent frontend conversion
            if created_at.tzinfo is None:
                # If datetime is naive, assume it's UTC
                utc_datetime = pytz.utc.localize(created_at)
            else:
                # If datetime is aware, convert to UTC
                utc_datetime = created_at.astimezone(pytz.utc)
        else:
            utc_datetime = None
            
        # Format job title with company in brackets
        formatted_title = f"{job_title} ({company_name})"
        
        live_feed_list.append({
            'job_title': formatted_title, 
            'posted_at': utc_datetime
        })
    
    return user_success_rate, application_trends, recent_activities_list, live_feed_list

@user_blueprint.route('/analytics')
@no_cache
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
@no_cache
@login_required
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

    # Paginate the notifications query
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Changed from unlimited to 5 per page

    # Use the user's login_id for querying communications and filter out hidden ones if needed.
    notifications_query = Communication.query.filter_by(user_id=user.login_id, hidden=False)\
        .order_by(Communication.timestamp.desc())
    
    notifications_pagination = notifications_query.paginate(page=page, per_page=per_page, error_out=False)
    notifications = notifications_pagination.items
    total_pages = notifications_pagination.pages
    
    unread_count = Communication.query.filter_by(user_id=user.login_id, read_status=False, hidden=False).count()

    return render_template(
        '/user/notification.html',
        notifications=notifications,
        unread_count=unread_count,
        page=page,
        total_pages=total_pages
    )

@user_blueprint.route('/mark_notification_read/<uuid:notification_id>', methods=['POST'], endpoint='mark_single_notification_read')
@no_cache
@login_required
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
@no_cache
@login_required
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
@no_cache
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
                # Check if certification already exists (case insensitive)
                existing_certification = Certification.query.filter(
                    Certification.user_id == user.id,
                    db.func.lower(Certification.certification_name) == certification_name.lower()
                ).first()
                
                if existing_certification:
                    flash(f'Skill "{certification_name}" already exists in your profile!', 'warning')
                else:
                    certification = Certification(
                        user_id=user.id,
                        certification_name=certification_name,
                        verification_status=False
                    )
                    db.session.add(certification)
                    db.session.commit()
                    flash(f'Skill "{certification_name}" added successfully!', 'success')
            else:
                flash('Please enter a skill name.', 'error')
        
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
@no_cache
@login_required
def application_history():
    user_id = session.get('user_id')
   
    if not user_id:
        flash("User is not logged in.", "error")
        return redirect(url_for('auth.login'))
    
    # Fetch all applications for the logged-in user, ordered by date_applied descending (most recent first)
    applications = JobApplication.query.filter_by(user_id=user_id).order_by(JobApplication.date_applied.desc()).all()
   
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
import re
import requests
from urllib.parse import urlparse
from datetime import datetime, timedelta  # Ensure these are imported if not already

# ============================================================================
# HELPER FUNCTIONS FOR USER MODULE
# ============================================================================
def sanitize_text(value: str) -> str:
    """ Sanitize text input to prevent XSS attacks. Removes script tags, javascript: URLs, data: URLs, and event handlers. """
    if not value:
        return ''
    # Remove <script>...</script>
    value = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', value, flags=re.IGNORECASE | re.DOTALL)
    # Remove javascript: or data: URLs inside attributes or text
    value = re.sub(r'javascript\s*:', '', value, flags=re.IGNORECASE)
    value = re.sub(r'data\s*:[^ \t\r\n]*', '', value, flags=re.IGNORECASE)
    # Remove on* event handlers
    value = re.sub(r'on\w+\s*=\s*"[^\"]*"', '', value, flags=re.IGNORECASE)
    value = re.sub(r'on\w+\s*=\s*\'[^\']*\'', '', value, flags=re.IGNORECASE)
    # Remove < and > characters
    value = value.replace('<', '').replace('>', '')
    return value.strip()

def url_seems_reachable(url: str, timeout: float = 3.0) -> bool:
    """ Check if a URL is reachable by making a HEAD or GET request. Returns True if the URL responds with a 2xx or 3xx status code. """
    try:
        # HEAD is lighter; fall back to GET for servers that don't support HEAD well
        resp = requests.head(url, allow_redirects=True, timeout=timeout)
        if resp.status_code >= 400:
            # try GET once more for sites that treat HEAD oddly
            resp = requests.get(url, allow_redirects=True, timeout=timeout)
        # treat 2xx / 3xx as "exists"
        return 200 <= resp.status_code < 400
    except requests.RequestException:
        return False

def is_valid_url(url: str) -> bool:
    """ Validate if a string is a properly formatted URL. """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def is_valid_email(email: str) -> bool:
    """ Validate email format using regex. """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def count_words(text: str) -> int:
    """ Count words in a text string. """
    if not text:
        return 0
    return len(text.strip().split())

# ============================================================================
# USER PROFILE ROUTE WITH ENHANCED VALIDATION
# ============================================================================
@user_blueprint.route('/profile', methods=['GET', 'POST'])
@no_cache
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

    # Dictionary to hold form values for template repopulation on error
    form_values = {}

    if request.method == 'POST':
        # Get raw inputs first for invalid char check and repopulation
        raw_name = request.form.get('name', '').strip()
        raw_email = request.form.get('email', '').strip()
        raw_phone = request.form.get('phone', '').strip()
        raw_age = request.form.get('age', '').strip()
        raw_manual_college = request.form.get('college_name', '').strip()
        raw_about_me = request.form.get('about_me', '').strip()
        raw_profile_pic_url = request.form.get('profile_pic_url', '').strip()
        raw_coupon_code = request.form.get('coupon_code', '').strip()

        # Store raw values for repopulation
        form_values = {
            'name': raw_name,
            'email': raw_email,
            'phone': raw_phone,
            'age': raw_age,
            'college_name': raw_manual_college,
            'about_me': raw_about_me,
            'profile_pic_url': raw_profile_pic_url,
            'coupon_code': raw_coupon_code
        }

        # Check for invalid characters (< or >) in all text fields
        text_fields_to_check = [
            ('Name', raw_name),
            ('Email', raw_email),
            ('Phone', raw_phone),
            ('College Name', raw_manual_college),
            ('About Me', raw_about_me),
            ('Profile Picture URL', raw_profile_pic_url),
            ('Coupon Code', raw_coupon_code)
        ]
        for field_name, raw_value in text_fields_to_check:
            if '<' in raw_value or '>' in raw_value:
                flash(f"Invalid characters (< or >) not allowed in {field_name} field.", "error")
                return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)

        # Sanitize inputs after invalid char check
        name_input = sanitize_text(raw_name)
        email_input = sanitize_text(raw_email)
        phone_input = sanitize_text(raw_phone)
        age_input = sanitize_text(raw_age)
        manual_college = sanitize_text(raw_manual_college)
        about_me_input = sanitize_text(raw_about_me)
        profile_pic_url = sanitize_text(raw_profile_pic_url)
        coupon_code = sanitize_text(raw_coupon_code)

        # Validate name
        if not name_input:
            flash("Name is required.", "error")
            return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)
        elif len(name_input) < 2:
            flash("Name must be at least 2 characters long.", "error")
            return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)
        elif len(name_input) > 100:
            flash("Name cannot exceed 100 characters.", "error")
            return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)

        # Validate email
        if not email_input:
            flash("Email is required.", "error")
            return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)
        elif not is_valid_email(email_input):
            flash("Please enter a valid email address (name@domain.com).", "error")
            return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)
        elif email_input != user.email:
            # Check for uniqueness only if email changed
            existing_email_user = User.query.filter_by(email=email_input).first()
            if existing_email_user:
                flash("This email is already registered to another user.", "error")
                return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)

        # Validate phone number if provided
        if phone_input:
            # Check if phone contains only digits
            if not phone_input.isdigit():
                return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)
            # Check phone length
            if len(phone_input) < 10 or len(phone_input) > 15:
                return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)
            # Check if phone number already exists for another user
            existing_phone_user = User.query.filter(
                User.phone == phone_input,
                User.id != user_id
            ).first()
            if existing_phone_user:
                return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)

        # Validate age if provided
        if age_input:
            try:
                age_value = int(age_input)
                if age_value < 18 or age_value > 80:
                    flash("Please enter a valid age between 18 and 80.", "error")
                    return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)
            except ValueError:
                flash("Please enter a valid age.", "error")
                return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)

        # Validate About Me word count if provided
        if about_me_input:
            word_count = count_words(about_me_input)
            if word_count > 200:
                flash(f"About Me section cannot exceed 200 words. Current count: {word_count} words.", "error")
                return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)
            if len(about_me_input) > 2000:
                flash("About Me section cannot exceed 2000 characters.", "error")
                return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)

        # Validate college name length if provided
        if manual_college:
            if len(manual_college) > 200:
                flash("College name cannot exceed 200 characters.", "error")
                return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)

        # Validate profile picture URL if provided
        if profile_pic_url:
            if not is_valid_url(profile_pic_url):
                flash("Please enter a valid URL for the profile picture.", "error")
                return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)
            # Check if URL is reachable (optional - can be slow)
            # Uncomment if you want to verify URL accessibility
            # if not url_seems_reachable(profile_pic_url):
            #     flash("The profile picture URL appears to be unreachable. Please check the URL.", "warning")

        # Handle college name and coupon code
        # Only process new coupon codes if user doesn't already have one
        if coupon_code and not user_coupon:
            coupon = Coupon.query.filter_by(code=coupon_code).first()
            if not coupon:
                flash("Invalid coupon code provided.", "error")
                return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)
            else:
                # Check if coupon is expired (created more than 2 years ago)
                current_date = datetime.now()
                coupon_creation_date = coupon.created_at
                expiration_threshold = current_date - timedelta(days=730)  # 2 years = 730 days
                if coupon_creation_date < expiration_threshold:
                    flash("Coupon has expired. This coupon is more than 2 years old.", "error")
                    return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)
                # Valid and non-expired coupon
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
                # Reload user_coupon after adding mapping
                user_coupon_mapping = Couponuser.query.filter_by(user_id=user_id).first()
                if user_coupon_mapping:
                    user_coupon = Coupon.query.filter_by(id=user_coupon_mapping.coupon_id).first()
        elif user_coupon:
            # User already has a coupon, don't allow changes to coupon-controlled fields
            if user_coupon.college:
                user.college_name = user_coupon.college.college_name
            else:
                user.college_name = manual_college or user.college_name
        else:
            # No coupon code provided and user doesn't have one, use manual college
            user.college_name = manual_college or user.college_name

        # Update user fields
        user.name = name_input
        user.email = email_input
        user.phone = phone_input if phone_input else None
        if age_input:
            try:
                user.age = int(age_input)
            except ValueError:
                pass  # Already validated above
        user.about_me = about_me_input if about_me_input else None
        # Profile picture URL update - clear if empty
        user.profile_picture = profile_pic_url if profile_pic_url else None

        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for('user.profile'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating profile: {str(e)}", "error")
            return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=True, form_values=form_values)

    return render_template('/user/profile.html', user=user, resumes=resumes, certifications=certifications, user_coupon=user_coupon, edit_mode=edit_mode, form_values=form_values)
from flask import jsonify

@user_blueprint.route('/get_application_details/<uuid:application_id>', methods=['GET'])
@no_cache
@login_required
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
# Job Details Route - Add this new route
# Job Details Route - Add this new route
@user_blueprint.route('/job_details/<uuid:job_id>')
@no_cache
@login_required
def job_details(job_id):
    login_id = session.get('login_id')
    if not login_id:
        flash("User not logged in", "error")
        return redirect(url_for('auth.login'))
   
    user = User.query.filter_by(login_id=login_id).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for('auth.login'))
    
    # Get current date for deadline comparison
    current_date = datetime.utcnow().date()
    
    # Fetch the job with deadline check
    job = Job.query.join(Company, Job.created_by == Company.login_id).filter(
        Job.job_id == job_id,
        Job.status != 'closed',
        Company.is_banned == False,
        Job.deadline > current_date  # Only show if deadline hasn't passed
    ).first()
    
    if not job:
        flash("Job not found or no longer available", "error")
        return redirect(url_for('user.job_search'))
    
    # Get user's applied and saved jobs
    applied_jobs = {app.job_id for app in JobApplication.query.filter_by(user_id=user.id).all()}
    saved_jobs = {fav.job_id for fav in Favorite.query.filter_by(user_id=user.id).all()}
    
    return render_template('/user/jobresults.html', 
                         job=job, 
                         applied_jobs=applied_jobs, 
                         saved_jobs=saved_jobs)

import re
import requests
from urllib.parse import urlparse
from datetime import datetime, timedelta, date  # Ensure date is imported
from sqlalchemy import or_

# Assuming sanitize_text is already defined from previous helpers

# ============================================================================
# JOB SEARCH ROUTE WITH ENHANCED VALIDATION AND SANITIZATION
# ============================================================================
@user_blueprint.route('/job_search', methods=['GET', 'POST'])
@no_cache
@login_required
def job_search():
    # Dictionary to hold form values for template repopulation on error
    form_values = {}

    if request.method == 'POST':
        # Get raw inputs first for invalid char check and repopulation
        raw_keyword = request.form.get('keyword', '').strip()
        raw_location = request.form.get('location', '').strip()
        raw_job_type = request.form.get('job_type', '').strip()
        raw_years_of_exp = request.form.get('years_of_exp', '').strip()
        raw_skills = request.form.get('skills', '').strip()
        raw_certifications = request.form.get('certifications', '').strip()
        raw_deadline = request.form.get('deadline', '').strip()

        # Store raw values for repopulation
        form_values = {
            'keyword': raw_keyword,
            'location': raw_location,
            'job_type': raw_job_type,
            'years_of_exp': raw_years_of_exp,
            'skills': raw_skills,
            'certifications': raw_certifications,
            'deadline': raw_deadline
        }

        # Check for invalid characters (< or >) in all text fields
        text_fields_to_check = [
            ('Keyword', raw_keyword),
            ('Location', raw_location),
            ('Skills', raw_skills),
            ('Certifications', raw_certifications)
        ]
        for field_name, raw_value in text_fields_to_check:
            if '<' in raw_value or '>' in raw_value:
                flash(f"Invalid characters (< or >) not allowed in {field_name} field.", "error")
                return render_template('/user/jobsearch.html', form_values=form_values)

        # Sanitize inputs after invalid char check
        keyword = sanitize_text(raw_keyword)
        location = sanitize_text(raw_location)
        job_type = sanitize_text(raw_job_type)
        years_of_exp = sanitize_text(raw_years_of_exp)
        skills = sanitize_text(raw_skills)
        certifications = sanitize_text(raw_certifications)
        deadline_str = sanitize_text(raw_deadline)

        # Validate deadline if provided
        deadline = None
        if deadline_str:
            try:
                deadline = date.fromisoformat(deadline_str)
                if deadline < date.today():
                    flash("Deadline cannot be in the past.", "error")
                    return render_template('/user/jobsearch.html', form_values=form_values)
            except ValueError:
                flash("Please enter a valid deadline date.", "error")
                return render_template('/user/jobsearch.html', form_values=form_values)

        # Get pagination parameters
        page = request.form.get('page', 1, type=int)
        per_page = 6  # Jobs per page

        # Get current date for base deadline comparison (show jobs on or after today)
        current_date = date.today()

        # Build the query with deadline check (>= for on or after today)
        query = Job.query.join(Company, Job.created_by == Company.login_id).filter(
            Job.status != 'closed',
            Company.is_banned == False,
            Job.deadline >= current_date  # Show jobs with deadline on or after today
        )

        # Apply search filters
        if keyword:
            keyword_like = f'%{keyword}%'
            query = query.filter(
                or_(
                    Job.title.ilike(keyword_like),
                    Job.description.ilike(keyword_like),
                    Job.skills.ilike(keyword_like),
                    Job.certifications.ilike(keyword_like),
                    Company.company_name.ilike(keyword_like)
                )
            )

        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))

        if job_type:
            query = query.filter(Job.job_type.ilike(job_type))

        if years_of_exp:
            try:
                if years_of_exp == '6':
                    query = query.filter(Job.years_of_exp >= 6)
                else:
                    exp_val = int(years_of_exp)
                    query = query.filter(Job.years_of_exp == exp_val)
            except (ValueError, TypeError):
                pass

        # Apply deadline filter if provided (jobs expiring on or before specified date)
        if deadline:
            query = query.filter(Job.deadline <= deadline)

        if skills:
            skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
            if skills_list:
                skills_filters = [Job.skills.ilike(f'%{skill}%') for skill in skills_list]
                query = query.filter(or_(*skills_filters))

        if certifications:
            cert_list = [cert.strip() for cert in certifications.split(',') if cert.strip()]
            if cert_list:
                cert_filters = [Job.certifications.ilike(f'%{cert}%') for cert in cert_list]
                query = query.filter(or_(*cert_filters))

        # Apply pagination
        jobs_pagination = query.order_by(Job.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        jobs = jobs_pagination.items

        # Get user's applied and saved jobs
        current_user_id = session.get('user_id')
        applied_applications = JobApplication.query.filter_by(user_id=current_user_id).all()
        applied_jobs = {app.job_id for app in applied_applications}
        saved_favorites = Favorite.query.filter_by(user_id=current_user_id).all()
        saved_jobs = {fav.job_id for fav in saved_favorites}

        # Pass search parameters to maintain state in results
        search_params = {
            'keyword': keyword,
            'location': location,
            'job_type': job_type,
            'years_of_exp': years_of_exp,
            'skills': skills,
            'certifications': certifications,
            'deadline': deadline_str if deadline_str else ''
        }

        return render_template('/user/jobresults.html',
                               jobs=jobs,
                               applied_jobs=applied_jobs,
                               saved_jobs=saved_jobs,
                               pagination=jobs_pagination,
                               search_params=search_params)
    else:
        return render_template('/user/jobsearch.html', form_values=form_values)
# Updated Save Job Route
@user_blueprint.route('/save_job1/<uuid:job_id>', methods=['POST'])
@no_cache
@login_required
def save_job1(job_id):
    login_id = session.get('login_id')
    if not login_id:
        flash("User not logged in", "error")
        return redirect(url_for('auth.login'))
   
    user = User.query.filter_by(login_id=login_id).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for('auth.login'))
   
    # Get the source page to determine redirect behavior
    source_page = request.form.get('source_page', 'job_search')
    
    # Check if job is already saved
    existing_favorite = Favorite.query.filter_by(user_id=user.id, job_id=job_id).first()
    if existing_favorite:
        flash("Job already saved", "info")
        # Redirect based on source page
        if source_page == 'job_details':
            return redirect(url_for('user.job_details', job_id=job_id))
        else:
            return redirect(request.referrer or url_for('user.job_search'))
   
    # Create new favorite entry
    new_favorite = Favorite(user_id=user.id, job_id=job_id)
    db.session.add(new_favorite)
    db.session.commit()
   
    flash("Job saved to favorites", "success")
    # Redirect based on source page
    if source_page == 'job_details':
        return redirect(url_for('user.job_details', job_id=job_id))
    else:
        return redirect(request.referrer or url_for('user.job_search'))


# Updated Apply for Job Route
@user_blueprint.route('/apply1_for_job/<uuid:job_id>', methods=['POST'])
@no_cache
@login_required
def apply1_for_job(job_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)  
    if not user:
        flash("User not found.", 'error')
        return redirect(url_for('user.user_dashboard'))
    
    # Get the source page to determine redirect behavior
    source_page = request.form.get('source_page', 'job_search')
    
    # Fetch the job that the user is applying for
    job = Job.query.get(job_id)
    if not job:
        flash("Job not found.", 'error')
        # Redirect based on source page
        if source_page == 'job_details':
            return redirect(url_for('user.job_search'))  # Can't show details if job doesn't exist
        else:
            return redirect(request.referrer or url_for('user.job_search'))
   
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
        # Redirect based on source page
        if source_page == 'job_details':
            return redirect(url_for('user.job_details', job_id=job_id))
        else:
            return redirect(request.referrer or url_for('user.job_search'))
    
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
    # Redirect based on source page
    if source_page == 'job_details':
        return redirect(url_for('user.job_details', job_id=job_id))
    else:
        return redirect(request.referrer or url_for('user.job_search'))
@user_blueprint.route('/save_job/<uuid:job_id>', methods=['POST'])
@no_cache
@login_required
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

from flask import request
from sqlalchemy import or_

@user_blueprint.route('/favorites')
@no_cache
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
   
    # Get pagination and search parameters
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str).strip()
    per_page = 5  # Number of favorites per page, adjust as needed
   
    # Base query - Join Favorite with Job and include company information
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
    )
    
    # Apply search filter if search query exists
    if search_query:
        favorites_query = favorites_query.filter(
            or_(
                Job.title.ilike(f'%{search_query}%'),
                Job.description.ilike(f'%{search_query}%'),
                Job.skills.ilike(f'%{search_query}%'),
                Job.location.ilike(f'%{search_query}%'),
                Job.job_type.ilike(f'%{search_query}%'),
                Job.certifications.ilike(f'%{search_query}%'),
                Company.company_name.ilike(f'%{search_query}%')
            )
        )
    
    # Order by saved date
    favorites_query = favorites_query.order_by(Favorite.saved_at.desc())
   
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
        applied_job_ids=applied_job_ids,
        search_query=search_query  # Pass search query to template
    )
@user_blueprint.route('/remove_favorite/<uuid:job_id>', methods=['POST'])
@no_cache
@login_required
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
@no_cache
@login_required
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
@no_cache
@login_required
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