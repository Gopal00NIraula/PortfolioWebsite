# PythonAnywhere Deployment Guide

This guide will help you deploy your Flask Portfolio Website to PythonAnywhere.

## Prerequisites

1. A PythonAnywhere account (free tier works fine)
2. Your code uploaded to PythonAnywhere (via Git or file upload)

## Step-by-Step Deployment

### 1. Upload Your Code

**Option A: Using Git (Recommended)**
```bash
# In PythonAnywhere Bash console
cd ~
git clone https://github.com/yourusername/PortfolioWebsite.git
cd PortfolioWebsite
```

**Option B: Upload Files**
- Use the Files tab in PythonAnywhere to upload your files
- Create a folder: `/home/yourusername/PortfolioWebsite`
- Upload all files there

### 2. Set Up Virtual Environment

In the PythonAnywhere Bash console:

```bash
cd ~/PortfolioWebsite
mkvirtualenv --python=/usr/bin/python3.10 portfolio-env
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file from the example:

```bash
cd ~/PortfolioWebsite
cp .env.example .env
nano .env  # or use the Files tab editor
```

Edit the `.env` file and change:
- `SECRET_KEY` - Generate a random string (use: `python -c "import secrets; print(secrets.token_hex(32))"`)
- `ADMIN_USERNAME` - Your desired admin username
- `ADMIN_PASSWORD` - A strong password

### 4. Initialize the Database

```bash
cd ~/PortfolioWebsite
workon portfolio-env
python -c "from database import init_db; init_db()"
```

### 5. Set Up the Web App

1. Go to the **Web** tab in PythonAnywhere
2. Click **Add a new web app**
3. Choose **Manual configuration** (not Flask)
4. Select **Python 3.10**

### 6. Configure WSGI File

1. In the Web tab, find the **Code** section
2. Click on the WSGI configuration file link
3. **Delete all contents** and replace with:

```python
import sys
import os

# Add your project directory to the sys.path
# Replace 'yourusername' with your actual PythonAnywhere username
project_home = '/home/yourusername/PortfolioWebsite'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app
from app import app as application
```

**Important:** Replace `yourusername` with your actual PythonAnywhere username!

### 7. Configure Virtual Environment

In the Web tab:
1. Find the **Virtualenv** section
2. Enter: `/home/yourusername/.virtualenvs/portfolio-env`
3. Replace `yourusername` with your actual username

### 8. Configure Static Files

In the Web tab, add these static file mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/PortfolioWebsite/static/` |

Replace `yourusername` with your actual username.

### 9. Set Environment Variables (Alternative Method)

If the `.env` file doesn't work, you can set environment variables directly in the WSGI file:

```python
import os

os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['ADMIN_USERNAME'] = 'admin'
os.environ['ADMIN_PASSWORD'] = 'your-password-here'
os.environ['FLASK_ENV'] = 'production'
```

### 10. Reload Your Web App

1. Go back to the **Web** tab
2. Click the green **Reload** button
3. Your site should now be live at: `yourusername.pythonanywhere.com`

## Post-Deployment

### Accessing the Admin Panel

Visit: `yourusername.pythonanywhere.com/admin/login`

Use the credentials you set in your `.env` file.

### Adding Projects

1. Log in to the admin panel
2. Click "Add New Project"
3. Fill in the project details
4. Upload images and README files

### Updating Your Code

If you make changes locally:

```bash
# In PythonAnywhere Bash console
cd ~/PortfolioWebsite
git pull  # if using Git
# or upload files via Files tab

# Reload the web app from the Web tab
```

### Creating Database Backups

```bash
cd ~/PortfolioWebsite
cp portfolio.db portfolio_backup_$(date +%Y%m%d).db
```

## Troubleshooting

### Site Shows Error

1. Check the **Error log** in the Web tab
2. Check the **Server log** in the Web tab
3. Common issues:
   - Wrong paths in WSGI file
   - Virtual environment not activated
   - Missing dependencies

### Static Files Not Loading

- Verify static file mappings in Web tab
- Check file paths are absolute
- Ensure files were uploaded correctly

### Database Errors

```bash
cd ~/PortfolioWebsite
workon portfolio-env
python -c "from database import init_db; init_db()"
```

### Can't Login to Admin

- Check your `.env` file credentials
- Try setting environment variables directly in WSGI file
- Make sure session secret key is set

## Important Security Notes

1. **Never commit `.env` file to Git** - Add it to `.gitignore`
2. **Change default passwords** before deploying
3. **Use strong secret key** - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
4. Keep your PythonAnywhere account secure with a strong password

## Free Tier Limitations

PythonAnywhere free tier includes:
- One web app at `yourusername.pythonanywhere.com`
- Limited CPU/bandwidth (sufficient for portfolio sites)
- Must reload your site every 3 months to keep it active

## Need Help?

- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- PythonAnywhere Help: https://help.pythonanywhere.com/
- Flask Documentation: https://flask.palletsprojects.com/

## File Checklist

Make sure these files are uploaded:
- ✅ `app.py`
- ✅ `wsgi.py` (created for you)
- ✅ `database.py` (updated for production)
- ✅ `admin.py`
- ✅ `requirements.txt` (updated)
- ✅ `.env` (create from `.env.example`)
- ✅ All `templates/` folder files
- ✅ All `static/` folder files
- ✅ `run.py` (optional, for local development)

## Quick Command Reference

```bash
# Activate virtual environment
workon portfolio-env

# Install/update dependencies
pip install -r requirements.txt

# Initialize database
python -c "from database import init_db; init_db()"

# Check Python path
python -c "import sys; print(sys.path)"

# Test import
python -c "from app import app; print('Success!')"

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

Good luck with your deployment! 🚀
