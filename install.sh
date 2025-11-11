cat > install.sh << 'EOF'
#!/bin/bash
echo "[INSTALL] Mengunduh toolsbreaker.py..."
curl -L https://raw.githubusercontent.com/MrFoock12/toolsbreaker/main/toolsbreaker.py > toolsbreaker.py

echo "[INSTALL] Mengunduh requirements.txt..."
curl -L https://raw.githubusercontent.com/MrFoock12/toolsbreaker/main/requirements.txt > requirements.txt

echo "[INSTALL] Install paket..."
pip install -r requirements.txt

echo "[INSTALL] Setup storage..."
termux-setup-storage

echo "[SUCCESS] Install selesai! Jalankan: cd ~/toolsbreaker && python toolsbreaker.py"
EOF

chmod +x install.sh
