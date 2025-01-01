from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, User,Job

auth_blueprint = Blueprint('auth', __name__)




auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        phone = request.form['phone']

        # Check if username or email already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('auth.signup'))

        # Create a new user
        new_user = User(
            username=username,
            role=role,
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

    return render_template('signup.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
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
        if user.role.lower() == 'admin':
            return redirect(url_for('admin_routes.admin_dashboard'))
        else:
            return redirect(url_for('user.user_dashboard'))

    return render_template('login.html')


@auth_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))
