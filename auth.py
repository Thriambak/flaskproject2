from flask import Blueprint, render_template, request, redirect
from flask import url_for, session, flash, make_response, jsonify
from config import Config
from models import Admin, College, db, User, Job, Login, Company, Login
import re
import random
import string
from extensions import mail
from flask_mail import Message
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from sqlalchemy import func
from functools import wraps
import re
import os

auth_blueprint = Blueprint('auth', __name__)

def no_cache(f):
    """Decorator to prevent caching of responses"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
        return resp
    return decorated_function

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def secure_route(f):
    """Enhanced decorator that combines login requirement with no-cache headers"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check session validity first
        if not check_session_validity():
            return redirect(url_for('auth.login'))
        
        # Execute the route function
        response = make_response(f(*args, **kwargs))
        
        # Add comprehensive cache control headers
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, post-check=0, pre-check=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Last-Modified'] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        response.headers['ETag'] = '0'
        
        return response
    return decorated_function

def check_session_validity():
    """Check if the current session is valid"""
    if 'login_id' not in session:
        return False
    
    # Verify the login still exists in database
    login = Login.query.filter_by(id=session['login_id']).first()
    if not login:
        session.clear()
        return False
    
    # Check if user is banned (if applicable)
    if login.role == 'user':
        user = User.query.filter_by(login_id=login.id).first()
        if user and user.is_banned:
            session.clear()
            return False
    elif login.role == 'company':
        company = Company.query.filter_by(login_id=login.id).first()
        if company and company.is_banned:
            session.clear()
            return False
    
    return True

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
@no_cache
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'user')  # Default to 'user'
        email = request.form['email']

        # Confirm password check
        '''if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('auth.signup'))'''
        
        # Forbidden Username Validation
        username_lower = username.lower()
        if username_lower == 'admin' or username_lower == 'administrator':
            flash('The entered username is not allowed. Please choose a different username.', 'danger')
            return redirect(url_for('auth.signup'))
        
        # Username length validation
        if not (3 <= len(username) <= 30):
            flash('Username must be between 3 and 30 characters long.', 'danger')
            return redirect(url_for('auth.signup'))
        
        # Username validation
        # Allowed: single word (alphanumeric), email, or 10-digit phone number
        username_pattern = r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$|^[a-zA-Z0-9]+$|^[0-9]{10}$'
        if not re.match(username_pattern, username):
            flash('Username must be a single word (letters/numbers only) and a valid email.', 'danger')
            return redirect(url_for('auth.signup'))
        if username.startswith('_') or username.startswith('.') or username.endswith('_') or username.endswith('.'):
            flash('Username cannot start or end with an underscore (_) or period (.)', 'danger')
            return redirect(url_for('auth.signup'))
        if ' ' in username:
            flash('Username cannot contain spaces.', 'danger')
            return redirect(url_for('auth.signup'))

        # Password validation
        password = password.strip()
        '''if ' ' in password:
            flash('Password cannot contain spaces.', 'danger')
            return redirect(url_for('auth.signup'))'''
        if not re.match(r'^[a-zA-Z0-9@#$%^&+= ]+$', password):
            flash('Password can only contain letters, numbers, and special characters @ #$%^&+=', 'danger')
            return redirect(url_for('auth.signup'))
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('auth.signup'))
       
        # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash('Invalid email format. Please use a valid email (e.g., user@domain.com).', 'danger')
            return redirect(url_for('auth.signup'))

        # Check for existing username or email
        if Login.query.filter(func.lower(Login.username) == username.lower()).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.signup'))
        if (User.query.filter_by(email=email).first() or 
            Company.query.filter_by(email=email).first() or 
            College.query.filter_by(email=email).first() or 
            Admin.query.filter_by(email=email).first()):
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.signup'))

        # Create entry in the Login table
        new_login = Login(username=username, role=role)
        new_login.set_password(password)
        db.session.add(new_login)
        db.session.flush()  # Get the login ID

        # Insert role-specific data
        if role == 'user':
            new_user = User(login_id=new_login.id, name=username, email=email)
            db.session.add(new_user)
        elif role == 'company':
            new_company = Company(login_id=new_login.id, company_name=username, email=email)
            db.session.add(new_company)
        elif role == 'college':
            new_college = College(login_id=new_login.id, college_name=username, email=email)
            db.session.add(new_college)
        else:
            flash('Invalid profile type specified.', 'danger')
            return redirect(url_for('auth.signup'))

        db.session.commit()
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth_blueprint.route('/check-session', methods=['POST'])
def check_session():
    """Check if user session is valid - for AJAX calls"""
    if 'login_id' in session:
        return jsonify({'authenticated': True})
    return jsonify({'authenticated': False})

@auth_blueprint.route('/clear-history')
def clear_history():
    """Clear browser history and redirect to login"""
    response = make_response(redirect(url_for('auth.login')))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Update your existing login route to include cache control headers
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the Login table
        login = Login.query.filter_by(username=username).first()
        if not login or not login.check_password(password):
            resp = make_response(render_template('login.html', error='Invalid username or password.'))
            resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            resp.headers['Pragma'] = 'no-cache'
            resp.headers['Expires'] = '0'
            return resp

        # Now check the `is_banned` status for the user or company
        if login.role in ['user', 'company']:
            # Check if the user or company is banned
            if login.role == 'user':
                user = User.query.filter_by(login_id=login.id).first()
                if user and user.is_banned:
                    resp = make_response(render_template('login.html', error="Cannot login. Contact support."))
                    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                    resp.headers['Pragma'] = 'no-cache'
                    resp.headers['Expires'] = '0'
                    return resp
            elif login.role == 'company':
                company = Company.query.filter_by(login_id=login.id).first()
                if company and company.is_banned:
                    resp = make_response(render_template('login.html', error="Cannot login. Contact support."))
                    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                    resp.headers['Pragma'] = 'no-cache'
                    resp.headers['Expires'] = '0'
                    return resp

        # Store session details
        session['login_id'] = login.id
        session['username'] = login.username
        session['role'] = login.role
        session['last_activity'] = datetime.utcnow()
        session.permanent = True  # Make session permanent

        # Redirect based on role
        if login.role == 'user':
            user = User.query.filter_by(login_id=login.id).first()
            if not user:
                resp = make_response(render_template('login.html', error='User details not found.'))
                resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                resp.headers['Pragma'] = 'no-cache'
                resp.headers['Expires'] = '0'
                return resp
            session['user_id'] = user.id  
            return redirect(url_for('user.user_dashboard'))
        elif login.role == 'company':
            company = Company.query.filter_by(login_id=login.id).first()
            if not company:
                resp = make_response(render_template('login.html', error='Company details not found.'))
                resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                resp.headers['Pragma'] = 'no-cache'
                resp.headers['Expires'] = '0'
                return resp
            return redirect(url_for('company.company_dashboard'))
        elif login.role == 'admin':
            admin = Admin.query.filter_by(login_id=login.id).first()
            if not admin:
                resp = make_response(render_template('login.html', error='Admin details not found.'))
                resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                resp.headers['Pragma'] = 'no-cache'
                resp.headers['Expires'] = '0'
                return resp
            return redirect(url_for('admin_routes.admin_dashboard'))
        elif login.role == 'college':
            college = College.query.filter_by(login_id=login.id).first()
            session['college_id'] = college.id
            if not college:
                resp = make_response(render_template('login.html', error='College details not found.'))
                resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                resp.headers['Pragma'] = 'no-cache'
                resp.headers['Expires'] = '0'
                return resp
            return redirect(url_for('college.college_dashboard'))
    
    # For GET requests, return login page with cache control headers
    resp = make_response(render_template('login.html'))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

@auth_blueprint.route('/logout')
@no_cache
def logout():
    session.pop('login_id', None)
    session.pop('username', None)
    session.pop('role', None)
    session.pop('user_id', None)
    session.pop('college_id', None)
    session.pop('company_id', None)  # Fixed typo: was 'comapany_id'
    session.clear()  # Clears all session variables
    
    # Create a response object for the redirect
    response = make_response(redirect(url_for('auth.login')))
    
    # Add comprehensive headers to clear the browser cache
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Last-Modified"] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    response.headers["ETag"] = "0"
    
    return response

@auth_blueprint.route('/forgot-password', methods=['GET', 'POST'])
@no_cache
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if(user is None):
            user = College.query.filter_by(email=email).first()
            if(user is None):
                user=Company.query.filter_by(email=email).first()
                if(user is None):
                    user=Admin.query.filter_by(email=email).first()

        if user:
            otp = ''.join(random.choices(string.digits, k=6))  # Generate OTP
            session['otp'] = otp
            session['email'] = email  # Store email temporarily
            session['otp_time'] = datetime.utcnow().isoformat()  # Store OTP generation time

            # Send OTP via email
            msg = Message("Password Reset OTP", recipients=[email])
            msg.body = f"Your OTP for password reset is: {otp}. It will expire in 10 minutes."
            mail.send(msg)

            flash("OTP has been sent to your email.", "success")
            return redirect(url_for('auth.verify_otp'))
        else:
            flash("Email not found. Please check and try again.", "danger")

    return render_template('forgot_password.html')

@auth_blueprint.route('/verify-otp', methods=['GET', 'POST'])
@no_cache
def verify_otp(): 
    # Check if OTP and OTP time exist in the session
    if 'otp' not in session or 'otp_time' not in session:
        flash("Session expired. Please request a new OTP.", "danger")
        return redirect(url_for('auth.forgot_password'))

    # Get OTP time and calculate remaining time
    otp_time = datetime.fromisoformat(session['otp_time'])
    remaining_time = (otp_time + timedelta(minutes=10)) - datetime.utcnow()

    # If OTP expired
    if remaining_time.total_seconds() <= 0:
        session.pop('otp', None)
        session.pop('otp_time', None)
        flash("OTP expired. Please request a new one.", "danger")
        return redirect(url_for('auth.forgot_password'))

    # Handle POST request when OTP is entered
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session.get('otp'):
            return redirect(url_for('auth.reset_password'))
        else:
            flash("Invalid OTP. Please try again.", "danger")

    # Render the verify_otp page and pass remaining time to template
    return render_template('verify_otp.html', remaining_time=int(remaining_time.total_seconds()))

@auth_blueprint.route('/otp-timer')
@no_cache
def otp_timer():
    """API endpoint to check remaining OTP time."""
    # If OTP time does not exist in the session
    if 'otp_time' not in session:
        return jsonify({'expired': True, 'remaining_time': 0})

    # Get OTP time and calculate remaining time
    otp_time = datetime.fromisoformat(session['otp_time'])
    remaining_time = (otp_time + timedelta(minutes=10)) - datetime.utcnow()

    # If OTP expired
    if remaining_time.total_seconds() <= 0:
        session.pop('otp', None)
        session.pop('otp_time', None)
        return jsonify({'expired': True, 'remaining_time': 0})

    # Return remaining time if OTP is still valid
    return jsonify({'expired': False, 'remaining_time': int(remaining_time.total_seconds())})

# Password Reset Route
@auth_blueprint.route('/reset-password', methods=['GET', 'POST'])
@no_cache
def reset_password():
    if 'email' not in session:
        flash("Session expired. Please request a new OTP.", "danger")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate password
        if new_password != confirm_password:
            flash("Passwords do not match. Please try again.", "danger")
            return redirect(url_for('auth.reset_password'))

        if ' ' in new_password:
            flash('Password cannot contain spaces.', 'danger')
            return redirect(url_for('auth.reset_password'))

        if not re.match(r'^[a-zA-Z0-9@#$%^&+=]+$', new_password):
            flash('Password can only contain letters, numbers, and special characters @#$%^&+=', 'danger')
            return redirect(url_for('auth.reset_password'))

        if len(new_password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('auth.reset_password'))

        # Hash password
        hashed_password = generate_password_hash(new_password)

        # Find user by email
        email = session.get('email')
        user = User.query.filter_by(email=email).first() or \
               College.query.filter_by(email=email).first() or \
               Company.query.filter_by(email=email).first() or \
               Admin.query.filter_by(email=email).first()

        if user:
            # Get the corresponding Login entry
            login_entry = Login.query.filter_by(id=user.login_id).first()
            if login_entry:
                login_entry.password_hash = hashed_password
                db.session.commit()

                # Clear session data
                session.pop('email', None)
                session.pop('otp', None)

                flash("Password reset successful! You can now log in.", "success")
                return redirect(url_for('auth.login'))

        flash("Error resetting password. Please try again.", "danger")

    return render_template('reset_password.html')
