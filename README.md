# Rate Limiter Service

Bu proje, web uygulamalarında aşırı istek (ör. brute force) durumlarını önlemek amacıyla geliştirilmiş IP bazlı bir rate limiter servisidir. Servis, belirli bir zaman aralığında aynı istemciden  gelen istek sayısını sınırlandırarak sistemi korur.

---

## Proje Özeti

- FastAPI tabanlı web uygulaması
- IP bazlı rate limiting
- Belirli süre içinde maksimum istek sınırı
- Limit aşımında HTTP 429 (Too Many Requests)
- Birim testler ve uçtan uca senaryo içerir

---

## Kullanılan Teknolojiler

- Python 3
- FastAPI
- Uvicorn
- Pytest
- FastAPI TestClient

---

## Uygulamayı Çalıştırma

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
---

# Tarayıcıdan test etmek için:
- http://127.0.0.1:8000/limited-endpoint

---

# Testler
- Birim Testler
Rate limiting mekanizması, pytest kullanılarak yazılmış en az 5 adet birim test ile doğrulanmıştır.

- Uçtan Uca Senaryo (Otomatik)
 FastAPI TestClient kullanılarak, gerçek HTTP istekleri üzerinden limit altı ve limit aşımı durumları test edilmiştir.
- python -m pytest

---

# Uçtan Uca Saldırı Senaryosu (Demo)
-demo/brute_force_scenario.py dosyası ile brute force saldırısını temsil eden bir istemci senaryosu çalıştırılabilir. 2 farklı terminal gereklidir.
1) uvicorn app.main:app --reload
2) python demo/brute_force_scenario.py


