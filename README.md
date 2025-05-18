# EcoFinds

A sustainable marketplace Flask application that connects eco-conscious buyers with sellers of environmentally friendly products.

## Features

- User authentication and authorization
- Product listings with categories and search functionality
- Secure payment processing
- User profiles and ratings
- Administrative dashboard
- Responsive design for mobile and desktop

## System Requirements

- Python 3.8 or higher
- PostgreSQL (optional, SQLite can be used for development)
- pip (Python package installer)

## Installation & Setup

### Quick Setup (Recommended)

We've created a setup script that handles all the necessary installation steps:

```bash
# Clone the repository
git clone <repository-url>
cd EcoFinds

# Make the setup script executable if it's not already
chmod +x setup.sh

# Run the setup script
./setup.sh
```

The setup script will:
1. Create a Python virtual environment
2. Check for PostgreSQL development libraries
3. Install all required dependencies
4. Set up environment variables
5. Initialize the database

### Manual Setup

If you prefer to set up manually, follow these steps:

1. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

Note: If you encounter issues with `psycopg2-binary` installation:
- For Fedora/RHEL: `sudo dnf install postgresql-devel`
- For Ubuntu/Debian: `sudo apt install libpq-dev`
- Or remove `psycopg2-binary` from requirements.txt to use SQLite

3. **Set up environment variables**

```bash
./setup_env.sh
```

This creates a `.env` file with default settings. Edit this file to update configurations like database URI, email settings, etc.

4. **Initialize the database**

```bash
./db_setup.sh
```

## Running the Application

After completing the setup:

```bash
# Activate the virtual environment (if not already activated)
source venv/bin/activate

# Run the application
python run.py
```

The application will be available at http://127.0.0.1:5000

## Development

### Project Structure

```
EcoFinds/
├── app/                  # Application package
│   ├── __init__.py       # App factory
│   ├── models/           # Database models
│   ├── routes/           # Application routes
│   ├── templates/        # Jinja2 templates
│   ├── static/           # Static files (CSS, JS, images)
│   └── utils/            # Utility functions
├── migrations/           # Database migrations
├── tests/                # Test suite
├── .env                  # Environment variables (created by setup_env.sh)
├── requirements.txt      # Dependencies
├── run.py                # Application entry point
└── setup.sh              # Setup script
```

### Running Tests

```bash
pytest tests/
```

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running if you're using it
- Check your database URI in the `.env` file
- For SQLite, ensure the application has write permissions in the directory

### Dependency Issues

- Ensure you have activated the virtual environment
- Try upgrading pip: `pip install --upgrade pip`
- Install system dependencies for cryptography: `sudo apt install build-essential libssl-dev libffi-dev python3-dev` (on Debian/Ubuntu)

## License

[MIT License](LICENSE)

## Contact

For questions or support, please contact [maintainer email]
