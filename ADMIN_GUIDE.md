# Admin Panel Guide

## 🚀 Quick Start

Your portfolio website now has a powerful admin panel for managing projects!

### Access the Admin Panel

1. **URL**: http://localhost:5000/admin/login
2. **Default Credentials**:
   - Username: `admin`
   - Password: `password123`

⚠️ **IMPORTANT**: Change these credentials in `admin.py` before deploying!

## 📋 Features

### 1. **Dashboard** (`/admin/dashboard`)
- View all projects in a table
- See project thumbnails, categories, and status
- Quick edit/delete actions
- Total project count

### 2. **Add Project** (`/admin/project/new`)
Upload new projects with:
- **Title**: Project name
- **Category**: Python, Web, Java, C++, Android, Unity, Blender, or UX/UI
- **Description**: What the project does
- **Technologies**: Languages/frameworks used
- **Image**: Upload project screenshot (PNG, JPG, GIF, WEBP up to 16MB)
- **Project URL**: Live demo link
- **GitHub URL**: Repository link
- **Featured**: ⭐ Mark as featured project

### 3. **Edit Project** (`/admin/project/edit/<id>`)
- Update any project information
- Replace project image
- Change featured status

### 4. **Delete Project**
- Remove projects with confirmation dialog

## 🎯 Workflow

### Adding a New Project

1. Go to http://localhost:5000/admin/login
2. Login with credentials
3. Click "**+ Add New Project**"
4. Fill in the form:
   ```
   Title: My Awesome Project
   Category: python
   Description: A cool Python app that...
   Technologies: Python, Flask, SQLite
   Image: [Upload screenshot.png]
   Project URL: https://myproject.com
   GitHub URL: https://github.com/username/project
   ✓ Featured (optional)
   ```
5. Click "**Add Project**"
6. Project appears on your portfolio immediately!

### Managing Existing Projects

- **View**: Projects display on portfolio category pages automatically
- **Edit**: Click "Edit" button in dashboard
- **Delete**: Click "Delete" (with confirmation)
- **Feature**: Check "Featured" to highlight important projects

## 📁 File Storage

- **Database**: `portfolio.db` (SQLite)
- **Images**: `static/images/projects/`
- Uploaded images are automatically saved and linked

## 🔐 Security

### Change Default Password

Edit `admin.py`:

```python
ADMIN_USERNAME = 'your_username'
ADMIN_PASSWORD = 'your_secure_password'
```

### For Production

Consider:
- Using environment variables for credentials
- Implementing password hashing
- Adding user management
- Using PostgreSQL instead of SQLite

## 🎨 Customization

### Admin Panel Colors

Edit `static/css/admin.css`:
```css
/* Change primary color from orange */
.btn-primary {
    background: #your-color;
}
```

### Categories

Add/modify categories in `app.py`:
```python
PORTFOLIO_CATEGORIES = [
    {'id': 'newcat', 'name': 'New Category', 'icon': '🎯', 'color': '#color'},
]
```

## 📊 Database Schema

### Projects Table
```sql
- id (INTEGER PRIMARY KEY)
- title (TEXT)
- category (TEXT)
- description (TEXT)
- technologies (TEXT)
- image_url (TEXT)
- project_url (TEXT)
- github_url (TEXT)
- featured (BOOLEAN)
- created_at (TIMESTAMP)
```

## 🛠️ Troubleshooting

**Can't login?**
- Check credentials in `admin.py`
- Make sure session secret key is set in `app.py`

**Images not uploading?**
- Check `static/images/projects/` folder exists
- Verify file size < 16MB
- Ensure file format is supported

**Projects not showing?**
- Check database has data: `python database.py`
- Verify category matches in database

**Database errors?**
- Delete `portfolio.db` and run `python database.py` again

## 💡 Tips

1. **Featured Projects**: Use sparingly for best work
2. **Good Images**: Use high-quality screenshots (1200x800px recommended)
3. **Descriptions**: Keep concise but informative (2-3 sentences)
4. **Technologies**: List main tech stack, comma-separated
5. **URLs**: Add live demos when possible for better showcase

## 🚀 Next Steps

- Add more projects through admin panel
- Customize categories for your needs
- Consider adding project tags/filters
- Implement search functionality
- Add analytics to track views

---

**Need Help?** 
- Check the Flask documentation: https://flask.palletsprojects.com/
- Database queries in `database.py`
- Routes in `app.py` and `admin.py`
