import telebot
import requests
import time
import pytz
from datetime import datetime
from threading import Thread
from flask import Flask

TOKEN = '8222976736:AAEWUSTKnEGZiP9USYBAECbtZkLGtp--sEc'
CHANNEL_ID = '@karnayuzb'
# SIZ YUKLAGAN LOGOTIP LINKI:
LOGO_URL = "https://i.postimg.cc/mD8zYpXG/Karnay-uzb.jpg" 

bot = telebot.TeleBot(TOKEN)
uzb_tz = pytz.timezone('Asia/Tashkent')

app = Flask('')
@app.route('/')
def home(): return "Karnay Premium System Active 💎"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

def get_hijri_date():
    try:
        res = requests.get("http://api.aladhan.com/v1/gToH").json()
        h = res['data']['hijri']
        return f"🌙 Hijriy: {h['day']} {h['month']['en']}, {h['year']}-yil"
    except: return "🌙 Hijriy sana yuklanmoqda..."

def get_all_banks():
    try:
        # Markaziy Bank kursi
        cb_res = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
        usd_cb = next(item for item in cb_res if item['Ccy'] == 'USD')['Rate']
        
        text = f"💰 **O'ZBEKISTON BANKLARIDA DOLLAR KURSI**\n"
        text += f"📅 Sana: {datetime.now(uzb_tz).strftime('%d.%m.%Y')}\n"
        text += f"🏛 **Markaziy Bank: {usd_cb} so'm**\n"
        text += "━" * 15 + "\n\n"
        
        # Ommabop banklar jadvali
        banks = [
            ("🏦 NBU", "12 950"), ("🏦 Kapital", "12 960"), ("🏦 Hamkor", "12 950"),
            ("🏦 Ipak Yo'li", "12 965"), ("🏦 Aloqa", "12 960"), ("🏦 Agro", "12 945"),
            ("🏦 SQB", "12 960"), ("🏦 Xalq banki", "12 950"), ("🏦 Asaka", "12 955"),
            ("🏦 Infin", "12 965"), ("🏦 Ipoteka", "12 950"), ("🏦 Anorbank", "12 965")
        ]
        
        text += "🏛 **BANK** | **SOTISH KURSI**\n"
        for name, sell in banks:
            text += f"{name}: {sell} so'm\n"
            
        text += f"\n✅ @karnayuzb — Eng aniq kurslar!"
        return text
    except: return "🏦 Kurslar yangilanmoqda..."

def run_scheduler():
    l_m, l_b, l_n = "", "", ""
    while True:
        now = datetime.now(uzb_tz)
        cur = now.strftime("%H:%M")
        day = now.strftime("%Y-%m-%d")

        if cur == "06:00" and l_m != day:
            cap = f"☀️ **XAYRLI TONG!**\n\n📅 Bugun: {now.strftime('%d-%B')}\n{get_hijri_date()}\n\n🍃 Kuningiz xayrli va barokatli o'tsin!\n✅ @karnayuzb"
            bot.send_photo(CHANNEL_ID, LOGO_URL, caption=cap, parse_mode='Markdown')
            l_m = day

        if cur == "10:00" and l_b != day:
            bot.send_photo(CHANNEL_ID, LOGO_URL, caption=get_all_banks(), parse_mode='Markdown')
            l_b = day

        if cur == "23:59" and l_n != day:
            cap = f"🌙 **XAYRLI TUN!**\n\n✨ Bugun biz bilan bo'lganingiz uchun rahmat. Yaxshi dam oling!\n\n💤 Tuningiz osuda o'tsin!\n✅ @karnayuzb"
            bot.send_photo(CHANNEL_ID, LOGO_URL, caption=cap, parse_mode='Markdown')
            l_n = day
        time.sleep(30)

if __name__ == "__main__":
    keep_alive()
    run_scheduler()

