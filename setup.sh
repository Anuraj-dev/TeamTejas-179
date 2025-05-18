#!/bin/bash

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "========================================"
echo "EcoFinds Application Setup"
echo "========================================"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please install python3-venv package."
        echo "For Fedora/RHEL: sudo dnf install python3-venv"
        echo "For Ubuntu/Debian: sudo apt install python3-venv"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install PostgreSQL development libraries if needed
echo "Checking for PostgreSQL development libraries..."
if ! command -v pg_config &> /dev/null; then
    echo "PostgreSQL development libraries not found."
    echo "You have two options:"
    echo "1. Install PostgreSQL development libraries (recommended for production)"
    echo "   For Fedora/RHEL: sudo dnf install postgresql-devel"
    echo "   For Ubuntu/Debian: sudo apt install libpq-dev"
    echo "2. Use SQLite for development (no additional installation required)"
    
    read -p "Would you like to continue with SQLite for now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Setting up with SQLite database..."
        # Modify requirements.txt to remove psycopg2-binary
        sed -i.bak '/psycopg2-binary/d' requirements.txt
        echo "# Using SQLite instead of PostgreSQL" >> requirements.txt
    else
        echo "Please install PostgreSQL development libraries and run this script again."
        exit 1
    fi
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Please check the error message above."
    exit 1
fi

# Set up environment file
if [ ! -f ".env" ]; then
    echo "Setting up environment variables..."
    bash setup_env.sh
fi

# Set Flask app and environment
export FLASK_APP=run.py
export FLASK_ENV=development

# Initialize database
echo "Setting up database..."
bash db_setup.sh

echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: python run.py"
echo "The application will be available at http://127.0.0.1:5000"
echo "========================================" 