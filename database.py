import sqlite3
import json
import os
from datetime import datetime

# Get the absolute path to the database
# This ensures the database works both locally and on PythonAnywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'portfolio.db')

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with tables"""
    conn = get_db_connection()
    
    # Create projects table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            full_description TEXT,
            technologies TEXT,
            image_url TEXT,
            screenshots TEXT,
            project_url TEXT,
            github_url TEXT,
            featured BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create categories table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            icon TEXT,
            icon_image TEXT,
            color TEXT,
            is_listed BOOLEAN DEFAULT 1,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Migration: Add icon_image column if it doesn't exist
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(categories)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'icon_image' not in columns:
        conn.execute("ALTER TABLE categories ADD COLUMN icon_image TEXT")
    
    # Create admin users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def add_sample_projects():
    """Add some sample projects to get started"""
    conn = get_db_connection()
    
    sample_projects = [
        {
            'title': 'Snake Game',
            'category': 'python',
            'description': 'Classic snake game built with Python and Pygame',
            'technologies': 'Python, Pygame',
            'image_url': 'SnakeGame.png',
            'featured': 1
        },
        {
            'title': 'Guess Who Game',
            'category': 'uxui',
            'description': 'UX/UI design for a modern Guess Who game',
            'technologies': 'Figma, Adobe XD',
            'image_url': 'GuessWho.png',
            'featured': 1
        }
    ]
    
    for project in sample_projects:
        conn.execute('''
            INSERT INTO projects (title, category, description, technologies, image_url, featured)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (project['title'], project['category'], project['description'], 
              project['technologies'], project['image_url'], project['featured']))
    
    conn.commit()
    conn.close()
    print("Sample projects added!")

def get_all_projects():
    """Get all projects"""
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects ORDER BY created_at DESC').fetchall()
    conn.close()
    return projects

def get_projects_by_category(category):
    """Get projects by category"""
    conn = get_db_connection()
    projects = conn.execute(
        'SELECT * FROM projects WHERE category = ? ORDER BY created_at DESC',
        (category,)
    ).fetchall()
    conn.close()
    return projects

def get_project_by_id(project_id):
    """Get a single project by ID"""
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE id = ?', (project_id,)).fetchone()
    conn.close()
    return project

def add_project(title, category, description, technologies, image_url, project_url='', github_url='', featured=0, full_description='', screenshots=''):
    """Add a new project"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO projects (title, category, description, full_description, technologies, image_url, screenshots, project_url, github_url, featured)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, category, description, full_description, technologies, image_url, screenshots, project_url, github_url, featured))
    conn.commit()
    conn.close()

def update_project(project_id, title, category, description, technologies, image_url, project_url='', github_url='', featured=0, full_description='', screenshots=''):
    """Update an existing project"""
    conn = get_db_connection()
    conn.execute('''
        UPDATE projects 
        SET title=?, category=?, description=?, full_description=?, technologies=?, image_url=?, screenshots=?, project_url=?, github_url=?, featured=?
        WHERE id=?
    ''', (title, category, description, full_description, technologies, image_url, screenshots, project_url, github_url, featured, project_id))
    conn.commit()
    conn.close()

def get_all_categories():
    """Get all categories ordered by sort_order"""
    conn = get_db_connection()
    categories = conn.execute(
        'SELECT * FROM categories ORDER BY sort_order ASC, name ASC'
    ).fetchall()
    conn.close()
    return categories

def get_listed_categories():
    """Get only listed/visible categories"""
    conn = get_db_connection()
    categories = conn.execute(
        'SELECT * FROM categories WHERE is_listed = 1 ORDER BY sort_order ASC, name ASC'
    ).fetchall()
    conn.close()
    return categories

def get_category_by_id(category_id):
    """Get a single category by ID"""
    conn = get_db_connection()
    category = conn.execute(
        'SELECT * FROM categories WHERE id = ?',
        (category_id,)
    ).fetchone()
    conn.close()
    return category

def toggle_category_visibility(category_id):
    """Toggle category visibility (list/unlist)"""
    conn = get_db_connection()
    # Get current state
    category = conn.execute(
        'SELECT is_listed FROM categories WHERE id = ?',
        (category_id,)
    ).fetchone()
    
    if category:
        new_state = 0 if category['is_listed'] else 1
        conn.execute(
            'UPDATE categories SET is_listed = ? WHERE id = ?',
            (new_state, category_id)
        )
        conn.commit()
    conn.close()
    return new_state if category else None

def init_default_categories():
    """Initialize default categories if they don't exist"""
    default_categories = [
        {'id': 'python', 'name': 'Python Projects', 'icon': '🐍', 'color': '#3776ab', 'sort_order': 1},
        {'id': 'web', 'name': 'Web Development', 'icon': '🌐', 'color': '#e34f26', 'sort_order': 2},
        {'id': 'java', 'name': 'Java Projects', 'icon': '☕', 'color': '#007396', 'sort_order': 3},
        {'id': 'cpp', 'name': 'C++ Projects', 'icon': '⚡', 'color': '#00599c', 'sort_order': 4},
        {'id': 'android', 'name': 'Android Apps', 'icon': '📱', 'color': '#3ddc84', 'sort_order': 5},
        {'id': 'unity', 'name': 'Unity Games', 'icon': '🎮', 'color': '#000000', 'sort_order': 6},
        {'id': 'blender', 'name': '3D Modeling', 'icon': '🎨', 'color': '#f5792a', 'sort_order': 7},
        {'id': 'uxui', 'name': 'UX/UI Design', 'icon': '✨', 'color': '#ff6b6b', 'sort_order': 8}
    ]
    
    conn = get_db_connection()
    for cat in default_categories:
        # Check if category exists
        existing = conn.execute(
            'SELECT id FROM categories WHERE id = ?',
            (cat['id'],)
        ).fetchone()
        
        if not existing:
            conn.execute(
                'INSERT INTO categories (id, name, icon, color, is_listed, sort_order) VALUES (?, ?, ?, ?, 1, ?)',
                (cat['id'], cat['name'], cat['icon'], cat['color'], cat['sort_order'])
            )
    
    conn.commit()
    conn.close()

def add_category(category_id, name, icon, color, sort_order=999, icon_image=None):
    """Add a new category"""
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO categories (id, name, icon, icon_image, color, is_listed, sort_order) VALUES (?, ?, ?, ?, ?, 1, ?)',
            (category_id, name, icon, icon_image, color, sort_order)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return False

def update_category(category_id, name, icon, color, icon_image=None):
    """Update an existing category"""
    conn = get_db_connection()
    try:
        if icon_image is not None:
            # Update with new image
            conn.execute(
                'UPDATE categories SET name = ?, icon = ?, icon_image = ?, color = ? WHERE id = ?',
                (name, icon, icon_image, color, category_id)
            )
        else:
            # Update without changing image
            conn.execute(
                'UPDATE categories SET name = ?, icon = ?, color = ? WHERE id = ?',
                (name, icon, color, category_id)
            )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return False

def delete_category(category_id):
    """Delete a category and update projects using it to NULL"""
    conn = get_db_connection()
    # First check if any projects use this category
    projects_count = conn.execute(
        'SELECT COUNT(*) as count FROM projects WHERE category = ?',
        (category_id,)
    ).fetchone()['count']
    
    # Update projects to have NULL category
    conn.execute(
        'UPDATE projects SET category = NULL WHERE category = ?',
        (category_id,)
    )
    
    # Delete the category
    conn.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()
    return projects_count

def delete_project(project_id):
    """Delete a project"""
    conn = get_db_connection()
    conn.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    add_sample_projects()
