"""
Database migration script to add icon_image column to categories table
Run this once to update your existing database
"""
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'portfolio.db')

def migrate():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(categories)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'icon_image' not in columns:
        print("Adding icon_image column to categories table...")
        cursor.execute("ALTER TABLE categories ADD COLUMN icon_image TEXT")
        conn.commit()
        print("✓ Migration completed successfully!")
    else:
        print("icon_image column already exists. No migration needed.")
    
    conn.close()

if __name__ == '__main__':
    migrate()
