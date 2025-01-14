from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from config import Config
from models import db, User, Job, Login, Company

auth_blueprint = Blueprint('auth', __name__)

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
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
            new_admin = Admin(login_id=new_login.id, name=username)
            db.session.add(new_admin)
        else:
            flash('Invalid role specified.', 'danger')
            return redirect(url_for('auth.signup'))

        db.session.commit()
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


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
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))

        # Store session details
        session['login_id'] = login.id
        session['username'] = login.username
        session['role'] = login.role

        # Redirect based on role
        if login.role == 'user':
            user = User.query.filter_by(login_id=login.id).first()
            if not user:
                flash('User details not found.', 'danger')
                return redirect(url_for('auth.login'))
            return redirect(url_for('user.user_dashboard'))
        elif login.role == 'company':
            company = Company.query.filter_by(login_id=login.id).first()
            if not company:
                flash('Company details not found.', 'danger')
                return redirect(url_for('auth.login'))
            return redirect(url_for('company.company_dashboard'))
        elif login.role == 'admin':
            admin = Admin.query.filter_by(login_id=login.id).first()
            if not admin:
                flash('Admin details not found.', 'danger')
                return redirect(url_for('auth.login'))
            return redirect(url_for('admin.admin_dashboard'))

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

