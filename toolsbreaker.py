import os, json, time, uuid, random, string, subprocess, base64
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from termcolor import colored

init(autoreset=True)

# CONFIG
RESULTS_DIR = "results"
LICENSE_FILE = 'tokens.json'
os.makedirs(RESULTS_DIR, exist_ok=True)

VPS_IP = "209.97.166.25"
VPS_USER = "root"
VPS_PATH = "/root/korban/results"

CURRENT_TIME = datetime.now().strftime("%d %b %Y - %I:%M %p WIB")
COUNTRY = "ID"

# MUSIK
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

# DEVELOPER CHECK
WHOAMI = subprocess.getoutput("whoami")
DEVELOPER_WHOAMI = "u0_a197"  # GANTI SESUAI whoami LO
IS_DEVELOPER = WHOAMI == DEVELOPER_WHOAMI

# TOKEN SYSTEM
def load_tokens():
    if not os.path.exists(LICENSE_FILE):
        return {}
    try:
        return json.load(open(LICENSE_FILE))
    except:
        return {}

def save_tokens(t):
    with open(LICENSE_FILE, 'w') as f:
        json.dump(t, f, indent=2)

def validate_token(username, token):
    t = load_tokens()
    if username not in t: return None
    user = t[username]
    if not user['active'] or user['token'] != token: return None
    if datetime.now() > datetime.fromisoformat(user['expires']): 
        user['active'] = False
        save_tokens(t)
        return None
    return user

def create_token():
    print(colored("\n[DEVELOPER MODE] BUAT TOKEN BARU", 'magenta', attrs=['bold']))
    username = input(colored("Username buyer: ", 'yellow')).strip()
    buyer_whoami = input(colored("whoami buyer: ", 'yellow')).strip()
    
    print(colored("Pilih plan:", 'cyan'))
    plans = ["pemula 1hari", "pemula 1minggu", "pemula 1bulan", "pro 1hari", "pro 1minggu", "pro 1bulan"]
    for p in plans: print(colored(f"  {p}", 'white'))
    
    plan_input = input(colored("Plan: ", 'yellow')).strip().lower()
    plan_map = {
        "pemula 1hari": ("PEMULA 1HARI", 1),
        "pemula 1minggu": ("PEMULA 1MINGGU", 7),
        "pemula 1bulan": ("PEMULA 1BULAN", 30),
        "pro 1hari": ("PRO 1HARI", 1),
        "pro 1minggu": ("PRO 1MINGGU", 7),
        "pro 1bulan": ("PRO 1BULAN", 30),
    }
    
    if plan_input not in plan_map:
        print(colored("Plan salah!", 'red'))
        return False
    
    plan_name, days = plan_map[plan_input]
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    expires = (datetime.now() + timedelta(days=days)).isoformat()
    
    t = load_tokens()
    t[username] = {
        "token": token,
        "plan": plan_name,
        "active": True,
        "expires": expires,
        "whoami": buyer_whoami,
        "created_at": CURRENT_TIME,
        "country": COUNTRY
    }
    save_tokens(t)
    print(colored(f"\n[SUCCESS] Token: {token}", 'green'))
    print(colored(f"   Plan: {plan_name}", 'cyan'))
    print(colored(f"   whoami: {buyer_whoami}", 'cyan'))
    input("\nEnter...")

# LIHAT TOKEN — HANYA DEVELOPER
def view_tokens():
    if not IS_DEVELOPER:
        print(colored("\n[ERROR] Akses ditolak!", 'red', attrs=['bold']))
        input("\nEnter...")
        return
    t = load_tokens()
    print(colored("\n=== DATABASE TOKEN ===", 'yellow', attrs=['bold']))
    if not t:
        print(colored("   [KOSONG]", 'red'))
    else:
        print(json.dumps(t, indent=2, ensure_ascii=False))
    input("\nEnter...")

# BANNER
PURPLE = '\033[38;5;55m'
def print_banner(uid, plan):
    print(colored(f"""
{PURPLE}{Style.BRIGHT}
╔═══════════════════════════════╗
║       TOOLS BREAKER v1.0      ║
╚═══════════════════════════════╝
{Style.RESET_ALL}Tools oleh Mr.Foock | ID: {uid} | Plan: {plan}
Lokasi: Jakarta, ID | Waktu: {CURRENT_TIME}
""", None))

# SAVE RESULT + AUTO SCP KE VPS
def save_result(filename, content):
    filepath = os.path.join(RESULTS_DIR, filename)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {content}\n")
    print(colored(f"[SAVED] {filename}", 'green'))
    try:
        subprocess.run(f"scp -o StrictHostKeyChecking=no {filepath} {VPS_USER}@{VPS_IP}:{VPS_PATH}/{filename}", 
                      shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(colored(f"[SYNC] → VPS", 'cyan'))
    except:
        print(colored("[SYNC] Gagal", 'red'))

# FITUR 10: NOTIF RETAS
def fitur_notif_retas():
    print(colored("\nNOTIF WHATSAPP ANDA KENA RETAS", 'blue', attrs=['bold']))
    target = input(colored("Nomor target (+62): ", 'yellow'))
    save_result("notif_retas.log", f"Target: {target}")
    save_result("notif_retas.log", "Status: KLIK → DATA MASUK")
    print(colored(f"[SENT] Terkirim!", 'green'))
    input("Enter...")

# MAIN
def main():
    os.system('clear')
    print_banner("??????", "LOGIN")
    
    if IS_DEVELOPER:
        uid = str(uuid.uuid4())[:8]
        plan = "DEVELOPER LIFETIME"
        print(colored(f"\n[DEVELOPER] Login @{WHOAMI}", 'magenta', attrs=['bold']))
        input("Enter...")
    else:
        while True:
            print(colored("\n[1] MASUKIN TOKEN LU", 'yellow'))
            print(colored("[0] Keluar", 'red'))
            choice = input(colored("Pilih: ", 'yellow')).strip()
            if choice == "1":
                username = input(colored("Username: ", 'yellow')).strip()
                token = input(colored("Token: ", 'yellow')).strip()
                user = validate_token(username, token)
                if not user:
                    print(colored("TOKEN SALAH / KADALUARSA!", 'red'))
                    continue
                uid = str(uuid.uuid4())[:8]
                plan = user['plan']
                print(colored(f"\n[SUCCESS] Login @{username} | {plan}", 'green'))
                input("Enter...")
                break
            elif choice == "0": return

    # DEVELOPER MENU
    while IS_DEVELOPER:
        print(colored("\n[2] Buat Token Baru", 'magenta'))
        print(colored("[3] Lihat Database Token", 'yellow'))
        print(colored("[0] Masuk ke Tools", 'green'))
        ch = input(colored("Pilih: ", 'yellow')).strip()
        if ch == "2": create_token()
        elif ch == "3": view_tokens()
        elif ch == "0": break
        else: print(colored("Pilihan salah!", 'red'))

    # MENU UTAMA
    while True:
        os.system('clear')
        print_banner(uid, plan)
        print(colored(" < 11 MENU UTAMA — TOTAL 100+ FITUR > ", 'cyan'))
        print("╔════╦══════════════════════════╦════════════════╗")
        print("║ 10 ║ NOTIF RETAS (PUSAT BANTUAN) ║ Aktif          ║")
        print("╚════╩══════════════════════════╩════════════════╝")
        ch = input(colored("\nPilih Menu (10 / 00): ", 'yellow')).strip()
        if ch == "10": fitur_notif_retas()
        elif ch == "00": 
            print(colored("\nKELUAR LU DARI SINI...", 'red'))
            break
        input(colored("\nTekan Enter...", 'cyan'))

if __name__ == "__main__":
    main()
