Çalıştırma Komutları


Linux

1-git clone https://github.com/muhsinvoid/Brute-Force
2-cd Brute-Force
3-ls
4-python brute_force.py


cmd

1-zip dosyası olarak indirdikten sonra masaüstüne klasöre ayıklayın
2-cd ( dosya yolu )
3-python brute_force.py


Çalıştırmadan Önce
Python Kodundaki TARGET_USERNAME = "hedef_kullanıcı_adı" Kısmına Hedefinizin Kullanıcı Adını Yazın
TARGET_URL = "https://instagram.com/login" Hedef Sitenin Login Sayfasının Linkini Koyun

try:
u_elem = driver.find_element(By.NAME, "username")
except:
try:
u_elem = driver.find_element(By.NAME, "email")
except: ------------------------------------------------- ( Bu Kısıma Hedef Sitenizdeki Login Ve Pass Kutularının "name" değeri neyse onları yazın user , username , pass , password gibi )
