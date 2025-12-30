"""
Database initialization script
Run this to set up the database with categories
"""
from database import init_db, init_default_categories

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Adding default categories...")
    init_default_categories()
    print("Database setup complete!")
    print("\nDefault categories added:")
    print("- Python Projects")
    print("- Web Development")
    print("- Java Projects")
    print("- C++ Projects")
    print("- Android Apps")
    print("- Unity Games")
    print("- 3D Modeling")
    print("- UX/UI Design")
    print("\nAll categories are listed by default.")
    print("Go to /admin/categories to manage visibility.")
