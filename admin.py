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

# Use absolute paths for upload folders (critical for PythonAnywhere)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images', 'projects')
README_FOLDER = os.path.join(BASE_DIR, 'static', 'readme')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Ensure upload directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
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

def get_category_choices():
    """Helper function to get category choices for forms"""
    categories = get_all_categories()
    return [(cat['id'], f"{cat['icon']} {cat['name']}") for cat in categories]

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
    
    categories = get_category_choices()
    return render_template('admin/project_form.html', project=None, categories=categories)

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
    
    categories = get_category_choices()
    return render_template('admin/project_form.html', project=project, categories=categories)

@admin_bp.route('/project/delete/<int:project_id>')
@login_required
def delete_project_route(project_id):
    """Delete a project"""
    delete_project(project_id)
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/categories')
@login_required
def manage_categories():
    """Manage categories page"""
    from database import get_all_categories
    categories = get_all_categories()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/category/toggle/<category_id>', methods=['POST'])
@login_required
def toggle_category(category_id):
    """Toggle category visibility (list/unlist)"""
    from database import toggle_category_visibility
    new_state = toggle_category_visibility(category_id)
    
    if new_state is not None:
        status = "listed" if new_state else "unlisted"
        flash(f'Category {status} successfully!', 'success')
    else:
        flash('Category not found!', 'error')
    
    return redirect(url_for('admin.manage_categories'))

@admin_bp.route('/category/add', methods=['POST'])
@login_required
def add_category():
    """Add a new category"""
    from database import add_category as db_add_category, get_all_categories
    import os
    from werkzeug.utils import secure_filename
    
    category_id = request.form.get('category_id', '').strip().lower()
    name = request.form.get('name', '').strip()
    icon = request.form.get('icon', '').strip()
    color = request.form.get('color', '#ff8d29').strip()
    
    # Validation
    if not category_id or not name:
        flash('Category ID and Name are required!', 'error')
        return redirect(url_for('admin.manage_categories'))
    
    # Handle icon image upload
    icon_image = None
    if 'icon_image' in request.files:
        file = request.files['icon_image']
        if file and file.filename:
            filename = secure_filename(file.filename)
            # Create category-icons directory if it doesn't exist
            icons_dir = os.path.join('static', 'images', 'category-icons')
            os.makedirs(icons_dir, exist_ok=True)
            
            # Save with category_id as filename
            ext = os.path.splitext(filename)[1]
            icon_filename = f"{category_id}{ext}"
            file.save(os.path.join(icons_dir, icon_filename))
            icon_image = f"category-icons/{icon_filename}"
    
    # Get max sort order
    categories = get_all_categories()
    max_sort = max([cat['sort_order'] for cat in categories], default=0) if categories else 0
    
    # Add category
    success = db_add_category(category_id, name, icon, color, max_sort + 1, icon_image)
    
    if success:
        flash(f'Category "{name}" added successfully!', 'success')
    else:
        flash('Category ID already exists or database error!', 'error')
    
    return redirect(url_for('admin.manage_categories'))

@admin_bp.route('/category/delete/<category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    """Delete a category"""
    from database import delete_category as db_delete_category
    
    projects_count = db_delete_category(category_id)
    
    if projects_count > 0:
        flash(f'Category deleted! {projects_count} project(s) were updated to have no category.', 'warning')
    else:
        flash('Category deleted successfully!', 'success')
    
    return redirect(url_for('admin.manage_categories'))

@admin_bp.route('/category/edit/<category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    """Edit a category"""
    from database import get_category_by_id, update_category
    import os
    from werkzeug.utils import secure_filename
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        icon = request.form.get('icon', '').strip()
        color = request.form.get('color', '#ff8d29').strip()
        
        if not name:
            flash('Category name is required!', 'error')
            return redirect(url_for('admin.edit_category', category_id=category_id))
        
        # Handle icon image upload
        icon_image = None
        if 'icon_image' in request.files:
            file = request.files['icon_image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                icons_dir = os.path.join('static', 'images', 'category-icons')
                os.makedirs(icons_dir, exist_ok=True)
                
                ext = os.path.splitext(filename)[1]
                icon_filename = f"{category_id}{ext}"
                file.save(os.path.join(icons_dir, icon_filename))
                icon_image = f"category-icons/{icon_filename}"
        
        # Update category
        success = update_category(category_id, name, icon, color, icon_image)
        
        if success:
            flash(f'Category "{name}" updated successfully!', 'success')
            return redirect(url_for('admin.manage_categories'))
        else:
            flash('Failed to update category!', 'error')
    
    # GET request - show edit form
    category = get_category_by_id(category_id)
    if not category:
        flash('Category not found!', 'error')
        return redirect(url_for('admin.manage_categories'))
    
    return render_template('admin/edit_category.html', category=category)
