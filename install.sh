#!/bin/bash

# ============================================
# TOOLS BREAKER v.0 - INSTALLATION SCRIPT
# Author: MrFoock12
# GitHub: https://github.com/MrFoock12/toolsbreaker
# ============================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════╗"
echo "║         TOOLS BREAKER v1.0 INSTALL       ║"
echo "║            by MrFoock12                  ║"
echo "╚══════════════════════════════════════════╝${NC}"
echo ""

# Check if running on Termux
if [ ! -d "/data/data/com.termux/files/usr" ]; then
    echo -e "${RED}[ERROR] This script is for Termux only!${NC}"
    exit 1
fi

# Function to print status
print_status() {
    echo -e "${CYAN}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Update and upgrade
print_status "Updating packages..."
pkg update -y && pkg upgrade -y
if [ $? -eq 0 ]; then
    print_success "Packages updated successfully"
else
    print_error "Failed to update packages"
    exit 1
fi

# Install basic dependencies
print_status "Installing basic dependencies..."
pkg install -y python openssh termux-api git wget curl nano vim
if [ $? -eq 0 ]; then
    print_success "Basic dependencies installed"
else
    print_error "Failed to install basic dependencies"
    exit 1
fi

# Setup storage
print_status "Setting up storage..."
termux-setup-storage
sleep 2

# Create toolsbreaker directory
print_status "Creating toolsbreaker directory..."
mkdir -p ~/toolsbreaker
cd ~/toolsbreaker || exit

# Download main script
print_status "Downloading main script..."
if command -v wget &> /dev/null; then
    wget -q https://raw.githubusercontent.com/MrFoock12/toolsbreaker/main/tools_breaker.py -O tools_breaker.py
elif command -v curl &> /dev/null; then
    curl -s -L https://raw.githubusercontent.com/MrFoock12/toolsbreaker/main/tools_breaker.py -o tools_breaker.py
else
    print_error "Neither wget nor curl found. Installing curl..."
    pkg install -y curl
    curl -s -L https://raw.githubusercontent.com/MrFoock12/toolsbreaker/main/tools_breaker.py -o tools_breaker.py
fi

if [ -f "tools_breaker.py" ]; then
    print_success "Main script downloaded"
else
    print_error "Failed to download main script"
    exit 1
fi

# Download requirements.txt
print_status "Downloading requirements..."
if command -v wget &> /dev/null; then
    wget -q https://raw.githubusercontent.com/MrFoock12/toolsbreaker/main/requirements.txt -O requirements.txt
elif command -v curl &> /dev/null; then
    curl -s -L https://raw.githubusercontent.com/MrFoock12/toolsbreaker/main/requirements.txt -o requirements.txt
fi

# Download ua.txt (User-Agents)
print_status "Downloading User-Agents file..."
cat > ua.txt << 'EOF'
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36
EOF
print_success "User-Agents file created"

# Install Python dependencies
print_status "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    # Install default dependencies if requirements.txt not found
    print_warning "requirements.txt not found, installing default dependencies..."
    pip install --upgrade pip
    pip install requests colorama termcolor cryptography pillow selenium qrcode[pil]
fi

# Additional dependencies for Termux
print_status "Installing Termux-specific dependencies..."
pkg install -y proot-distro
pkg install -y libxml2 libxslt libjpeg-turbo libpng
pip install lxml

# Make script executable
print_status "Making script executable..."
chmod +x tools_breaker.py

# Create alias for easy access
print_status "Creating alias..."
echo "alias toolsbreaker='cd ~/toolsbreaker && python tools_breaker.py'" >> ~/.bashrc
echo "alias tb='cd ~/toolsbreaker && python tools_breaker.py'" >> ~/.bashrc

# Create launcher script
print_status "Creating launcher script..."
cat > ~/../usr/bin/toolsbreaker << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/toolsbreaker
python tools_breaker.py
EOF
chmod +x ~/../usr/bin/toolsbreaker

# Create update script
print_status "Creating update script..."
cat > update_toolsbreaker.sh << 'EOF'
#!/bin/bash
cd ~/toolsbreaker
echo "Updating Tools Breaker..."
if command -v wget &> /dev/null; then
    wget -q https://raw.githubusercontent.com/MrFoock12/toolsbreaker/main/tools_breaker.py -O tools_breaker_new.py
elif command -v curl &> /dev/null; then
    curl -s -L https://raw.githubusercontent.com/MrFoock12/toolsbreaker/main/tools_breaker.py -o tools_breaker_new.py
fi

if [ -f "tools_breaker_new.py" ]; then
    mv tools_breaker.py tools_breaker_backup.py
    mv tools_breaker_new.py tools_breaker.py
    chmod +x tools_breaker.py
    echo "Update successful! Backup saved as tools_breaker_backup.py"
else
    echo "Update failed!"
fi
EOF
chmod +x update_toolsbreaker.sh

# Create README
print_status "Creating README..."
cat > README.txt << 'EOF'
╔══════════════════════════════════════════╗
║         TOOLS BREAKER v1.0               ║
║            by MrFoock12                  ║
╚══════════════════════════════════════════╝

📌 INSTALLATION COMPLETE!

📍 Location: ~/toolsbreaker/
📁 Files:
  - tools_breaker.py    (Main script)
  - requirements.txt    (Python dependencies)
  - ua.txt             (User-Agents)
  - update_toolsbreaker.sh (Update script)

🚀 HOW TO USE:
1. Run: toolsbreaker
   or: tb
   or: cd ~/toolsbreaker && python tools_breaker.py

2. First time will create tokens.json automatically

3. Login with token from @MrFoock12

🔄 UPDATE:
Run: ./update_toolsbreaker.sh

📞 SUPPORT:
Telegram: @MrFoock12
WhatsApp: +62895622994489

⚠️ DISCLAIMER:
For educational purposes only.
Use at your own risk.
EOF

# Final message
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           INSTALLATION COMPLETE!         ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📦 Installation Summary:${NC}"
echo -e "  ${GREEN}✓${NC} Tools installed in: ~/toolsbreaker/"
echo -e "  ${GREEN}✓${NC} Main script: tools_breaker.py"
echo -e "  ${GREEN}✓${NC} Aliases created: 'toolsbreaker' and 'tb'"
echo -e "  ${GREEN}✓${NC} System command: toolsbreaker"
echo -e "  ${GREEN}✓${NC} Update script: update_toolsbreaker.sh"
echo ""
echo -e "${YELLOW}🚀 Quick Start:${NC}"
echo -e "  1. Restart Termux or run: ${CYAN}source ~/.bashrc${NC}"
echo -e "  2. Run: ${CYAN}toolsbreaker${NC}"
echo -e "  3. Or: ${CYAN}cd ~/toolsbreaker && python tools_breaker.py${NC}"
echo ""
echo -e "${YELLOW}📞 Support:${NC}"
echo -e "  Telegram: ${CYAN}@MrFoock12${NC}"
echo -e "  WhatsApp: ${CYAN}+62895622994489${NC}"
echo ""
echo -e "${RED}⚠️  Disclaimer:${NC}"
echo -e "  For educational purposes only."
echo -e "  Use responsibly and legally."
echo ""

# Restart bash to load aliases
exec bash
