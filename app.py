from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from flask import Flask, session, redirect, url_for
from config import Config
from models import db, User,Job
from auth import auth_blueprint
from user import user_blueprint
from flask_migrate import Migrate
from admin_routes import admin_blueprint
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Ensure upload folder exists
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)

# Load configuration from Config object
app.config.from_object(Config)

# Register blueprints with URL prefixes
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
db.init_app(app)


migrate = Migrate(app, db)

# Register blueprints


# Initialize Flask-Login

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
