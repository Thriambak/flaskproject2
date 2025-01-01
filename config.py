import os

class Config:
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'png'}
    
    basedir = os.path.abspath(os.path.dirname(__file__))

    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'  # For session management and CSRF protection
    
    # For SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'  # SQLite URI (local file-based database)


    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

