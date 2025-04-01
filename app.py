from flask import Flask, render_template, g
import sqlite3
from flask_login import LoginManager
from config import Config
from flask import Flask, session, redirect, url_for
from models import db, User,Job
from auth import auth_blueprint
from user import user_blueprint
from company import company_blueprint
from college import college_blueprint
from admin_routes import admin_blueprint
from flask_migrate import Migrate
from flask import jsonify, request
from flask_mail import Mail

from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session pip install mysql-connector-python


# Ensure upload folder exists
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)

# Load configuration from Config object          
app.config.from_object(Config)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your mail server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Sender email address
app.config['MAIL_PASSWORD'] = 'your_email_password'  # Sender email password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

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

# Initialize Flask-Login
@app.route('/')
def index():
    return render_template('home.html')



if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)


''' Routes to test db

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return {'message': 'User added successfully'}

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])
    
'''