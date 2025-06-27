#!/bin/bash

# 🔥 GOD-TIER PhantomAutoBuyBot - Automated Setup Script
# =====================================================

set -e  # Exit on any error

echo "🔥 Setting up GOD-TIER PhantomAutoBuyBot..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Check if Python 3.11+ is installed
print_info "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Python $PYTHON_VERSION found"
    
    # Check if version is 3.11+
    if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 11) else 1)'; then
        print_status "Python version is compatible"
    else
        print_error "Python 3.11+ required, found $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Check if pip is installed
print_info "Checking pip..."
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
else
    print_error "pip3 not found. Please install pip"
    exit 1
fi

# Create virtual environment (optional but recommended)
print_info "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip
print_status "pip upgraded"

# Install requirements
print_info "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_status "Dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Install Playwright browsers
print_info "Installing Playwright browsers..."
playwright install chromium
print_status "Playwright browsers installed"

# Create necessary directories
print_info "Creating directories..."
mkdir -p logs
mkdir -p screenshots
mkdir -p data
mkdir -p backups
print_status "Directories created"

# Copy configuration template
print_info "Setting up configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.template" ]; then
        cp .env.template .env
        print_status "Configuration template copied to .env"
        print_warning "Please edit .env file with your actual API keys and settings"
    else
        print_error ".env.template not found"
        exit 1
    fi
else
    print_warning ".env file already exists, skipping template copy"
fi

# Set permissions
print_info "Setting permissions..."
chmod +x setup.sh
chmod +x health_check.py 2>/dev/null || true
chmod +x deploy.sh 2>/dev/null || true
print_status "Permissions set"

# Create .gitignore if it doesn't exist
print_info "Setting up .gitignore..."
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# Screenshots
screenshots/
*.png
*.jpg
*.jpeg

# Data files
data/
backups/
vector_db.json
*.db
*.sqlite

# OS
.DS_Store
Thumbs.db

# Temporary files
tmp/
temp/
*.tmp
EOF
    print_status ".gitignore created"
else
    print_warning ".gitignore already exists"
fi

# Run health check
print_info "Running health check..."
if python3 health_check.py 2>/dev/null; then
    print_status "Health check passed"
else
    print_warning "Health check failed - some components may need configuration"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo "================================"
echo ""
print_info "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - GOLOGIN_API_KEY"
echo "   - TELEGRAM_TOKEN"
echo "   - TELEGRAM_CHAT_ID"
echo ""
echo "2. Test the configuration:"
echo "   python3 test_telegram.py"
echo ""
echo "3. Run the bot:"
echo "   python3 phantom_autobuy/main.py"
echo ""
print_warning "Remember: Never commit .env file to version control!"
echo ""
print_status "GOD-TIER PhantomAutoBuyBot is ready! 🔥"