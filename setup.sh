#!/bin/bash

# Update and upgrade packages
echo "Updating and upgrading packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install PostgreSQL and development headers
echo "Installing PostgreSQL and development headers..."
sudo apt-get install -y postgresql libpq-dev

sudo service postgresql start
# Extract database credentials from .env
postgre_user=$(grep POSTGRE_USER .env | cut -d '=' -f2)
postgre_pass=$(grep POSTGRE_PASS .env | cut -d '=' -f2)
postgre_db=$(grep POSTGRE_DB .env | cut -d '=' -f2)

# Configure PostgreSQL and create user and database
echo "Setting up PostgreSQL user and database..."
sudo -u postgres psql << EOF
CREATE USER $postgre_user WITH PASSWORD '$postgre_pass';
CREATE DATABASE $postgre_db;
GRANT ALL PRIVILEGES ON DATABASE $postgre_db TO $postgre_user;
\q
EOF

# Run your Python scripts
echo "Running Python scripts..."
python3 firebase_worker.py &
python3 main.py

echo "Installation and execution steps completed!"
