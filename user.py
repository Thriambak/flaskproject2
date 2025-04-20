from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for, flash
from flask_login import current_user
from config import Config
from functools import wraps
import os
from werkzeug.utils import secure_filename
from models import Certification, Coupon, Couponuser, Job, JobApplication, Login,User,ResumeCertification, Notification #, JobApplication
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
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
        return redirect(url_for('admin.admin_dashboard'))
    
    # Get the User object using login_id from the Login table
    user = User.query.filter_by(login_id=login_id).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for('auth.login'))
    user_id = user.id  # This is the User table's id, used for job application queries
    
    db.session.commit()
    db.session.expire_all()  # Forces fresh query results

    # Paginate the jobs query
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Adjust as needed
    jobs_pagination = Job.query.order_by(Job.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    jobs = jobs_pagination.items
    total_pages = jobs_pagination.pages

    # Remove chart data; only upcoming events and notifications remain
    current_date = datetime.utcnow()
    upcoming_events = db.session.query(Job.title, Job.deadline)\
        .join(JobApplication, Job.job_id == JobApplication.job_id)\
        .filter(JobApplication.user_id == user_id, Job.deadline > current_date)\
        .order_by(Job.deadline.asc()).all()
    recent_notifications = Notification.query.filter_by(user_id=user_id, hidden=False)\
        .order_by(Notification.timestamp.desc()).limit(5).all()
    
    return render_template('user_dashboard.html',
                           jobs=jobs,
                           upcoming_events=upcoming_events,
                           recent_notifications=recent_notifications,
                           page=page,
                           total_pages=total_pages)
from datetime import datetime

from models import db, User, Job, JobApplication, ResumeCertification, Notification

@user_blueprint.route('/apply_for_job/<int:job_id>', methods=['POST'])

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

@user_blueprint.route('/apply1_for_job/<int:job_id>', methods=['POST'])

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

def get_chart_data_for_user(user_id):
    """
    Retrieves dynamic chart data, recent activities, and live feed for the given user.
    Returns four items:
      - user_success_rate: counts of applications by status (hired, rejected, pending)
      - application_trends: daily count of applications (as a trend over time)
      - recent_activities: list of user's recent job applications
      - live_feed: list of recent job postings
    """
    # Chart data: User success rate
    hired = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'Hired').scalar() or 0
    rejected = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'Rejected').scalar() or 0
    
    pending = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'Pending').scalar() or 0
    interviewed = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'Interviewed').scalar() or 0
    user_success_rate = {"hired": hired, "rejected": rejected, "pending": pending,"Interviewed":interviewed}

    # Chart data: Application trends (daily count)
    trend_data = db.session.query(
        db.func.date(JobApplication.date_applied).label('date'),
        db.func.count(JobApplication.id).label('count')
    ).filter(JobApplication.user_id == user_id)\
     .group_by(db.func.date(JobApplication.date_applied))\
     .order_by(db.func.date(JobApplication.date_applied)).all()
    trend_labels = [row.date.strftime('%Y-%m-%d') for row in trend_data]
    trend_counts = [row.count for row in trend_data]
    application_trends = {"labels": trend_labels, "counts": trend_counts}

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

    # Live feed: Last 5 job postings
    live_feed = db.session.query(Job)\
        .order_by(Job.created_at.desc())\
        .limit(5).all()
    live_feed_list = [
        {'job_title': job.title, 'posted_at': job.created_at}
        for job in live_feed
    ]

    return user_success_rate, application_trends, recent_activities_list, live_feed_list

@user_blueprint.route('/analytics')
@login_required
def analytics():
    user_id = session.get('user_id')
    user_success_rate, application_trends, recent_activities, live_feed = get_chart_data_for_user(user_id)
    return render_template(
        'analytics.html',
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
        'notification.html',
        notifications=notifications,
        unread_count=unread_count
    )
@user_blueprint.route('/mark_notification_read/<int:notification_id>', methods=['POST'], endpoint='mark_single_notification_read')
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

@user_blueprint.route('/delete_notification/<int:notification_id>', methods=['POST'])
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
        return redirect(url_for('login'))

    # Fetch user data
    user = User.query.get(user_id)
    print(user_id, user)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))

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
        'resume_certifications.html',
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
    return render_template(
        'applicationhistory.html',
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
        return render_template('jobresults.html', jobs=jobs)
    else:
        return render_template('jobsearch.html')






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
    
    # Other data for charts, etc.
    edit_mode = request.args.get('edit', 'false').lower() == 'true'
    
    if request.method == 'POST':
        # Update phone, age, etc.
        user.phone = request.form.get('phone', user.phone)
        age_input = request.form.get('age', '')
        if age_input:
            try:
                user.age = int(age_input)
            except ValueError:
                flash("Invalid age provided.", "error")
                return redirect(url_for('user.profile', edit='true'))
        user.about_me = request.form.get('about_me', user.about_me)
        manual_college = request.form.get('college_name', '').strip()
        coupon_code = request.form.get('coupon_code', "").strip()
        if coupon_code:
            coupon = Coupon.query.filter_by(code=coupon_code).first()
            if coupon:
                existing_mapping = Couponuser.query.filter_by(user_id=user_id, coupon_id=coupon.id).first()
                if not existing_mapping:
                    new_mapping = Couponuser(user_id=user_id, coupon_id=coupon.id)
                    db.session.add(new_mapping)
                if coupon.college:
                    user.college_name = f"Connected to {coupon.college.college_name}"
                else:
                    user.college_name = manual_college or user.college_name
            else:
                flash("Invalid coupon code provided.", "error")
                user.college_name = manual_college or user.college_name
        else:
            user.college_name = manual_college or user.college_name
        
        # NEW: Get the profile picture URL from the form and update the field
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
    
    return render_template('profile.html',
                           user=user,
                           resumes=resumes,
                           certifications=certifications,
                           edit_mode=edit_mode)
from flask import jsonify

@user_blueprint.route('/get_application_details/<int:application_id>', methods=['GET'])
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
@user_blueprint.route('/save_job/<int:job_id>', methods=['POST'])

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


# Favorites Page Route
@user_blueprint.route('/favorites')

def favorites():
    login_id = session.get('login_id')
    if not login_id:
        flash("User not logged in", "error")
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(login_id=login_id).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for('auth.login'))
    
    # Join Favorite with Job so that all job details are available.
    favorites_data = (
        db.session.query(Favorite, Job)
        .join(Job, Favorite.job_id == Job.job_id)
        .filter(Favorite.user_id == user.id)
        .order_by(Favorite.saved_at.desc())
        .all()
    )
    
    # Extract the Job objects from the tuple results.
    favorites = [job for favorite, job in favorites_data]
    
    return render_template('favorites.html', favorites=favorites)
@user_blueprint.route('/remove_favorite/<int:job_id>', methods=['POST'])
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
