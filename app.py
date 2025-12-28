from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime
from admin import admin_bp
from database import get_projects_by_category, init_db

app = Flask(__name__)

# Configuration
# Use environment variable for secret key, fallback to default for local development
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Register admin blueprint
app.register_blueprint(admin_bp)

# Initialize database
init_db()

# Context processor to inject current year into all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# Portfolio project categories
PORTFOLIO_CATEGORIES = [
    {'id': 'python', 'name': 'Python Projects', 'icon': '🐍', 'color': '#3776ab'},
    {'id': 'web', 'name': 'Web Development', 'icon': '🌐', 'color': '#e34f26'},
    {'id': 'java', 'name': 'Java Projects', 'icon': '☕', 'color': '#007396'},
    {'id': 'cpp', 'name': 'C++ Projects', 'icon': '⚡', 'color': '#00599c'},
    {'id': 'android', 'name': 'Android Apps', 'icon': '📱', 'color': '#3ddc84'},
    {'id': 'unity', 'name': 'Unity Games', 'icon': '🎮', 'color': '#000000'},
    {'id': 'blender', 'name': '3D Modeling', 'icon': '🎨', 'color': '#f5792a'},
    {'id': 'uxui', 'name': 'UX/UI Design', 'icon': '✨', 'color': '#ff6b6b'}
]

# Personal information
PERSONAL_INFO = {
    'name': 'Gopal Niraula',
    'title': 'Computer Programmer',
    'location': 'Nepal',
    'university': 'Youngstown State University',
    'major': 'Computer Science',
    'bio': "Hi, I'm Gopal Niraula — a Computer Science student at Youngstown State University, passionate about data analytics and problem-solving. I thrive on turning data into insights that can drive smarter decisions.",
    'social_links': {
        'discord': 'https://discordapp.com/users/816671772648275980',
        'facebook': 'https://www.facebook.com/rupesh.niroula.3/',
        'linkedin': '',
        'email': ''
    }
}

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', info=PERSONAL_INFO)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', info=PERSONAL_INFO)

@app.route('/portfolio')
def portfolio():
    """Portfolio page"""
    return render_template('portfolio.html', categories=PORTFOLIO_CATEGORIES, info=PERSONAL_INFO)

@app.route('/portfolio/<category>')
def portfolio_category(category):
    """Individual portfolio category page"""
    category_info = next((cat for cat in PORTFOLIO_CATEGORIES if cat['id'] == category), None)
    if not category_info:
        return "Category not found", 404
    
    # Get projects from database
    projects = get_projects_by_category(category)
    
    return render_template('portfolio/category.html', 
                         category=category_info, 
                         projects=projects,
                         info=PERSONAL_INFO)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    """Individual project detail page"""
    from database import get_project_by_id
    project = get_project_by_id(project_id)
    
    if not project:
        return "Project not found", 404
    
    # Get category info
    category_info = next((cat for cat in PORTFOLIO_CATEGORIES if cat['id'] == project['category']), None)
    
    return render_template('portfolio/project_detail.html', 
                         project=project,
                         category=category_info,
                         info=PERSONAL_INFO)

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contacts.html', info=PERSONAL_INFO)

@app.route('/api/categories')
def api_categories():
    """API endpoint to get portfolio categories"""
    return jsonify(PORTFOLIO_CATEGORIES)

# Only run the development server when executed directly
# PythonAnywhere will use the WSGI file instead
if __name__ == '__main__':
    # This is for local development only
    app.run(debug=True, host='0.0.0.0', port=5000)
