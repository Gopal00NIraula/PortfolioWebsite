# Pre-Deployment Checklist

Before deploying to PythonAnywhere, make sure you've completed these steps:

## Local Preparation

- [ ] All files committed to Git (except .env, *.db, and files in .gitignore)
- [ ] Tested the application locally with `python run.py`
- [ ] Verified admin login works locally
- [ ] All project images and content added
- [ ] README files for projects prepared

## Files to Upload

- [ ] `app.py` (updated with environment variables)
- [ ] `wsgi.py` (WSGI configuration)
- [ ] `admin.py` (updated with environment variables)
- [ ] `database.py` (updated with absolute paths)
- [ ] `requirements.txt` (includes python-dotenv)
- [ ] `.env.example` (template for environment variables)
- [ ] `templates/` folder (all HTML templates)
- [ ] `static/` folder (CSS, JavaScript, images)
- [ ] `run.py` (optional, for local development)

## PythonAnywhere Setup

### Initial Setup
- [ ] Created PythonAnywhere account
- [ ] Uploaded/cloned code to `/home/yourusername/PortfolioWebsite`
- [ ] Ran `setup_pythonanywhere.sh` script
- [ ] Created `.env` file from `.env.example`

### Environment Variables (.env file)
- [ ] Changed `SECRET_KEY` to a random string
- [ ] Changed `ADMIN_USERNAME` to your desired username
- [ ] Changed `ADMIN_PASSWORD` to a strong password
- [ ] Verified `FLASK_ENV=production`
- [ ] Verified `FLASK_DEBUG=False`

### Virtual Environment
- [ ] Created virtual environment: `mkvirtualenv --python=/usr/bin/python3.10 portfolio-env`
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Verified installation: `pip list`

### Database
- [ ] Initialized database: `python -c "from database import init_db; init_db()"`
- [ ] Verified database file created: `ls -l portfolio.db`

### Web App Configuration
- [ ] Created new web app (Manual configuration, Python 3.10)
- [ ] Updated WSGI file with correct username
- [ ] Set virtual environment path: `/home/yourusername/.virtualenvs/portfolio-env`
- [ ] Added static file mapping: `/static/` → `/home/yourusername/PortfolioWebsite/static/`

### WSGI File
- [ ] Replaced `yourusername` with actual PythonAnywhere username
- [ ] Verified project_home path is correct
- [ ] Saved WSGI file

### Testing
- [ ] Clicked "Reload" button in Web tab
- [ ] Visited site: `yourusername.pythonanywhere.com`
- [ ] Homepage loads correctly
- [ ] Static files (CSS, images) load correctly
- [ ] Navigation works (About, Portfolio, Contact)
- [ ] Admin login page accessible: `/admin/login`
- [ ] Can login to admin with credentials from .env
- [ ] Can view admin dashboard

## Post-Deployment

### Security
- [ ] Verified `.env` file is NOT committed to Git
- [ ] Changed all default passwords
- [ ] Using a strong, random SECRET_KEY
- [ ] Tested admin login with new credentials

### Content
- [ ] Added initial portfolio projects
- [ ] Uploaded project images
- [ ] Added project descriptions and README files
- [ ] Verified all projects display correctly

### Maintenance
- [ ] Bookmarked PythonAnywhere dashboard
- [ ] Set reminder to reload app every 3 months (free tier)
- [ ] Created backup of database: `cp portfolio.db portfolio_backup.db`
- [ ] Documented how to update the site

## Common Issues Checklist

If site doesn't load:
- [ ] Check Error log in Web tab
- [ ] Check Server log in Web tab
- [ ] Verify username in WSGI file is correct
- [ ] Verify virtual environment path is correct
- [ ] Verify all dependencies installed: `pip list`

If admin login fails:
- [ ] Verify .env file exists
- [ ] Check environment variables in WSGI file
- [ ] Try setting variables manually in WSGI file
- [ ] Check Session secret key is set

If static files don't load:
- [ ] Verify static file mapping in Web tab
- [ ] Check paths are absolute, not relative
- [ ] Verify files exist: `ls -la static/`
- [ ] Check file permissions

## Success Criteria

✅ Your deployment is successful when:
- Site loads at `yourusername.pythonanywhere.com`
- All pages work (Home, About, Portfolio, Contact)
- CSS and images load correctly
- Can login to admin panel
- Can add/edit/delete projects from admin
- No errors in Error log

## Next Steps After Deployment

1. Add your portfolio projects through admin panel
2. Update personal information if needed
3. Share your site URL!
4. Consider upgrading to paid tier for custom domain

## Support Resources

- PythonAnywhere Help: https://help.pythonanywhere.com/
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- Flask Documentation: https://flask.palletsprojects.com/
- This project's DEPLOYMENT.md file

---

**Remember:** After making changes to your code, always:
1. Upload/push the changes
2. Click "Reload" in the Web tab
3. Test the changes on your live site
