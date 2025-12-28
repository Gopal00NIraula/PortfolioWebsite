from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import markdown
from database import *

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin credentials from environment variables for security
# In production (PythonAnywhere), set these in your .env file
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password123')  # Change this!

UPLOAD_FOLDER = 'static/images/projects'
README_FOLDER = 'static/readme'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(README_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    """Decorator to require login for admin routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please login to access the admin panel', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """Logout admin"""
    session.pop('admin_logged_in', None)
    flash('Successfully logged out', 'success')
    return redirect(url_for('index'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    projects = get_all_projects()
    return render_template('admin/dashboard.html', projects=projects)

@admin_bp.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    """Create new project"""
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        full_description = request.form.get('full_description', '')
        technologies = request.form.get('technologies')
        project_url = request.form.get('project_url', '')
        github_url = request.form.get('github_url', '')
        featured = 1 if request.form.get('featured') else 0
        
        # Handle README.md upload
        readme_path = ''
        if 'readme' in request.files:
            file = request.files['readme']
            if file and file.filename.endswith('.md'):
                filename = secure_filename(f"{title.replace(' ', '_')}_README.md")
                filepath = os.path.join(README_FOLDER, filename)
                file.save(filepath)
                readme_path = f'readme/{filename}'
                
                # Read and convert markdown to HTML
                with open(filepath, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                    full_description = markdown.markdown(md_content, extensions=['extra', 'codehilite', 'fenced_code'])
        
        # Handle main image upload
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(filepath)
                image_url = f'projects/{filename}'
        
        # Handle multiple screenshots
        screenshots = []
        if 'screenshots' in request.files:
            files = request.files.getlist('screenshots')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(filepath)
                    screenshots.append(f'projects/{filename}')
        
        screenshots_str = ','.join(screenshots)
        add_project(title, category, description, technologies, image_url, project_url, github_url, featured, full_description, screenshots_str)
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/project_form.html', project=None)

@admin_bp.route('/project/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Edit existing project"""
    project = get_project_by_id(project_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        full_description = request.form.get('full_description', '')
        technologies = request.form.get('technologies')
        project_url = request.form.get('project_url', '')
        github_url = request.form.get('github_url', '')
        featured = 1 if request.form.get('featured') else 0
        
        # Handle README.md upload
        if 'readme' in request.files:
            file = request.files['readme']
            if file and file.filename.endswith('.md'):
                filename = secure_filename(f"{title.replace(' ', '_')}_README.md")
                filepath = os.path.join(README_FOLDER, filename)
                file.save(filepath)
                
                # Read and convert markdown to HTML
                with open(filepath, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                    full_description = markdown.markdown(md_content, extensions=['extra', 'codehilite', 'fenced_code'])
        
        # Handle main image upload
        image_url = project['image_url']
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(filepath)
                image_url = f'projects/{filename}'
        
        # Handle multiple screenshots
        screenshots_str = project['screenshots'] if project['screenshots'] else ''
        if 'screenshots' in request.files:
            files = request.files.getlist('screenshots')
            new_screenshots = []
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(filepath)
                    new_screenshots.append(f'projects/{filename}')
            if new_screenshots:
                screenshots_str = ','.join(new_screenshots)
        
        update_project(project_id, title, category, description, technologies, image_url, project_url, github_url, featured, full_description, screenshots_str)
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/project_form.html', project=project)

@admin_bp.route('/project/delete/<int:project_id>')
@login_required
def delete_project_route(project_id):
    """Delete a project"""
    delete_project(project_id)
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))
