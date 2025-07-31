#!/bin/bash

# ACS-Chat Universal Deployment Script
# For complete deployment on any new EC2 instance

set -e  # Exit on any error

echo "🚀 ACS-Chat Universal Deployment Script Starting..."

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   log_error "Do not run this script as root user"
   exit 1
fi

# Get domain name from user
echo ""
log_info "Please enter your domain name (e.g., example.com):"
read -r DOMAIN_NAME

if [ -z "$DOMAIN_NAME" ]; then
    log_error "Domain name is required"
    exit 1
fi

# Get email for SSL certificate
echo ""
log_info "Please enter your email for SSL certificate:"
read -r EMAIL

if [ -z "$EMAIL" ]; then
    log_error "Email is required for SSL certificate"
    exit 1
fi

# Check for existing .env file
if [ -f "be/.env" ]; then
    log_info "Detected existing .env file, will use existing configuration"
    USE_EXISTING_ENV=true
else
    log_info "No .env file detected, will create from template"
    USE_EXISTING_ENV=false
fi

# 1. System update
log_info "Updating system packages..."
sudo yum update -y

# 2. Install Docker
log_info "Installing Docker..."
if ! command -v docker &> /dev/null; then
    sudo yum install -y docker
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -a -G docker ec2-user
    log_info "Docker installation completed"
else
    log_info "Docker already installed"
fi

# 3. Install Docker Compose
log_info "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo ln -sf /usr/local/bin/docker-compose /usr/local/bin/docker-compose
    log_info "Docker Compose installation completed"
else
    log_info "Docker Compose already installed"
fi

# 4. Install Git
log_info "Installing Git..."
sudo yum install -y git

# 5. Install Certbot
log_info "Installing Certbot..."
sudo yum install -y certbot

# 6. Clone project (if not exists)
if [ ! -d "/home/ec2-user/ACS-Chat" ]; then
    log_info "Cloning project code..."
    cd /home/ec2-user
    git clone https://github.com/DarcyHU999/ACS-Chat.git
    cd ACS-Chat
    log_info "Project code cloned successfully"
else
    cd /home/ec2-user/ACS-Chat
    log_info "Project directory exists, updating code..."
    git pull origin main
    log_info "Project code updated successfully"
fi

# 7. Configure environment variables
if [ "$USE_EXISTING_ENV" = false ]; then
    log_info "Creating environment file from template..."
    cp be/env.example be/.env
    log_warn "⚠️  IMPORTANT: Please edit be/.env and configure your API keys:"
    echo "   - OPENAI_API_KEY: Your OpenAI API key"
    echo "   - QDRANT_URL: Your Qdrant Cloud URL"
    echo "   - QDRANT_API_KEY: Your Qdrant Cloud API key"
    echo ""
    echo "Press Enter to continue after editing the .env file..."
    read -r
    log_info "Environment configuration completed"
else
    log_info "Using existing environment configuration"
fi

# 8. Set secure file permissions
log_info "Setting secure file permissions..."
chmod 600 be/.env

# 9. Apply SSL certificate
log_info "Applying SSL certificate for domain: $DOMAIN_NAME"
if [ ! -d "/etc/letsencrypt/live/$DOMAIN_NAME" ]; then
    # Stop services that might use port 80
    sudo pkill -f nginx || true
    sudo pkill -f certbot || true
    
    # Apply certificate
    sudo certbot certonly --standalone -d "$DOMAIN_NAME" --non-interactive --agree-tos --email "$EMAIL"
    log_info "SSL certificate applied successfully"
else
    log_info "SSL certificate already exists"
fi

# 10. Setup certificate auto-renewal
log_info "Setting up certificate auto-renewal..."
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
log_info "Certificate auto-renewal configured"

# 11. Clean existing services
log_info "Cleaning existing services..."
docker compose down 2>/dev/null || true

# 12. Build services
log_info "Building Docker services..."
docker compose build

# 13. Start application
log_info "Starting application..."
docker compose up -d

# Wait for services to start
log_info "Waiting for services to start..."
sleep 30

# 14. Check service status
log_info "Checking service status..."
docker compose ps

# 15. Verify application
log_info "Verifying application is running..."
if curl -s -I "https://$DOMAIN_NAME" | grep -q "200\|301\|302"; then
    log_info "✅ Application is running successfully!"
else
    log_warn "⚠️  Application may need more time to start, please check later"
fi

# 16. Display system information
log_info "System resource usage:"
echo "Memory usage:"
free -h
echo ""
echo "Disk usage:"
df -h
echo ""
echo "Docker container status:"
docker compose ps

# 17. Display access information
echo ""
log_info "🎉 Deployment completed!"
echo "📱 Application access URLs:"
echo "   - Frontend: https://$DOMAIN_NAME"
echo "   - API: https://$DOMAIN_NAME/api/v1/"
echo "   - Health check: https://$DOMAIN_NAME/api/health"
echo ""
echo "🔧 Common commands:"
echo "   - Check status: docker compose ps"
echo "   - View logs: docker compose logs -f"
echo "   - Restart services: docker compose restart"
echo "   - Update code: git pull origin main"
echo ""
echo "📊 Monitoring commands:"
echo "   - Memory usage: free -h"
echo "   - Disk usage: df -h"
echo "   - Container resources: docker stats"
echo ""
echo "🔒 Security reminders:"
echo "   - Ensure AWS Security Groups only allow ports 80 and 443"
echo "   - Regularly monitor OpenAI API usage"
echo "   - Regularly update system and Docker images" 