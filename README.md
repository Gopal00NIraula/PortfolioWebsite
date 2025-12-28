# Portfolio Website - Flask Application

A dynamic portfolio website built with Flask, showcasing projects across multiple categories including Python, Web Development, Java, C++, Android, Unity, Blender, and UX/UI Design.

## Features

- **Dynamic Content**: Flask-powered backend with Jinja2 templating
- **Responsive Design**: Modern, clean UI with smooth animations
- **Portfolio Categories**: Organized project showcase by technology
- **Contact Form**: Interactive contact form with validation
- **Particle Effects**: Engaging background animations on homepage
- **Social Integration**: Links to social media profiles

## Tech Stack

- **Backend**: Flask 3.0.0
- **Frontend**: HTML5, CSS3, JavaScript
- **Templating**: Jinja2
- **Effects**: Particles.js

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PortfolioWebsite
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

```
PortfolioWebsite/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Homepage
│   ├── about.html         # About page
│   ├── portfolio.html     # Portfolio listing
│   ├── contacts.html      # Contact page
│   └── portfolio/         # Category-specific pages
├── static/                # Static assets
│   ├── css/              # Stylesheets
│   ├── scripts/          # JavaScript files
│   ├── images/           # Images and icons
│   └── portfolio/        # Portfolio project pages
└── README.md             # This file
```

## Configuration

Edit `app.py` to customize:
- **PERSONAL_INFO**: Your personal details, bio, and social links
- **PORTFOLIO_CATEGORIES**: Project categories and descriptions
- **SECRET_KEY**: Change to a secure random key for production

## Development

The application runs in debug mode by default. For production:

1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

## Features to Add

- Database integration for projects
- Admin panel for content management
- Blog section
- Email functionality for contact form
- Project filtering and search
- Analytics integration

## Author

**Gopal Niraula** (Zenos)
- Computer Science Student at Youngstown State University
- Passionate about data analytics and problem-solving

## License

This project is open source and available for personal and educational use.
