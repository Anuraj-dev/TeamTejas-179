#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set Flask app and environment
export FLASK_APP=run.py
export FLASK_ENV=development

# Initialize database directory
mkdir -p instance

# Initialize the database
echo "Initializing database..."
flask init-db

# Initialize migration repository if it doesn't exist
if [ ! -d "migrations/versions" ]; then
    echo "Initializing migration repository..."
    flask db init
fi

# Create initial migration
echo "Creating initial migration..."
flask db migrate -m "Initial migration"

# Apply migration
echo "Applying migration..."
flask db upgrade

echo "Database setup complete!" 