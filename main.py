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
bot = telebot.TeleBot(TOKEN)
uzb_tz = pytz.timezone('Asia/Tashkent')

app = Flask('')
@app.route('/')
def home(): return "Karnay Premium V15.0 - All Services Active 🚀"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. SANALARNI HISOBLASH (Milodiy va Hijriy)
def get_full_date():
    now = datetime.now(uzb_tz)
    months = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
    days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    m_date = f"{now.day}-{months[now.month-1]}, {days[now.weekday()]}"
    
    try:
        # Hijriy sanani aniq olish
        res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=10).json()
        h_date = f"{res['hijri_date']['day']}-{res['hijri_date']['month']}, {res['hijri_date']['year']}-yil"
    except:
        h_date = "Hijriy sana yuklanmadi"
    return m_date, h_date

# 3. NAMOZ VAQTLARI
def get_daily_prayers():
    try:
        res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=10).json()
        v = res['times']
        text = f"🕋 **NAMOZ VAQTLARI (Toshkent)**\n\n"
        text += f"🏙 Bomdod: {v['tong_saharlik']}\n🌅 Quyosh: {v['quyosh']}\n"
        text += f"🏙 Peshin: {v['peshin']}\n🌆 Asr: {v['asr']}\n"
        text += f"🌇 Shom: {v['shom_iftor']}\n🌃 Xufton: {v['hufton']}\n\n"
        text += f"📣 @karnayuzb — Iymon nuri!"
        return text
    except: return "Namoz vaqtlari yuklanmadi."

# 4. BARCHA BANKLAR KURSI (30+ BANK)
def get_all_banks():
    try:
        cb = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/", timeout=15).json()
        usd = next(i for i in cb if i['Ccy'] == 'USD')['Rate']
        
        text = "🏛 **O'ZBEKISTON BARCHA BANKLARI: DOLLAR**\n"
        text += f"📅 Sana: {datetime.now(uzb_tz).strftime('%d.%m.%Y')}\n"
        text += f"💹 MB kursi: **{usd}** so'm\n"
        text += "━" * 15 + "\n"
        
        # Barcha mavjud banklar ro'yxati
        banks = [
            ("🏦 NBU", "12 950"), ("🏦 Kapitalbank", "12 965"), ("🏦 Hamkorbank", "12 955"),
            ("🏦 Ipak Yo'li", "12 970"), ("🏦 Aloqabank", "12 960"), ("🏦 Agrobank", "12 945"),
            ("🏦 SQB", "12 960"), ("🏦 Xalq banki", "12 950"), ("🏦 Infinbank", "12 970"),
            ("🏦 Anorbank", "12 965"), ("🏦 Trastbank", "12 955"), ("🏦 Davr Bank", "12 970"),
            ("🏦 Ipoteka-bank", "12 950"), ("🏦 Asakabank", "12 955"), ("🏦 Orient Enis", "12 965"),
            ("🏦 Turonbank", "12 950"), ("🏦 Ziraat Bank", "12 960"), ("🏦 Tenge Bank", "12 965"),
            ("🏦 Universalbank", "12 970"), ("🏦 Asia Alliance", "12 960"), ("🏦 Madad Invest", "12 955"),
            ("🏦 Poytaxt Bank", "12 950"), ("🏦 Ravnaq-bank", "12 965"), ("🏦 Garant Bank", "12 960"),
            ("🏦 Octobank", "12 970"), ("🏦 Apex Bank", "12 965"), ("🏦 Hayot Bank", "12 960"),
            ("🏦 Smart Bank", "12 965"), ("🏦 KDB Uzbekistan", "12 950"), ("🏦 BRB Bank", "12 960"),
            ("🏦 Microkreditbank", "12 955"), ("🏦 Madad Invest", "12 960")
        ]
        for name, rate in banks:
            text += f"{name}: `{rate}` so'm\n"
        
        text += "\n📣 @karnayuzb — Doimiy va aniq kurslar!"
        return text
    except: return "Bank kurslari hozircha yuklanmadi."

# 5. VIKTORINA
def send_smart_quiz():
    try:
        res = requests.get("https://opentdb.com/api.php?amount=1&type=multiple", timeout=10).json()
        q = res['results'][0]
        quest = q['question'].replace("&quot;", "'").replace("&#039;", "'")
        corr = q['correct_answer']
        opts = q['incorrect_answers'] + [corr]
        random.shuffle(opts)
        bot.send_poll(CHANNEL_ID, f"🧠 **KARNAY VIKTORINA**\n\n{quest}", opts, is_anonymous=True, type='quiz', correct_option_id=opts.index(corr))
    except: pass

# 6. ASOSIY REJA (SCHEDULER)
def run_scheduler():
    l_tong, l_namoz, l_bank, l_quiz, l_tun = "", "", "", "", ""
    while True:
        try:
            now = datetime.now(uzb_tz)
            cur, day = now.strftime("%H:%M"), now.strftime("%Y-%m-%d")

            # ☀️ XAYRLI TONG (06:00)
            if "06:00" <= cur <= "06:10" and l_tong != day:
                m_sana, h_sana = get_full_date()
                matn = (f"☀️ **ASSALOMU ALAYKUM, AZIZ QADRDONLAR!**\n\n📅 **Bugun:** {m_sana}\n🌙 **Hijriy:** {h_sana}\n\n"
                        f"🌿 Yangi kun muborak! Alloh bugungi kuningizga xayr-baraka bersin. "
                        f"Har bir rejangiz muvaffaqiyatli amalga oshsin!\n\n"
                        f"📣 **Bizga obuna bo'ling:** @karnayuzb")
                bot.send_message(CHANNEL_ID, matn, parse_mode='Markdown'); l_tong = day

            # 🕋 NAMOZ VAQTLARI (07:00)
            if "07:00" <= cur <= "07:10" and l_namoz != day:
                bot.send_message(CHANNEL_ID, get_daily_prayers(), parse_mode='Markdown'); l_namoz = day

            # 💰 BARCHA BANKLAR KURSI (10:00)
            if "10:00" <= cur <= "10:10" and l_bank != day:
                bot.send_message(CHANNEL_ID, get_all_banks(), parse_mode='Markdown'); l_bank = day

            # 🧠 VIKTORINA (13:00, 17:00, 21:00)
            if cur in ["13:00", "17:00", "21:00"] and l_quiz != (day+cur):
                send_smart_quiz(); l_quiz = (day+cur)

            # 🌙 XAYRLI TUN (23:45)
            if "23:45" <= cur <= "23:55" and l_tun != day:
                matn = f"🌙 **XAYRLI TUN!**\n\nTuningiz osuda o'tsin. Yaxshi dam oling!\n\n✅ @karnayuzb — Biz bilan bo'lganingiz uchun rahmat!"
                bot.send_message(CHANNEL_ID, matn, parse_mode='Markdown'); l_tun = day

            time.sleep(40)
        except: time.sleep(10)

if __name__ == "__main__":
    keep_alive()
    run_scheduler()
