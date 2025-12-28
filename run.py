# Flask Portfolio Website
# Run this file to start the development server
# Use: python run.py

from app import app

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════╗
    ║   Portfolio Website - Flask Application      ║
    ║   Created by: Gopal Niraula (Zenos)          ║
    ║                                               ║
    ║   Server running at: http://localhost:5000   ║
    ║   Press CTRL+C to quit                        ║
    ╚═══════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)
