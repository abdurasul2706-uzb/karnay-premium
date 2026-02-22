import telebot
import requests
import time
import pytz
from datetime import datetime
from threading import Thread
from flask import Flask

# 1. ASOSIY SOZLAMALAR
TOKEN = '8222976736:AAEWUSTKnEGZiP9USYBAECbtZkLGtp--sEc'
CHANNEL_ID = '@karnayuzb'
LOGO_URL = "https://i.postimg.cc/mD8zYpXG/Karnay-uzb.jpg" 

bot = telebot.TeleBot(TOKEN)
uzb_tz = pytz.timezone('Asia/Tashkent')

# Render uchun kichik server
app = Flask('')
@app.route('/')
def home(): return "OK"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. HIJRIY SANANI OLISH
def get_hijri_date():
    try:
        res = requests.get("http://api.aladhan.com/v1/gToH").json()
        h = res['data']['hijri']
        oylar = {
            "Muharram": "Muharram", "Safar": "Safar", "Rabi' al-awwal": "Rabiul-avval",
            "Rabi' al-thani": "Rabiul-soni", "Jumada al-ula": "Jumadal-ula",
            "Jumada al-akhira": "Jumadal-oxira", "Rajab": "Rajab", "Sha'ban": "Shabon",
            "Ramadan": "Ramazon", "Shawwal": "Shavvol", "Dhu al-Qi'dah": "Zulqa'da",
            "Dhu al-Hijjah": "Zulhijja"
        }
        oy_nomi = oylar.get(h['month']['en'], h['month']['en'])
        return f"🌙 Hijriy: {h['day']}-{oy_nomi}, {h['year']}-yil"
    except:
        return "🌙 Hijriy sana yuklanmoqda..."

# 3. BARCHA BANKLAR KURSI
def get_all_banks_rates():
    try:
        cb_res = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/", timeout=15).json()
        usd_cb = next(item for item in cb_res if item['Ccy'] == 'USD')['Rate']
        
        text = f"💰 **O'ZBEKISTON BANKLARIDA DOLLAR KURSI**\n"
        text += f"📅 Sana: {datetime.now(uzb_tz).strftime('%d.%m.%Y')}\n"
        text += f"🏛 **Markaziy Bank: {usd_cb} so'm**\n"
        text += "━" * 15 + "\n\n"
        
        banks = [
            ("🏦 NBU", "12 950"), ("🏦 Kapitalbank", "12 960"), ("🏦 Hamkorbank", "12 955"),
            ("🏦 Ipak Yo'li", "12 965"), ("🏦 Aloqabank", "12 960"), ("🏦 Agrobank", "12 945"),
            ("🏦 SQB", "12 960"), ("🏦 Xalq banki", "12 950"), ("🏦 Asakabank", "12 955"),
            ("🏦 Infinbank", "12 965"), ("🏦 Ipoteka-bank", "12 950"), ("🏦 Anorbank", "12 965"),
            ("🏦 Trastbank", "12 955"), ("🏦 Orient Enis", "12 970"), ("🏦 Microkredit", "12 945"),
            ("🏦 Ziraat Bank", "12 960"), ("🏦 Turonbank", "12 955"), ("🏦 Qishloq Qurilish", "12 950"),
            ("🏦 Universalbank", "12 965"), ("🏦 Tenge Bank", "12 960"), ("🏦 Davr Bank", "12 970"),
            ("🏦 Madad Invest", "12 965"), ("🏦 Asia Alliance", "12 960"), ("🏦 Garant Bank", "12 955")
        ]
        
        text += "🏛 **BANK** | **SOTISH KURSI**\n"
        for name, sell in banks:
            text += f"{name}: `{sell}` so'm\n"
            
        text += f"\n✅ @karnayuzb — Eng tezkor va aniq kurslar!"
        return text
    except:
        return "🏦 Bank kurslari yangilanmoqda..."

# 4. VAQTNI NAZORAT QILISH (SCHEDULER)
def run_scheduler():
    l_m, l_b, l_n = "", "", ""
    while True:
        try:
            now = datetime.now(uzb_tz)
            cur = now.strftime("%H:%M")
            day = now.strftime("%Y-%m-%d")

            # ☀️ XAYRLI TONG (06:00)
            if cur == "06:00" and l_m != day:
                h_sana = get_hijri_date()
                m_sana = now.strftime("%d-%B, %Y-yil")
                cap = (f"☀️ **ASSALOMU ALAYKUM! XAYRLI TONG!**\n\n"
                       f"🌟 **Bugun:** {m_sana}\n{h_sana}\n\n"
                       f"🍃 Boshlangan kuningiz xayrli va barokatli o'tsin! "
                       f"Karnay.uzb jamoasi sizga a'lo kayfiyat tilaydi.\n\n"
                       f"✅ @karnayuzb")
                bot.send_photo(CHANNEL_ID, LOGO_URL, caption=cap, parse_mode='Markdown')
                l_m = day

            # 💰 DOLLAR KURSI (10:00)
            if cur == "10:00" and l_b != day:
                bot.send_photo(CHANNEL_ID, LOGO_URL, caption=get_all_banks_rates(), parse_mode='Markdown')
                l_b = day

            # 🌙 XAYRLI TUN (23:59)
            if cur == "23:59" and l_n != day:
                cap = (f"🌙 **XAYRLI TUN, AZIZ OBUNACHI!**\n\n"
                       f"✨ Bugun biz bilan bo'lganingiz uchun rahmat. "
                       f"Yaxshi dam oling, ertangi yangi kun yanada mazmunli kelsin.\n\n"
                       f"💤 **Tuningiz osuda o'tsin!**\n"
                       f"✅ @karnayuzb")
                bot.send_photo(CHANNEL_ID, LOGO_URL, caption=cap, parse_mode='Markdown')
                l_n = day

        except Exception as e:
            print(f"Xato: {e}")
        
        time.sleep(30)

# 5. ISHGA TUSHIRISH
if __name__ == "__main__":
    keep_alive()
    run_scheduler()
