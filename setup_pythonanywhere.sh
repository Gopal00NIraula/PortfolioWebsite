#!/bin/bash
# Quick setup script for PythonAnywhere
# Run this in the PythonAnywhere Bash console after uploading your code

echo "======================================"
echo "Portfolio Website - PythonAnywhere Setup"
echo "======================================"
echo ""

# Get current directory
PROJECT_DIR=$(pwd)
echo "Project directory: $PROJECT_DIR"
echo ""

# Step 1: Create virtual environment
echo "Step 1: Creating virtual environment..."
mkvirtualenv --python=/usr/bin/python3.10 portfolio-env
echo "✓ Virtual environment created"
echo ""

# Step 2: Install dependencies
echo "Step 2: Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Step 3: Set up environment file
echo "Step 3: Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file from example"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and change:"
    echo "   - SECRET_KEY"
    echo "   - ADMIN_USERNAME"
    echo "   - ADMIN_PASSWORD"
    echo ""
else
    echo "✓ .env file already exists"
fi
echo ""

# Step 4: Initialize database
echo "Step 4: Initializing database..."
python -c "from database import init_db; init_db()"
echo "✓ Database initialized"
echo ""

echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Configure Web app in PythonAnywhere dashboard"
echo "3. Set WSGI file path"
echo "4. Set virtual environment path: $HOME/.virtualenvs/portfolio-env"
echo "5. Configure static files mapping"
echo "6. Reload your web app"
echo ""
echo "See DEPLOYMENT.md for detailed instructions"
echo ""
