#!/bin/bash

# Check if .env file already exists
if [ -f .env ]; then
    read -p ".env file already exists. Do you want to overwrite it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup aborted."
        exit 1
    fi
fi

# Create .env file with default values
cat > .env << EOF
# Flask configuration
FLASK_APP=run.py
FLASK_CONFIG=development
FLASK_DEBUG=1
SECRET_KEY=$(openssl rand -hex 24)

# Database URIs
DEV_DATABASE_URI=sqlite:///dev.db
TEST_DATABASE_URI=sqlite:///test.db
DATABASE_URI=postgresql://username:password@localhost/ecofinds

# Email configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password
MAIL_DEFAULT_SENDER=noreply@ecofinds.com

# Security settings
REQUIRE_HTTPS=false
EOF

echo ".env file created successfully with default values."
echo "Please edit the file to set your specific configuration values." 