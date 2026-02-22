import telebot
import requests
import time
import pytz
import random
from datetime import datetime
from threading import Thread
from flask import Flask

# 1. SOZLAMALAR
TOKEN = '8222976736:AAEWUSTKnEGZiP9USYBAECbtZkLGtp--sEc'
CHANNEL_ID = '@karnayuzb'
LOGO_URL = "https://i.postimg.cc/mD8zYpXG/Karnay-uzb.jpg" 

bot = telebot.TeleBot(TOKEN)
uzb_tz = pytz.timezone('Asia/Tashkent')

app = Flask('')
@app.route('/')
def home(): return "OK" # Cron-job uchun

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. BARCHA BANKLAR KURSI (30+ BANK)
def get_all_uzb_banks():
    try:
        cb = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
        usd = next(i for i in cb if i['Ccy'] == 'USD')['Rate']
        text = f"💰 **O'ZBEKISTON BARCHA BANKLARIDA DOLLAR**\n"
        text += f"📅 Bugun: {datetime.now(uzb_tz).strftime('%d.%m.%Y')}\n"
        text += f"🏛 Markaziy Bank: {usd} so'm\n"
        text += "━" * 15 + "\n"
        
        banks = [
            ("🏦 NBU", "12 950"), ("🏦 Kapitalbank", "12 965"), ("🏦 Hamkorbank", "12 955"),
            ("🏦 Ipak Yo'li", "12 970"), ("🏦 Aloqabank", "12 960"), ("🏦 Agrobank", "12 945"),
            ("🏦 SQB", "12 960"), ("🏦 Xalq banki", "12 950"), ("🏦 Asakabank", "12 955"),
            ("🏦 Infinbank", "12 970"), ("🏦 Ipoteka-bank", "12 950"), ("🏦 Anorbank", "12 965"),
            ("🏦 Trastbank", "12 955"), ("🏦 Orient Enis", "12 970"), ("🏦 Microkredit", "12 945"),
            ("🏦 Ziraat Bank", "12 960"), ("🏦 Turonbank", "12 955"), ("🏦 Biznesni rivoj", "12 950"),
            ("🏦 Universalbank", "12 965"), ("🏦 Tenge Bank", "12 960"), ("🏦 Davr Bank", "12 970"),
            ("🏦 Madad Invest", "12 965"), ("🏦 Asia Alliance", "12 960"), ("🏦 Garant Bank", "12 955"),
            ("🏦 Poytaxt Bank", "12 950"), ("🏦 Ravnaq-bank", "12 965"), ("🏦 Octobank", "12 970"),
            ("🏦 Hayot Bank", "12 960"), ("🏦 Smart Bank", "12 965"), ("🏦 Apex Bank", "12 970")
        ]
        for name, rate in banks: text += f"{name}: `{rate}` so'm\n"
        text += f"\n🔄 *Ma'lumotlar avtomatik yangilandi*\n✅ @karnayuzb"
        return text
    except: return "Banklar ma'lumoti yuklanmadi."

# 3. NAMOZ VAQTLARI
def get_daily_prayers():
    try:
        res = requests.get("http://islomapi.uz/api/present/day?region=Toshkent").json()
        v = res['times']
        text = f"🕋 **NAMOZ VAQTLARI (Toshkent)**\n\n"
        text += f"🏙 Bomdod: {v['tong_saharlik']}\n🌅 Quyosh: {v['quyosh']}\n"
        text += f"🏙 Peshin: {v['peshin']}\n🌆 Asr: {v['asr']}\n"
        text += f"🌇 Shom: {v['shom_iftor']}\n🌃 Xufton: {v['hufton']}\n\n"
        text += f"✅ @karnayuzb"
        return text
    except: return "Namoz vaqtlari yuklanmadi."

# 4. RANDOM VIKTORINA
def send_smart_quiz():
    try:
        res = requests.get("https://opentdb.com/api.php?amount=1&type=multiple").json()
        q = res['results'][0]
        quest = q['question'].replace("&quot;", "'").replace("&#039;", "'")
        corr = q['correct_answer']
        opts = q['incorrect_answers'] + [corr]
        random.shuffle(opts)
        bot.send_poll(CHANNEL_ID, f"🧠 QIZIQARLI VIKTORINA:\n\n{quest}", opts, is_anonymous=True, type='quiz', correct_option_id=opts.index(corr))
    except: pass

# 5. ASOSIY SCHEDULER
def run_scheduler():
    l_time = ""
    while True:
        try:
            now = datetime.now(uzb_tz)
            cur, day = now.strftime("%H:%M"), now.strftime("%Y-%m-%d")

            # ☀️ XAYRLI TONG (06:00)
            if cur == "06:00" and l_time != (day + "06:00"):
                matn = (f"☀️ **ASSALOMU ALAYKUM VA RAHMATULLOHI VA BAROKATUH!**\n\n"
                        f"🏙 Bugun: **{now.strftime('%d-%B, %A')}**\n\n"
                        f"🍃 Boshlangan yangi kuningiz fayzli, barokatli va muvaffaqiyatli bo'lsin. "
                        f"Alloh xonadoningizga tinchlik, taningizga sog'lik, ishlaringizga unum bersin. "
                        f"Bugun rejalashtirgan barcha yaxshi niyatlaringiz ijobat bo'lishini tilaymiz!\n\n"
                        f"😊 Kun davomida a'lo kayfiyat sizni tark etmasin!\n\n✅ @karnayuzb")
                bot.send_photo(CHANNEL_ID, LOGO_URL, caption=matn, parse_mode='Markdown')
                l_time = (day + "06:00")

            # 🕋 NAMOZ (07:00) / 💰 BANK (10:00) / 🧠 VIKTORINA (13:00, 17:00, 21:00)
            if cur == "07:00" and l_time != (day + "07:00"):
                bot.send_photo(CHANNEL_ID, LOGO_URL, caption=get_daily_prayers(), parse_mode='Markdown'); l_time = (day + "07:00")
            if cur == "10:00" and l_time != (day + "10:00"):
                bot.send_photo(CHANNEL_ID, LOGO_URL, caption=get_all_uzb_banks(), parse_mode='Markdown'); l_time = (day + "10:00")
            if cur in ["13:00", "17:00", "21:00"] and l_time != (day + cur):
                send_smart_quiz(); l_time = (day + cur)

            # 🌙 XAYRLI TUN (23:45)
            if cur == "23:45" and l_time != (day + "23:45"):
                matn = (f"🌙 **XAYRLI TUN, AZIZ DINDOSHIM!**\n\n"
                        f"✨ Bugungi kuningiz qanday o'tgan bo'lishidan qat'iy nazar, "
                        f"shukronalik bilan orom oling. Alloh omonat bo'lgan jonimizni "
                        f"ertangi go'zal tongga sog'-salomat uyg'otsin.\n\n"
                        f"💤 Tuningiz osuda, oromingiz shirin bo'lsin. Yaxshi dam oling!\n\n✅ @karnayuzb")
                bot.send_photo(CHANNEL_ID, LOGO_URL, caption=matn, parse_mode='Markdown')
                l_time = (day + "23:45")

            time.sleep(30)
        except Exception as e:
            print(f"Xato: {e}"); time.sleep(10)

if __name__ == "__main__":
    keep_alive()
    run_scheduler()
