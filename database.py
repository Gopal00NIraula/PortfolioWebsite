import sqlite3
import json
from datetime import datetime

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect('portfolio.db')
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

def delete_project(project_id):
    """Delete a project"""
    conn = get_db_connection()
    conn.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    add_sample_projects()
