# ⚡ QUICK START - BOT TRADING FINEX XAU/USD

## 🎯 3 LANGKAH CEPAT

### 1️⃣ SETUP REPLIT (5 MENIT)
```
1. Buka https://replit.com
2. Login: Freddyhafanis
3. Create Repl → Python → finex-xau-bot
4. Upload: finex_xau_scalping_bot.py + requirements.txt
5. Terminal: pip install -r requirements.txt
```

### 2️⃣ EDIT CREDENTIALS (2 MENIT)
Di file `finex_xau_scalping_bot.py`, cari bagian bawah:

**Ganti ini:**
```python
LOGIN = 60677667  # ← Sudah benar
PASSWORD = "your_password_here"  # ← GANTI DENGAN PASSWORD MT5 KAMU
SERVER = "Finex-Demo"  # ← Cek nama server di MT5
```

**Save file** (Ctrl+S)

### 3️⃣ RUN BOT (1 MENIT)
```bash
python finex_xau_scalping_bot.py
```

✅ BOT JALAN! Lihat logs di Replit.

---

## 📌 PENTING!

✅ **MT5 HARUS TERBUKA** saat bot jalan  
✅ **Login ke akun Finex** di MT5 (60677667)  
✅ **XAUUSD pair di Market Watch** di MT5  

---

## 📊 STRATEGY

**Entry:** Hanya saat EMA + RSI + MACD SEMUA ALIGN (80%+ confidence)  
**Exit:** Opposite signal atau TP/SL hit  
**Trailing Stop:** Amankan profit otomatis  

---

## 🛑 STOP BOT

**Terminal:** Ctrl+C

---

**Baca PANDUAN_SETUP_BOT_BAHASA_INDONESIA.md untuk detail lengkap!**
