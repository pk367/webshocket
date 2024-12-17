#!/bin/bash

# Exit on error
set -e

# Configuration
APP_NAME="tvdata-api"
APP_DIR="/var/www/$APP_NAME"
PYTHON_VERSION="3.12"
USERNAME="your_username"  # Replace with your Hostinger username

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Starting deployment of $APP_NAME...${NC}"

# Create application directory if it doesn't exist
echo -e "${GREEN}Creating application directory...${NC}"
sudo mkdir -p $APP_DIR
sudo chown -R $USERNAME:$USERNAME $APP_DIR

# Create and activate virtual environment
echo -e "${GREEN}Setting up Python virtual environment...${NC}"
python$PYTHON_VERSION -m venv $APP_DIR/venv
source $APP_DIR/venv/bin/activate

# Install system dependencies
echo -e "${GREEN}Installing system dependencies...${NC}"
sudo apt-get update
sudo apt-get install -y python$PYTHON_VERSION python$PYTHON_VERSION-venv nginx supervisor

# Copy application files
echo -e "${GREEN}Copying application files...${NC}"
cp -r ./* $APP_DIR/
cp .env $APP_DIR/

# Install Python dependencies
echo -e "${GREEN}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r $APP_DIR/requirements.txt

# Set up Nginx
echo -e "${GREEN}Configuring Nginx...${NC}"
sudo cp tvdata.conf /etc/nginx/sites-available/tvdata
sudo ln -sf /etc/nginx/sites-available/tvdata /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Set up systemd service
echo -e "${GREEN}Configuring systemd service...${NC}"
sudo cp tvdata.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tvdata
sudo systemctl restart tvdata

# Set up SSL (if domain is configured)
echo -e "${GREEN}Setting up SSL...${NC}"
read -p "Do you want to set up SSL with Let's Encrypt? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo apt-get install -y certbot python3-certbot-nginx
    read -p "Enter your domain name: " domain_name
    sudo certbot --nginx -d $domain_name
fi

# Final steps
echo -e "${GREEN}Deployment completed!${NC}"
echo -e "${GREEN}Checking service status...${NC}"
sudo systemctl status tvdata

# Print URLs
echo -e "${GREEN}Your API is now available at:${NC}"
echo "http://your_domain.com (HTTP)"
echo "https://your_domain.com (HTTPS, if SSL was configured)"
echo -e "${GREEN}API Documentation available at:${NC}"
echo "http://your_domain.com/docs"
echo "http://your_domain.com/redoc" 