import logging
import random
import time
import sqlite3
from contextlib import closing

import pandas as pd
import requests

TARGET_URL = (
    "https://quotes.toscrape.com/api/quotes?page={page}"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.google.com",
}

TIMEOUT = 10
MIN_WAIT = 2
MAX_WAIT = 4
MAX_CONSECUTIVE_ERRORS = 3
CSV_FILE_PATH = "sozler.csv"
EXCEL_FILE_PATH = "sozler.xlsx"
DB_FILE_PATH = "sozler.db"
TABLE_NAME = "sozler_tablosu"

# log kurulumu 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
    handlers= [
        logging.FileHandler("quetos.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

def fetch_data(max_page=10):
    """ Belirtilen sayfa sayısı kadar veri çeker"""
    
    all_quotes = []
    consecutive_errors = 0
    
    for page in range(1, max_page + 1):
        url = TARGET_URL.format(page=page)
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            response.encoding = "utf-8"
            
            if response.status_code != 200:
                log.error("Sayfa %s HATA (kod: %s)", page, response.status_code)
                consecutive_errors += 1
                if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                    log.error("Ust uste %s hata, islem durduruldu", consecutive_errors)
                    break
                time.sleep(random.uniform(MIN_WAIT, MAX_WAIT))
                continue
            
            data = response.json()
            
            # Eksik veya null alanlara karsi güvenli erisim
            quotes = (data.get("quotes") or [])
            
            # Bos sayfa, sozlerin bittigi anlamına gelir
            if not quotes:
                 log.info("Sayfa %s bos geldi, sozler bitti.", page)
                 break
             
            for q in quotes:
                author = q.get("author") or {}
                name = author.get("name") or ""
                text = q.get("text") or ""
                
                all_quotes.append(
                    {
                        "soz": text,
                        "yazar": name,  
                    }
                )
                
            consecutive_errors = 0
            log.info("Sayfa %s basariyla cekildi (%s soz).", page, len(quotes))
            time.sleep(random.uniform(MIN_WAIT, MAX_WAIT))
        except (requests.exceptions.RequestException, ValueError) as e:
            consecutive_errors += 1
            log.error("Sayfa %s hata: %s", page, e)
            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                log.error("Ust uste %s hata, islem durduruldu.", consecutive_errors)
                break
            time.sleep(random.uniform(MIN_WAIT, MAX_WAIT))
    
    return all_quotes

def export_data(all_quotes):
    """ Toplanan verileri CSV, Excel ve SQLite formatlarinda kaydeder."""
    if not all_quotes:
        log.warning("Kaydedilecek veri bulunamadi!")
        return
    
    df = pd.DataFrame(all_quotes)
    
    first = len(df)
    df = df.drop_duplicates()
    log.info("%s tekrar eden soz silindi.", first - len(df))
    
    df.to_csv(CSV_FILE_PATH, index=False, encoding="utf-8-sig")
    log.info("Veriler '%s' dosyasina yazildi.", CSV_FILE_PATH)
    
    try:
        df.to_excel(EXCEL_FILE_PATH, index=False)
        log.info("Veriler '%s' dosyasina yazildi.", EXCEL_FILE_PATH)
    except (ImportError, OSError) as e:
        log.error("Excel kayit hatasi: %s", e)
        
    try:
        with closing(sqlite3.connect(DB_FILE_PATH)) as connecting:
            df.to_sql(TABLE_NAME, connecting, if_exists="replace", index=False)
        log.info("Veriler '%s' veri tabanina islendi.", DB_FILE_PATH)
    except sqlite3.Error as e:
        log.error("Veritabani kayit hatasi: %s", e)
        

# --- Ana Calistirma Blogu ---
if __name__ == "__main__":
    log.info("Web scraping operasyonu baslatiliyor...")
    quote_list = fetch_data(10)
    export_data(quote_list)
    log.info("Tum islemler tamamlandi")   