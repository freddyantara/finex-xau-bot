# 🤖 PANDUAN SETUP BOT TRADING XAU/USD - BAHASA INDONESIA

## 📋 Ringkasan Bot

**Bot:** Finex XAU/USD Scalping Trading Bot  
**Strategy:** EMA Crossover + RSI Filter + MACD Confirmation  
**Pair:** XAU/USD (Gold)  
**Account:** Finex Demo (60677667)  
**Lot Size:** 0.01 per trade  
**Target Win Rate:** 80%+ confidence per signal  
**Features:** Trailing Stop, Risk Management, Auto-Logging  

---

## ✅ SYARAT SEBELUM SETUP

1. ✅ Akun Finex sudah dibuat (Demo: 60677667)
2. ✅ MT5 sudah terinstall di komputer
3. ✅ Sudah login MT5 dengan akun Finex
4. ✅ Python 3.8+ sudah terinstall
5. ✅ Replit account aktif (username: Freddyhafanis)

---

## 🚀 STEP 1: SETUP PYTHON DI REPLIT

### A. Buka Replit
1. Buka https://replit.com
2. Login dengan akun kamu (Freddyhafanis)
3. Klik **"+ Create"** → **"New Repl"**
4. Pilih bahasa: **Python**
5. Nama project: `finex-xau-bot`
6. Klik **"Create Repl"**

### B. Upload File Bot

1. Di Replit, klik tombol **"Upload"** (atau drag-drop files)
2. Upload file:
   - `finex_xau_scalping_bot.py` (kode bot)
   - `requirements.txt` (library yang diperlukan)

### C. Install Dependencies

Di terminal Replit, ketik:
```bash
pip install -r requirements.txt
```

Tunggu sampai selesai (1-2 menit).

---

## 🔐 STEP 2: SETUP CREDENTIALS

### A. Edit File Bot dengan Credentials Kamu

1. Buka file `finex_xau_scalping_bot.py`
2. Scroll ke bawah, cari bagian ini:

```python
if __name__ == "__main__":
    bot = FinexScalpingBot()
    
    # EDIT THESE WITH YOUR CREDENTIALS
    LOGIN = 60677667  # Your Finex account number
    PASSWORD = "your_password_here"  # Your MT5 password
    SERVER = "Finex-Demo"  # Server name
```

### B. Isi Credentials Kamu

**Ganti ini:**
- `LOGIN = 60677667` → **Sudah benar** (nomor akun kamu)
- `PASSWORD = "your_password_here"` → **Ganti dengan password MT5 kamu**
- `SERVER = "Finex-Demo"` → **Cek di MT5 kamu**

**Cara cek server name di MT5:**
1. Buka MT5
2. Lihat di bagian atas jendela → tertulis nama server
3. Contoh: `Finex-Demo-Server` atau `Finex-Live-Server`
4. Copy-paste nama exact itu

### C. Save File

Klik **"Save"** atau Ctrl+S

---

## 📌 STEP 3: KONFIGURASI BOT (OPTIONAL)

Kalau kamu mau adjust parameter bot, edit bagian ini di file:

```python
class FinexScalpingBot:
    def __init__(self):
        self.symbol = "XAUUSD"  # Pair (jangan diubah)
        self.timeframe = mt5.TIMEFRAME_M5  # M5 = 5 menit (bisa pakai M15)
        self.lot_size = 0.01  # Lot size per trade
        
        # Strategy parameters
        self.ema_fast = 5  # EMA cepat
        self.ema_slow = 10  # EMA lambat
        self.rsi_period = 14  # RSI periode
        self.rsi_oversold = 30  # RSI oversold level
        self.rsi_overbought = 70  # RSI overbought level
        
        # Risk management
        self.stop_loss_pips = 75  # SL jarak (pips)
        self.take_profit_pips = 40  # TP jarak (pips)
        self.trailing_stop_pips = 20  # Trailing stop jarak
        self.max_daily_loss = 5  # Max rugi per hari (USD)
        self.min_win_probability = 0.80  # 80% confidence required
```

**Penjelasan:**
- `ema_fast` / `ema_slow`: Semakin kecil = semakin cepat sinyal (tapi lebih banyak false signal)
- `stop_loss_pips`: Semakin besar = lebih aman tapi profit lebih kecil
- `take_profit_pips`: Target profit per trade
- `trailing_stop_pips`: Jarak trailing stop untuk amankan profit
- `min_win_probability`: Jangan ubah (80% = best balance)

---

## ▶️ STEP 4: JALANKAN BOT DI REPLIT

### A. Pastikan MT5 Terbuka

**PENTING:** Bot ini connect ke MT5 kamu yang terbuka di komputer. Jadi:
1. ✅ Pastikan **MT5 sudah login** di akun Finex (60677667)
2. ✅ Pastikan **MT5 tetap terbuka** selama bot jalan
3. ✅ Jangan tutup MT5 (kalau tutup, bot berhenti)

### B. Run Bot di Replit

1. Di Replit terminal, ketik:
```bash
python finex_xau_scalping_bot.py
```

2. Tunggu sampai muncul:
```
==================================================
Finex XAU/USD Scalping Bot Started
==================================================
Symbol: XAUUSD
Timeframe: 5
Lot Size: 0.01
Min Win Probability: 80%
==================================================
```

3. Bot sekarang **jalan otomatis**! 🚀

---

## 📊 MONITORING BOT

### A. Lihat Logs di Replit

Setiap aksi bot ditulis di logs, contoh:

```
2026-10-15 06:45:23 - INFO - ✓ BUY Signal - Confidence: 85% | Ask: 2050.25
2026-10-15 06:46:15 - INFO - Position closed: Ticket 123456, PnL: $2.50
2026-10-15 06:47:00 - INFO - Trailing stop updated (BUY): New SL 2049.80
```

**Arti logs:**
- `✓ BUY/SELL Signal` = Order baru diplace
- `Position closed` = Trade selesai dengan profit/loss
- `Trailing stop updated` = Stop loss dinaikkan untuk amankan profit

### B. Lihat Trading di MT5

Bot membuat order langsung di akun kamu:
1. Buka MT5
2. Lihat tab **"Trade"** (positions aktif)
3. Lihat tab **"History"** (semua trades yang selesai)

---

## 🛑 STOP BOT

Untuk stop bot:
1. Di Replit terminal, tekan **Ctrl+C**
2. Bot akan berhenti setelah next check (max 5 detik)
3. Log akan tulis: `Bot stopped by user`

---

## 🔴 TROUBLESHOOT

### Problem 1: Connection Error
```
Error: Failed to connect: ...
```

**Solusi:**
1. ✅ Pastikan MT5 sudah login ke akun Finex (60677667)
2. ✅ Pastikan PASSWORD benar (case-sensitive!)
3. ✅ Pastikan SERVER name benar (cek di MT5)
4. ✅ Restart MT5 dan coba lagi

### Problem 2: No Data for XAUUSD
```
Error: No data for XAUUSD
```

**Solusi:**
1. ✅ Di MT5, pastikan **XAUUSD pair sudah di Market Watch**
2. ✅ Klik kanan pada pair → **"Add to favorites"**
3. ✅ Klik pada pair dan lihat candles (biar data load)

### Problem 3: Orders Tidak Placed

**Solusi:**
1. ✅ Pastikan akun demo punya **balance cukup** (min $10)
2. ✅ Pastikan **market sedang buka** (forex 24/5)
3. ✅ Cek di MT5 apakah ada error message
4. ✅ Cek logs untuk error detail

### Problem 4: Bot Jalan Tapi Tidak Ada Signal

**Artinya:** Strategi tidak match dengan market conditions saat ini.

**Solusi:**
1. Tunggu saja (market berubah)
2. Atau adjust parameter (ema_fast, rsi_period, etc)
3. Atau tunggu timeframe berbeda (coba M15 instead M5)

---

## 📈 STRATEGY EXPLANATION

### Entry Logic (Harus 3 Kondisi Align untuk SIGNAL):

**BUY Signal (80%+ confidence):**
1. ✅ EMA5 > EMA10 (trend bullish)
2. ✅ RSI < 50 (bukan overbought)
3. ✅ MACD > Signal Line (momentum up)

**SELL Signal (80%+ confidence):**
1. ✅ EMA5 < EMA10 (trend bearish)
2. ✅ RSI > 50 (bukan oversold)
3. ✅ MACD < Signal Line (momentum down)

### Risk Management:
- **Stop Loss:** 75 pips (auto close kalau loss)
- **Take Profit:** 40 pips (auto close kalau untung)
- **Trailing Stop:** +20 pips saat profit (amankan profit)
- **Max Daily Loss:** $5 (bot stop kalau rugi $5+)

---

## 💡 TIPS TRADING

1. **Backtest dulu:** Lihat trading bot beberapa hari di DEMO sebelum live
2. **Monitor awal:** Pantau logs 1 jam pertama untuk lihat sinyal
3. **Jangan di-tweak:** Kalau bot jalan baik, jangan ganti parameter
4. **Risk management:** Lot 0.01 = risiko minimal, bagus untuk testing
5. **Market hours:** Forex paling aktif saat US/Europe market jam (best untuk scalping)

---

## 🚀 NEXT STEPS

1. ✅ Setup Replit & upload files
2. ✅ Edit credentials (password & server)
3. ✅ Run bot: `python finex_xau_scalping_bot.py`
4. ✅ Monitor logs
5. ✅ Lihat trades di MT5
6. ✅ Tunggu 1-2 minggu hasil demo
7. ✅ Kalau bagus, lanjut live dengan real money

---

## 📞 SUPPORT

Kalau ada error atau pertanyaan:
1. Cek logs (scroll up di Replit)
2. Copy error message lengkap
3. Kirim error + screenshot ke saya
4. Saya bantu fix!

---

**Good luck! 🎯 Bot kamu siap trading!**

Last Updated: 2026-10-15  
Author: Mister (Your Trading Assistant)
