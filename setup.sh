#!/bin/bash

# Update and upgrade packages
echo "Updating and upgrading packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install PostgreSQL and development headers
echo "Installing PostgreSQL and development headers..."
sudo apt-get install -y postgresql libpq-dev

# Additional steps can be added below...

echo "Installation steps completed!"
