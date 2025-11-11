cat > README.md << 'EOF'
# TOOLS BREAKER v1.0

## CARA INSTALL (TERMUX)
```bash
pkg update -y && pkg upgrade -y && pkg install python openssh termux-api -y && termux-setup-storage && mkdir -p ~/toolsbreaker && cd ~/toolsbreaker && curl -L https://raw.githubusercontent.com/MrFoock12/toolsbreaker/main/install.sh | bash
