import os

class Config:
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'png'}
    PROFILE_PICS_FOLDER = os.path.join(UPLOAD_FOLDER, 'profile_pics')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max upload
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE = os.path.join(basedir, 'your_database.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'  # For session management and CSRF protection
    
    # Connection string for PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/mydb'
    # MySql URI --> 'mysql+pymysql://username:password@localhost:3306/db_name'
    @staticmethod
    def init_app(app):
        os.makedirs(Config.PROFILE_PICS_FOLDER, exist_ok=True)
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
