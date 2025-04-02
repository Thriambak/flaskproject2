from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response,jsonify
from config import Config
from models import Admin, College, db, User, Job, Login, Company
import re
import random
import string
from extensions import mail
from flask_mail import Message
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
auth_blueprint = Blueprint('auth', __name__)

import re
import os
@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'user')  # Default to 'user'
        email = request.form['email']

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
        if ' ' in password:
            flash('Password cannot contain spaces.', 'danger')
            return redirect(url_for('auth.signup'))
        if not re.match(r'^[a-zA-Z0-9@#$%^&+=]+$', password):
            flash('Password can only contain letters, numbers, and special characters @#$%^&+=', 'danger')
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
        if Login.query.filter_by(username=username).first():
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


'''@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'user').strip().lower()  # Default is 'user'
        email = request.form.get('email', '').strip()

        # Validate mandatory fields
        if not username or not password or not email:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('auth.signup'))

        # Validate email format
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            flash('Please enter a valid email address, e.g., example@domain.com.', 'danger')
            return redirect(url_for('auth.signup'))

        # Validate username:
        # Allow only alphanumeric characters and @ (if using email as username) and ensure it doesn't start/end with . or _
        if not re.match(r'^(?![._])(?!.*[._]$)[A-Za-z0-9@]+$', username):
            flash('Username must be a single word without spaces and cannot start or end with a period or underscore.', 'danger')
            return redirect(url_for('auth.signup'))

        # Check if username or email already exists across Login and role-specific tables
        if Login.query.filter_by(username=username).first() or (
            User.query.filter_by(email=email).first() or
            Company.query.filter_by(email=email).first() or
            Admin.query.filter_by(email=email).first() or
            College.query.filter_by(email=email).first()
        ):
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('auth.signup'))

        try:
            # Create a new login entry
            new_login = Login(username=username, role=role)
            new_login.set_password(password)
            db.session.add(new_login)
            db.session.flush()  # Flush to get new_login.id

            # Create role-specific data entry
            if role == 'user':
                new_role_instance = User(login_id=new_login.id, name=username, email=email)
            elif role == 'company':
                new_role_instance = Company(login_id=new_login.id, company_name=username, email=email)
            elif role == 'admin':
                new_role_instance = Admin(login_id=new_login.id, name=username, email=email)
            elif role == 'college':
                new_role_instance = College(login_id=new_login.id, college_name=username, email=email)
            else:
                flash('Invalid user account type specified.', 'danger')
                return redirect(url_for('auth.signup'))

            db.session.add(new_role_instance)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # Consider logging the exception here for debugging purposes
            flash('An error occurred during signup. Please try again later.', 'danger')
            return redirect(url_for('auth.signup'))

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')
'''

'''@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'user')  # Default to 'user' if role is not provided
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        phone = request.form['phone']

        # Check if username or email already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('auth.signup'))

        # Ensure role is either 'user' or 'admin'
        if role not in ['user', 'admin', 'company']:
            flash('Invalid role specified.', 'danger')
            return redirect(url_for('auth.signup'))

        # Create a new user
        new_user = User(
            username=username,
            role=role,  # Set the specified role
            name=name,
            email=email,
            age=age,
            phone=phone
        )
        new_user.set_password(password)  # Hash the password
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')'''


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the Login table
        login = Login.query.filter_by(username=username).first()
        if not login or not login.check_password(password):
            return render_template('login.html', error='Invalid username or password.')

        # Store session details
        session['login_id'] = login.id
        session['username'] = login.username
        session['role'] = login.role

        # Redirect based on role
        if login.role == 'user':
            user = User.query.filter_by(login_id=login.id).first()
            if not user:
                return render_template('login.html', error='User details not found.')
            session['user_id'] = user.id  
            return redirect(url_for('user.user_dashboard'))
        elif login.role == 'company':
            company = Company.query.filter_by(login_id=login.id).first()
            if not company:
                return render_template('login.html', error='Company details not found.')
            return redirect(url_for('company.company_dashboard'))
        elif login.role == 'admin':
            admin = Admin.query.filter_by(login_id=login.id).first()
            if not admin:
                return render_template('login.html', error='Admin details not found.')
            return redirect(url_for('admin_routes.admin_dashboard'))
        elif login.role == 'college':
            college = College.query.filter_by(login_id=login.id).first()
            session['college_id'] = college.id
            if not college:
                return render_template('login.html', error='College details not found.')
            return redirect(url_for('college.college_dashboard'))

    return render_template('login.html')


# ith login function, ithil when logged in it checks the login table , and if present, it takes the role and goes to corresponding page,


'''@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Find the user by username
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))

        # Login successful, store user information in session
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role

        flash(f'Welcome, {user.name}!', 'success')
        
        # Case-insensitive role check
        if user.role == 'admin':
            return redirect(url_for('admin_routes.admin_dashboard'))
        elif user.role == 'company':
            return redirect(url_for('company.company_dashboard'))
        else:
            return redirect(url_for('user.user_dashboard'))

    return render_template('login.html')'''

@auth_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    session.clear()  # Clears all session variables
    #flash("You have been logged out.", "info")
    # Create a response object for the redirect
    response = redirect(url_for('auth.login'))
    
    # Add headers to clear the browser cache
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response

@auth_blueprint.route('/forgot-password', methods=['GET', 'POST'])
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
def verify_otp():
    if 'otp' not in session or 'otp_time' not in session:
        flash("Session expired. Please request a new OTP.", "danger")
        return redirect(url_for('auth.forgot_password'))

    otp_time = datetime.fromisoformat(session['otp_time'])
    remaining_time = (otp_time + timedelta(minutes=10)) - datetime.utcnow()

    if remaining_time.total_seconds() <= 0:
        session.pop('otp', None)
        session.pop('otp_time', None)
        flash("OTP expired. Please request a new one.", "danger")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session.get('otp'):
            return redirect(url_for('auth.reset_password'))
        else:
            flash("Invalid OTP. Please try again.", "danger")

    return render_template('verify_otp.html', remaining_time=int(remaining_time.total_seconds()))


@auth_blueprint.route('/otp-timer')
def otp_timer():
    """API endpoint to check remaining OTP time."""
    if 'otp_time' not in session:
        return jsonify({'expired': True, 'remaining_time': 0})

    otp_time = datetime.fromisoformat(session['otp_time'])
    remaining_time = (otp_time + timedelta(minutes=10)) - datetime.utcnow()

    if remaining_time.total_seconds() <= 0:
        session.pop('otp', None)
        session.pop('otp_time', None)
        return jsonify({'expired': True, 'remaining_time': 0})

    return jsonify({'expired': False, 'remaining_time': int(remaining_time.total_seconds())})

# Password Reset Route
@auth_blueprint.route('/reset-password', methods=['GET', 'POST'])
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
