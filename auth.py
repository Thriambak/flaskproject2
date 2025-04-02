from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from config import Config
from models import Admin, College, db, User, Job, Login, Company
import re

auth_blueprint = Blueprint('auth', __name__)

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
        username = request.form['username']#ithil ellam varum, company name, admin name, college name and username. ithaan default name 
        password = request.form['password']
        role = request.form.get('role', 'user')  # Default is 'user'
        email = request.form['email']
        # phone = request.form.get('phone')
        # age = request.form.get('age')
        # address = request.form.get('address')

        # Check if username or email already exists in the Login table
        if Login.query.filter_by(username=username).first(): # or Login.query.join(User).filter(User.email == email).first()
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('auth.signup'))

        # Create entry in the Login table
        new_login = Login(username=username, role=role)
        new_login.set_password(password)
        db.session.add(new_login)
        db.session.flush()  # To get the login ID before committing

        # Insert role-specific data
        if role == 'user':
            new_user = User(login_id=new_login.id, name=username, email=email)  #, phone=phone, age=age
            db.session.add(new_user)
        elif role == 'company':
            new_company = Company(login_id=new_login.id, company_name=username, email=email)  #, address=address
            db.session.add(new_company)
        elif role == 'admin':
            new_admin = Admin(login_id=new_login.id, name=username, email=email)
            db.session.add(new_admin)
        elif role == 'college':
            new_college = College(login_id=new_login.id, college_name=username, email=email)
            db.session.add(new_college)    
        else:
            flash('Invalid role specified.', 'danger')
            return redirect(url_for('auth.signup'))

        db.session.commit()
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')
'''


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
    flash("You have been logged out.", "info")
    # Create a response object for the redirect
    response = redirect(url_for('auth.login'))
    
    # Add headers to clear the browser cache
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response
