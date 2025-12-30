from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime
from admin import admin_bp
from database import get_projects_by_category, get_listed_categories, get_category_by_id, init_db, init_default_categories

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
init_default_categories()

# Context processor to inject current year into all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# Remove hardcoded categories - now loaded from database

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
    categories = get_listed_categories()
    return render_template('portfolio.html', categories=categories, info=PERSONAL_INFO)

@app.route('/portfolio/<category>')
def portfolio_category(category):
    """Individual portfolio category page"""
    category_info = get_category_by_id(category)
    if not category_info:
        return "Category not found", 404
    
    # Check if category is listed
    if not category_info['is_listed']:
        return "Category is currently unlisted", 404
    
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
    
    # Get category info from database
    category_info = get_category_by_id(project['category'])
    
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
