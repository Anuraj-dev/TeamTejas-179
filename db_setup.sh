#!/bin/bash

# Exit on error
set -e

# Check if we are in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment not activated. Activating now..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "Error: Virtual environment not found. Please run setup.sh first."
        exit 1
    fi
fi

# Install dependencies if not already installed
if ! pip freeze | grep -q "Flask=="; then
echo "Installing dependencies..."
pip install -r requirements.txt
fi

# Set Flask app and environment
export FLASK_APP=run.py
export FLASK_ENV=development

# Initialize database directory
mkdir -p instance

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Environment file not found. Creating it now..."
    bash setup_env.sh
fi

# Set database URI based on whether psycopg2 is installed
if pip freeze | grep -q "psycopg2-binary"; then
    echo "Using PostgreSQL database..."
    # Check if database exists and is accessible
    source .env
    DB_NAME=$(echo $DATABASE_URI | awk -F'/' '{print $NF}')
    DB_USER=$(echo $DATABASE_URI | awk -F'[:@]' '{print $4}')
    
    if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ]; then
        echo "Error: Invalid DATABASE_URI in .env file."
        echo "Please edit .env file and set proper PostgreSQL connection details."
        exit 1
    fi
    
    echo "Note: Ensure PostgreSQL is running and the database exists."
    read -p "Continue with database setup? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Database setup aborted."
        exit 1
    fi
else
    echo "Using SQLite database..."
fi

# Initialize the database
echo "Initializing database..."
flask init-db || {
    echo "Error initializing database. Check your database connection."
    exit 1
}

# Initialize migration repository if it doesn't exist
if [ ! -d "migrations" ]; then
    echo "Initializing migration repository..."
    flask db init || {
        echo "Error initializing migrations. Check your database connection."
        exit 1
    }
elif [ ! -d "migrations/versions" ]; then
    echo "Initializing migration repository..."
    flask db init || {
        echo "Error initializing migrations. Check your database connection."
        exit 1
    }
fi

# Create initial migration
echo "Creating initial migration..."
flask db migrate -m "Initial migration" || {
    echo "Error creating migration. Check your database models for errors."
    exit 1
}

# Apply migration
echo "Applying migration..."
flask db upgrade || {
    echo "Error applying migration. Check your database connection."
    exit 1
}

echo "Database setup complete!" 
echo "You can now run the application with 'python run.py'" 