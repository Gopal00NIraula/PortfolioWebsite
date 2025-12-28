"""
WSGI Configuration for PythonAnywhere Deployment
This file is used by PythonAnywhere to run your Flask application.

Instructions:
1. Upload your code to PythonAnywhere
2. In the Web tab, set the WSGI configuration file path to this file
3. Update the project path below to match your PythonAnywhere username
"""

import sys
import os

# Add your project directory to the sys.path
# IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username
project_home = '/home/yourusername/PortfolioWebsite'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables from .env file (if python-dotenv is installed)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(project_home, '.env'))
except ImportError:
    # If python-dotenv is not installed, you can set variables manually here:
    # os.environ['SECRET_KEY'] = 'your-secret-key'
    # os.environ['ADMIN_USERNAME'] = 'admin'
    # os.environ['ADMIN_PASSWORD'] = 'your-password'
    pass

# Set environment to production
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = 'False'

# Import the Flask app
from app import app as application

# This is what PythonAnywhere will use
# Don't change the variable name 'application'
