from flask import Flask, jsonify, request, make_response, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager
from config import Config
from models import db, User, Company, Job, JobApplication
from auth import auth_blueprint
from user import user_blueprint
from company import company_blueprint
from admin_routes import admin_blueprint
from flask_migrate import Migrate
from flask_mail import Mail
import os
from sqlalchemy import or_
from datetime import datetime

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS

app.secret_key = 'your_secret_key'

# Ensure upload folder exists
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)

app.config.from_object(Config)

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

mail = Mail(app)

# Register Blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(company_blueprint, url_prefix='/company')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
# Removed college blueprint registration

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return jsonify({"message": "Flask API Running"}), 200

# ========== USERS API ==========
@app.route('/users', methods=['GET'])
def get_users():
    query = User.query
    
    if 'q' in request.args and request.args['q']:
        search_term = request.args['q']
        
        if "name:" in search_term:
            name_term = search_term.split("name:")[1].strip()
            query = query.filter(User.name.ilike(f"%{name_term}%"))
        elif "email:" in search_term:
            email_term = search_term.split("email:")[1].strip()
            query = query.filter(User.email.ilike(f"%{email_term}%"))
        else:
            search_term = f"%{search_term}%"
            query = query.filter(or_(
    		User.name.ilike(search_term),
    		User.email.ilike(search_term)
		))
    
    users = query.all()
    users_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    
    response = make_response(jsonify(users_data))
    response.headers['Content-Range'] = f'users 0-{len(users_data)-1}/{len(users_data)}'
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return response

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        name=data['name'],
        email=data['email'],
        # Add other user fields as needed
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!", "id": new_user.id}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    for key, value in data.items():
        setattr(user, key, value)
    
    db.session.commit()
    return jsonify({"message": "User updated successfully!"})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"})

@app.route('/users/bulk', methods=['DELETE'])
def delete_users_bulk():
    user_ids = request.json.get('ids', [])
    User.query.filter(User.id.in_(user_ids)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({"message": f"Deleted {len(user_ids)} users successfully"})

# ========== COMPANIES API ==========
@app.route('/companies', methods=['GET'])
def get_companies():
    query = Company.query
    
    if 'q' in request.args and request.args['q']:
        search_term = request.args['q']
        
        if "company_name:" in search_term:
            name_term = search_term.split("company_name:")[1].strip()
            query = query.filter(Company.company_name.ilike(f"%{name_term}%"))
        elif "email:" in search_term:
            email_term = search_term.split("email:")[1].strip()
            query = query.filter(Company.email.ilike(f"%{email_term}%"))
        else:
            search_term = f"%{search_term}%"
            query = query.filter(or_(
    		Company.company_name.ilike(search_term),
    		Company.email.ilike(search_term)
		))
    companies = query.all()
    companies_data = [{
        'id': company.id,
        'company_name': company.company_name,
        'email': company.email
    } for company in companies]
    
    response = make_response(jsonify(companies_data))
    response.headers['Content-Range'] = f'companies 0-{len(companies_data)-1}/{len(companies_data)}'
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return response

@app.route('/companies', methods=['POST'])
def create_company():
    data = request.json
    new_company = Company(
        company_name=data['company_name'],
        email=data['email']
    )
    db.session.add(new_company)
    db.session.commit()
    return jsonify({"message": "Company created successfully!", "id": new_company.id}), 201

@app.route('/companies/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404
    
    data = request.json
    for key, value in data.items():
        setattr(company, key, value)
    
    db.session.commit()
    return jsonify({"message": "Company updated successfully!"})

@app.route('/companies/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404
    
    db.session.delete(company)
    db.session.commit()
    return jsonify({"message": "Company deleted successfully!"})

@app.route('/companies/bulk', methods=['DELETE'])
def delete_companies_bulk():
    company_ids = request.json.get('ids', [])
    Company.query.filter(Company.id.in_(company_ids)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({"message": f"Deleted {len(company_ids)} companies successfully"})

# New route for company profile redirection
@app.route('/company/company_profile', methods=['GET'])
def company_profile_form():
    return jsonify({"message": "Company profile form page. This endpoint would normally serve HTML in a production app."}), 200

# New route for handling company profile submission
@app.route('/company/company_profile', methods=['POST'])
def submit_company_profile():
    data = request.json
    try:
        new_company = Company(
            company_name=data['company_name'],
            email=data['email'],
            # Add any additional fields your Company model supports
            # Such as description, address, website, etc.
        )
        db.session.add(new_company)
        db.session.commit()
        return jsonify({"success": True, "message": "Company profile created successfully!", "id": new_company.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error creating company profile: {str(e)}"}), 500

# ========== JOBS API ==========
@app.route('/jobs', methods=['GET'])
def get_jobs():
    query = Job.query
    
    if 'q' in request.args and request.args['q']:
        search_term = request.args['q']
        
        if "title:" in search_term:
            title_term = search_term.split("title:")[1].strip()
            query = query.filter(Job.title.ilike(f"%{title_term}%"))
        elif "job_type:" in search_term:
            type_term = search_term.split("job_type:")[1].strip()
            query = query.filter(Job.job_type.ilike(f"%{type_term}%"))
        elif "location:" in search_term:
            location_term = search_term.split("location:")[1].strip()
            query = query.filter(Job.location.ilike(f"%{location_term}%"))
        elif "status:" in search_term:
            status_term = search_term.split("status:")[1].strip()
            query = query.filter(Job.status.ilike(f"%{status_term}%"))
        else:
            search_term = f"%{search_term}%"
            query = query.filter(or_(
    		Job.title.ilike(search_term),
    		Job.job_type.ilike(search_term),
    		Job.location.ilike(search_term),
    		Job.status.ilike(search_term)
		))
    
    jobs = query.all()
    jobs_data = [{
        'id': job.job_id,
        'job_id': job.job_id,
        'title': job.title,
        'description': job.description,
        'job_type': job.job_type,
        'skills': job.skills,
        'years_of_exp': job.years_of_exp,
        'certifications': job.certifications,
        'location': job.location,
        'salary': job.salary,
        'total_vacancy': job.total_vacancy,
        'filled_vacancy': job.filled_vacancy,
        'status': job.status,
        'form_url': job.form_url,
        'deadline': job.deadline.strftime('%Y-%m-%d') if job.deadline else None,
        'created_by': job.created_by
    } for job in jobs]
    
    response = make_response(jsonify(jobs_data))
    response.headers['Content-Range'] = f'jobs 0-{len(jobs_data)-1}/{len(jobs_data)}'
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return response

@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.json
    
    # Parse deadline if it exists
    deadline = None
    if 'deadline' in data and data['deadline']:
        try:
            deadline = datetime.strptime(data['deadline'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid deadline format. Use YYYY-MM-DD"}), 400
    
    new_job = Job(
        title=data['title'],
        description=data['description'],
        job_type=data['job_type'],
        skills=data.get('skills', ''),
        years_of_exp=data['years_of_exp'],
        certifications=data.get('certifications', ''),
        location=data['location'],
        salary=data['salary'],
        total_vacancy=data['total_vacancy'],
        filled_vacancy=data.get('filled_vacancy', 0),
        status=data['status'],
        form_url=data.get('form_url', ''),
        deadline=deadline,
        created_by=data['created_by']
    )
    
    db.session.add(new_job)
    db.session.commit()
    return jsonify({"message": "Job created successfully!", "id": new_job.job_id}), 201

@app.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"message": "Job not found"}), 404
    
    data = request.json
    
    # Handle deadline update
    if 'deadline' in data:
        if data['deadline']:
            try:
                job.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d')
            except ValueError:
                return jsonify({"error": "Invalid deadline format. Use YYYY-MM-DD"}), 400
        else:
            job.deadline = None
    
    # Update other fields
    for key, value in data.items():
        if key != 'deadline':  # already handled
            setattr(job, key, value)
    
    db.session.commit()
    return jsonify({"message": "Job updated successfully!"})

@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"message": "Job not found"}), 404
    
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted successfully!"})

@app.route('/jobs/bulk', methods=['DELETE'])
def delete_jobs_bulk():
    job_ids = request.json.get('ids', [])
    if not job_ids:
        return jsonify({"message": "No IDs provided"}), 400
    
    try:
        # Delete all jobs with matching IDs
        Job.query.filter(Job.job_id.in_(job_ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({"message": f"Deleted {len(job_ids)} jobs successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# ========== DASHBOARD API ==========
@app.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    total_users = User.query.count()
    total_companies = Company.query.count()
    total_jobs = Job.query.count()
    total_applications = JobApplication.query.count()
    
    trends = [
        {"x": "2025-03-20", "applications": 0, "logins": 3},
        {"x": "2025-03-25", "applications": 0, "logins": 16},
        {"x": "2025-03-30", "applications": 1, "logins": 27}
    ]
    
    return jsonify({
        "metrics": {
            "users": total_users,
            "companies": total_companies,
            "jobs": total_jobs,
            "applications": total_applications
        },
        "trends": trends
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)