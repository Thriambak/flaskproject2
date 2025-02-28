from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for, flash
from flask_login import current_user
from config import Config
from functools import wraps
import os
from werkzeug.utils import secure_filename
from models import Certification, Coupon, Couponuser, Job, JobApplication,User,ResumeCertification, Notification #, JobApplication
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models import db  # Ensure 'db' is the instance of SQLAlchemy
  # Assuming your model is in 'models.py'
from config import Config
from utils import allowed_file  # Assuming your config file is named config.py


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
@user_blueprint.route('/user_dashboard')
@login_required
def user_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash("User not logged in", "error")
        return redirect(url_for('auth.login'))
    
    # Ensure that only regular users access this page.
    if session.get('role') != 'user':
        return redirect(url_for('admin.admin_dashboard'))
    
    # Fetch jobs for display (all jobs ordered by creation date).
    jobs = Job.query.order_by(Job.created_at.desc()).all()

    # Calculate application status counts for this user.
    hired = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'hired').scalar() or 0
    rejected = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'rejected').scalar() or 0
    pending = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'pending').scalar() or 0

    user_success_rate = {
        "hired": hired,
        "rejected": rejected,
        "pending": pending
    }

    # Prepare applications overview: group the number of applications by job title.
    overview = db.session.query(
        Job.title,
        db.func.count(JobApplication.id).label('applications')
    ).join(Job, Job.job_id == JobApplication.job_id)\
     .filter(JobApplication.user_id == user_id)\
     .group_by(Job.title).all()

    labels = [row.title for row in overview]
    applications = [row.applications for row in overview]
    applications_overview = {"labels": labels, "applications": applications}

    return render_template('user_dashboard.html',
                           jobs=jobs,
                           user_success_rate=user_success_rate,
                           applications_overview=applications_overview)






# Display the user dashboard



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
        flash("Application Successfull")
    if not resume_certification or not resume_certification.resume_path:
        flash("You must upload a resume to apply for a job.", 'error')
        return redirect(url_for('user.resume_certifications'))

    # Check if the user has already applied for this job
    existing_application = JobApplication.query.filter_by(user_id=user.id, job_id=job_id).first()
    if existing_application:
        flash(f"You have already applied for the job {job.title}.", 'error')
        return redirect(url_for('user.user_dashboard'))

    # Prepare the application
    new_application = JobApplication(
        user_id=user.id,
        job_id=job.job_id,
        status='pending',  # You can modify the status later (e.g., 'accepted', 'rejected')
        resume_path=resume_certification.resume_path,
    )

    message = f"{user.name} has applied for the job: {job.title}"
    new_notification = Notification(
        user_id=user.login_id,
        company_id=job.created_by,
        message=message,
    )

    # Add the application to the database
    db.session.add(new_application)
    db.session.add(new_notification)
    db.session.commit()

    flash(f"Application for {job.title} submitted successfully!", 'success')

    # Redirect to the user dashboard
    return redirect(url_for('user.user_dashboard'))
def get_chart_data_for_user(user_id):
    """
    Retrieves dynamic chart data from the JobApplication table for the given user.
    Returns two dictionaries:
      - user_success_rate: counts of applications by status (hired, rejected, pending)
      - applications_overview: a breakdown of application counts by job title
    """
    # Calculate application status counts
    hired = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'hired').scalar() or 0
    rejected = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'rejected').scalar() or 0
    pending = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'pending').scalar() or 0

    user_success_rate = {"hired": hired, "rejected": rejected, "pending": pending}

    # Prepare applications overview data grouped by job title
    overview = db.session.query(
        Job.title,
        db.func.count(JobApplication.id).label('applications')
    ).join(Job, Job.job_id == JobApplication.job_id)\
     .filter(JobApplication.user_id == user_id)\
     .group_by(Job.title).all()

    labels = [row.title for row in overview]
    applicationss = [row.applications for row in overview]
    applications_overview = {"labels": labels, "applications": applicationss}

    return user_success_rate, applications_overview


from models import Communication

from flask import session, render_template

@user_blueprint.route('/notifications', methods=['GET'])
def notifications():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view notifications.", "danger")
        return redirect(url_for('auth.login'))

    notifications = Communication.query.filter_by(user_id=user_id)\
        .order_by(Communication.timestamp.desc()).all()
    unread_count = Communication.query.filter_by(user_id=user_id, read_status=False).count()

    # Retrieve dynamic chart data
    user_success_rate, applications_overview = get_chart_data_for_user(user_id)

    return render_template(
        'notification.html',
        notifications=notifications,
        unread_count=unread_count,
        user_success_rate=user_success_rate,
        applications_overview=applications_overview
    )

from flask import session, render_template
from models import Communication

@user_blueprint.route('/mark_all_read', methods=['POST'])
def mark_all_read():
    user_id = session.get('user_id')

    if not user_id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.login'))

    Communication.query.filter_by(user_id=user_id, read_status=False).update({"read_status": True})
    db.session.commit()

    flash("All notifications marked as read.", "success")
    return redirect(url_for('user.notifications'))

# Helper function to check file type
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

    # Compute dynamic data for charts (available for GET and POST)
    hired = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'hired').scalar() or 0
    rejected = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'rejected').scalar() or 0
    pending = db.session.query(db.func.count(JobApplication.id))\
        .filter(JobApplication.user_id == user_id, JobApplication.status == 'pending').scalar() or 0

    user_success_rate = {"hired": hired, "rejected": rejected, "pending": pending}

    overview = db.session.query(
        Job.title,
        db.func.count(JobApplication.id).label('applications')
    ).join(Job, Job.job_id == JobApplication.job_id)\
     .filter(JobApplication.user_id == user_id)\
     .group_by(Job.title).all()

    labels = [row.title for row in overview]
    applications = [row.applications for row in overview]
    applications_overview = {"labels": labels, "applications": applications}

    # Retrieve data for display
    resumes = ResumeCertification.query.filter_by(user_id=user_id).all()
    certifications = Certification.query.filter_by(user_id=user_id).all()

    return render_template(
        'resume_certifications.html',
        resume_certifications=resumes,
        certifications=certifications,
        user_success_rate=user_success_rate,
        applications_overview=applications_overview,
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
    
    # Retrieve chart data using the common helper function
    user_success_rate, applications_overview = get_chart_data_for_user(user_id)

    # Render the template with the application data and chart data
    return render_template(
        'applicationhistory.html',
        applications=applications,
        user_success_rate=user_success_rate,
        applications_overview=applications_overview
    )

@user_blueprint.route('/job_search', methods=['GET', 'POST'])
def job_search():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form.get('title')
        location = request.form.get('location')
        job_type = request.form.get('job_type')
        skills = request.form.get('skills')
        certifications = request.form.get('certifications')
        salary = request.form.get('salary')
        deadline = request.form.get('deadline')
        years_of_exp = request.form.get('years_of_exp')
        description = request.form.get('description')
        total_vacancy = request.form.get('total_vacancy')
        filled_vacancy = request.form.get('filled_vacancy')
        status = request.form.get('status')
        
        # Start building the query
        query = Job.query
        if title:
            query = query.filter(Job.title.ilike(f'%{title}%'))
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))
        if job_type:
            query = query.filter(Job.job_type == job_type)
        if skills:
            query = query.filter(Job.skills.ilike(f'%{skills}%'))
        if certifications:
            query = query.filter(Job.certifications.ilike(f'%{certifications}%'))
        if salary:
            # Convert salary string to a number if needed; here we assume it's a comparable value.
            query = query.filter(Job.salary <= salary)
        if deadline:
            query = query.filter(Job.deadline <= deadline)
        if years_of_exp:
            query = query.filter(Job.years_of_exp == int(years_of_exp))
        if description:
            query = query.filter(Job.description.ilike(f'%{description}%'))
        if total_vacancy:
            query = query.filter(Job.total_vacancy == int(total_vacancy))
        if filled_vacancy:
            query = query.filter(Job.filled_vacancy == int(filled_vacancy))
        if status:
            query = query.filter(Job.status == status)
        
        # Order by most recent and get all matching jobs
        jobs = query.order_by(Job.created_at.desc()).all()
        
        # Render a separate results page
        return render_template('jobresults.html', jobs=jobs)
    else:
        # If GET, simply render the search form page
        return render_template('jobsearch.html')

@user_blueprint.route('/mark_notification_read/<int:notification_id>', methods=['POST'])
def mark_notification_read(notification_id):
    notification = Communication.query.get(notification_id)

    if not notification or notification.user_id != session.get('user_id'):
        flash("Notification not found or access denied.", "danger")
        return redirect(url_for('user.notifications'))

    notification.read = True
    db.session.commit()

    flash("Notification marked as read.", "success")
    return redirect(url_for('user.notifications'))



@user_blueprint.route('/delete_notification/<int:notification_id>', methods=['POST'])
def delete_notification(notification_id):
    notification = Communication.query.get(notification_id)

    if not notification or notification.user_id != session.get('user_id'):
        flash("Notification not found or access denied.", "danger")
        return redirect(url_for('user.notifications'))

    db.session.delete(notification)
    db.session.commit()

    flash("Notification deleted.", "success")
    return redirect(url_for('user.notifications'))


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
    
    # Retrieve dynamic chart data using the common helper function
    user_success_rate, applications_overview = get_chart_data_for_user(user_id)
    
    # Determine edit mode based on query parameter (?edit=true)
    edit_mode = request.args.get('edit', 'false').lower() == 'true'
    
    if request.method == 'POST':
        # (Your existing POST processing code)
        user.phone = request.form.get('phone', user.phone)
        age_input = request.form.get('age', '')
        if age_input:
            try:
                user.age = int(age_input)
            except ValueError:
                flash("Invalid age provided.", "error")
                return redirect(url_for('user.profile', edit='true'))
        user.about_me = request.form.get('about_me', user.about_me)
        
        coupon_code = request.form.get('coupon_code', "").strip()
        manual_college = request.form.get('college_name', "").strip()
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
                           edit_mode=edit_mode,
                           user_success_rate=user_success_rate,
                           applications_overview=applications_overview)
