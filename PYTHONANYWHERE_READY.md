# PythonAnywhere Deployment - Quick Start

Your Flask Portfolio Website is now ready for deployment to PythonAnywhere! 🚀

## What Was Changed

### New Files Created:
1. **wsgi.py** - WSGI configuration for PythonAnywhere
2. **.env.example** - Template for environment variables
3. **DEPLOYMENT.md** - Comprehensive deployment guide
4. **setup_pythonanywhere.sh** - Automated setup script

### Modified Files:
1. **app.py** - Updated to use environment variables for SECRET_KEY and DEBUG
2. **admin.py** - Updated to use environment variables for admin credentials
3. **database.py** - Updated to use absolute paths for database file
4. **requirements.txt** - Added python-dotenv for environment variable support

## Quick Deployment Steps

### 1. Upload to PythonAnywhere
```bash
# Option A: Git (Recommended)
cd ~
git clone https://github.com/yourusername/PortfolioWebsite.git
cd PortfolioWebsite

# Option B: Use PythonAnywhere Files tab to upload
```

### 2. Run Setup Script
```bash
cd ~/PortfolioWebsite
bash setup_pythonanywhere.sh
```

### 3. Configure Secrets
```bash
# Edit .env file
nano .env

# Change these values:
SECRET_KEY=your-randomly-generated-secret-key
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-secure-password
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Set Up Web App

Go to PythonAnywhere **Web** tab:

1. Click "Add a new web app"
2. Choose "Manual configuration"
3. Select "Python 3.10"

### 5. Configure WSGI File

Click on WSGI configuration file and replace with:

```python
import sys
import os

# REPLACE 'yourusername' WITH YOUR ACTUAL USERNAME!
project_home = '/home/yourusername/PortfolioWebsite'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

os.environ['FLASK_ENV'] = 'production'

from app import app as application
```

### 6. Set Virtual Environment

In Web tab, Virtualenv section:
```
/home/yourusername/.virtualenvs/portfolio-env
```

### 7. Configure Static Files

Add this mapping in Web tab:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/PortfolioWebsite/static/` |

### 8. Reload Web App

Click the big green **Reload** button!

Your site will be live at: **yourusername.pythonanywhere.com**

## Admin Access

Visit: `yourusername.pythonanywhere.com/admin/login`

Use the credentials you set in `.env` file.

## Important Notes

✅ **Security:**
- `.env` file is in `.gitignore` - never commit it!
- Change all default passwords before deploying
- Use a strong, random SECRET_KEY

✅ **Database:**
- Database file is created automatically
- Located at: `/home/yourusername/PortfolioWebsite/portfolio.db`
- Not committed to Git (in `.gitignore`)

✅ **Static Files:**
- Images and CSS are in `/static/` folder
- Must configure static file mapping in PythonAnywhere
- Upload folder: `static/images/projects/`

## Testing Locally Before Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python run.py

# Visit: http://localhost:5000
```

## Troubleshooting

**Site shows error?**
- Check Error log in Web tab
- Verify username in WSGI file
- Check virtual environment path

**Can't login to admin?**
- Verify .env file exists
- Check credentials in .env
- Try setting environment variables directly in WSGI

**Static files not loading?**
- Check static file mapping in Web tab
- Verify paths are absolute
- Ensure files were uploaded

## Need More Help?

See **DEPLOYMENT.md** for the complete step-by-step guide with screenshots and troubleshooting.

---

**Ready to deploy? Follow the steps above and you'll be live in minutes!** 🎉
