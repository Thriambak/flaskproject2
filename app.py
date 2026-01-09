from flask import Flask, render_template, g, session, redirect, flash
from flask import jsonify, request, make_response, url_for
from datetime import datetime, timedelta
import sqlite3
from flask_cors import CORS
from flask_login import LoginManager
from config import Config
from models import db, User, Job, Company, JobApplication, Login, Favorite, Communication, Notification, Couponuser, ResumeCertification, Certification
from auth import auth_blueprint
from user import user_blueprint
from company import company_blueprint
from college import college_blueprint
from admin import admin_blueprint
from flask_migrate import Migrate
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import os
import uuid
from sqlalchemy import or_
from datetime import datetime
import pytz
import re
import calendar

app = Flask(__name__)

# SECRET KEY - Set first
app.secret_key = 'your_secret_key'  # Change to secure random key in production

# SESSION CONFIGURATION - Minimal required settings
app.config['SESSION_COOKIE_NAME'] = 'admin_session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set True in production with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# CORS CONFIGURATION - Minimal required settings
# Place after app initialization and before blueprint registration
CORS(app, 
     origins=["http://127.0.0.1:3000"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "X-Requested-With", "Authorization"],
     expose_headers=["Content-Range", "X-Content-Range"],
     supports_credentials=True)


# Ensure upload folder exists
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)

# Load configuration from Config object          
app.config.from_object(Config)

# Set the session lifetime to 1 hour (3600 seconds) for inactivity logout
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your mail server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'employeerecruitment123@gmail.com'  # Sender email address
app.config['MAIL_PASSWORD'] = 'gbpanjpyqscfqykr'  # Sender email password
app.config['MAIL_DEFAULT_SENDER'] = 'employeerecruitment123@gmail.com'

# Initialize Flask-Mail
mail = Mail(app)

# Register blueprints with URL prefixes
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(company_blueprint, url_prefix='/company')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(college_blueprint, url_prefix='/college')

db.init_app(app)
migrate = Migrate(app, db)

# This function runs before each request to handle session timeout AND ban checks
@app.before_request
def before_request_handler():
    session.permanent = True
    if 'login_id' in session:
        # Exclude static files from these checks for efficiency
        if request.endpoint and 'static' in request.endpoint:
            return
        
        # Helper function to correctly log out while preserving the flash message
        def logout_and_flash(message, category):
            flash(message, category)
            # Manually remove only the keys related to authentication.
            session.pop('login_id', None)
            session.pop('username', None)
            session.pop('role', None)
            session.pop('user_id', None)
            session.pop('company_id', None)
            session.pop('college_id', None)
            session.pop('last_activity', None)
            session.pop('session_token', None) # Also remove the token
            return redirect(url_for('auth.login'))

        # 0. Check for session validity by comparing tokens
        login_entry = Login.query.filter_by(id=session['login_id']).first() # Use get_or_404 for simplicity
        
        if not login_entry:
            # Session record not found
            session.clear()
            return redirect(url_for('auth.login'))
        
        # If the token in the user's cookie doesn't match the one in the DB, log them out.
        if login_entry.session_token != session.get('session_token'):
            return logout_and_flash('Your session has expired because your password was changed. Please log in again.', 'info')

        now = datetime.utcnow()
        
        # 1. Check for session inactivity
        if 'last_activity' in session:
            last_activity = session['last_activity']
            if last_activity.tzinfo is not None:
                last_activity = last_activity.replace(tzinfo=None)
            if now - last_activity > app.config['PERMANENT_SESSION_LIFETIME']:
                flash('You have been logged out due to inactivity.', 'info')
                # session.clear()
                return redirect(url_for('auth.login'))

        # 2. Check for banned status on every request
        role = session.get('role')
        login_id = session.get('login_id')
        is_banned = False

        if role == 'user':
            user = User.query.filter_by(login_id=login_id).first()
            if user and user.is_banned:
                is_banned = True
        elif role == 'company':
            company = Company.query.filter_by(login_id=login_id).first()
            if company and company.is_banned:
                is_banned = True
        
        if is_banned:
            session.clear()
            flash('Your account has been suspended. Please contact support.', 'danger')
            return redirect(url_for('auth.login'))

        # If all checks pass, update the last activity time
        session['last_activity'] = now

# Initialize Flask-Home
@app.route('/')
def index():
    return render_template('home.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
