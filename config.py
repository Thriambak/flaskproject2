import os

class Config:
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'png'}
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE = os.path.join(basedir, 'your_database.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'  # For session management and CSRF protection
    
    # Connection string for PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/mydb'
    # MySql URI --> 'mysql+pymysql://username:password@localhost:3306/db_name'

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
