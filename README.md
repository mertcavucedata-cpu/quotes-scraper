# Quotes Scraper (JSON API)

[quotes.toscrape.com](https://quotes.toscrape.com) sitesinin JSON API'sinden sözleri ve yazarlarını çeken, temizleyen ve üç farklı formatta kaydeden Python scraper'ı.

> Bu site web scraping pratiği için hazırlanmış bir eğitim sitesidir, veri çekmek serbesttir.

## Özellikler

- Çok sayfalı veri çekme (sayfa sayısı ayarlanabilir)
- İstekler arasında rastgele bekleme (siteyi yormamak için)
- Zaman aşımı (timeout) ve hata yönetimi: art arda 3 hata olursa program güvenle durur
- Eksik veya boş (null) alanlara karşı korumalı veri okuma
- Tekrar eden kayıtların temizlenmesi
- Çıktı: **CSV**, **Excel (.xlsx)** ve **SQLite** veritabanı
- Tüm işlemler `quetos.log` dosyasına zaman damgasıyla kaydedilir

## Kullanılan Teknolojiler

Python 3, `requests`, `pandas`, `openpyxl`, `sqlite3`, `logging`

## Kurulum ve Çalıştırma

```bash
pip install requests pandas openpyxl
python queto_main.py
```

## Çıktı Dosyaları

| Dosya | Açıklama |
|---|---|
| `sozler.csv` | Tüm sözler (UTF-8) |
| `sozler.xlsx` | Excel formatında aynı veri |
| `sozler.db` | SQLite veritabanı (`sozler_tablosu`) |
| `quetos.log` | Çalışma kaydı |

Sütunlar: `soz`, `yazar`

### Örnek Çıktı
soz,yazar
“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”,Albert Einstein
"“It is our choices, Harry, that show what we truly are, far more than our abilities.”",J.K. Rowling
“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”,Albert Einstein
"“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”",Jane Austen
"“Imperfection is beauty, madness is genius and it's better to be absolutely ridiculous than absolutely boring.”",Marilyn Monroe

## Ayarlar

Tüm ayarlar dosyanın en üstündeki sabitlerde durur: sayfa adresi, bekleme süreleri, timeout, dosya adları.

## Notlar

Bu proje, JSON API tabanlı scraping, hata yönetimi ve veri dışa aktarma pratiği için hazırlanmıştır.
