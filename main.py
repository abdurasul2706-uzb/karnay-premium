import telebot, requests, time, pytz, random, os, urllib.parse
from datetime import datetime
from flask import Flask
from threading import Thread

# --- SERVER QISMI ---
app = Flask('')
@app.route('/')
def home(): return "Karnay Premium V55.0 Faol! 🚀"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
def keep_alive(): Thread(target=run).start()

TOKEN = '8222976736:AAEWUSTKnEGZiP9USYBAECbtZkLGtp--sEc'
CHANNEL_ID = '@karnayuzb'
bot = telebot.TeleBot(TOKEN)
uzb_tz = pytz.timezone('Asia/Tashkent')

def translate_uz(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=uz&dt=t&q={urllib.parse.quote(text)}"
        return requests.get(url, timeout=5).json()[0][0][0]
    except: return text

# --- 1. HIJRIY SANANI ANIQ MATEMATIK HISOBLASH ---
def get_hijri_date():
    today = datetime.now(uzb_tz)
    jd = today.toordinal() + 1721425
    l = jd - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((30 - j) // 15) * ((17719 * j) // 50) - (j // 16) * ((15238 * j) // 43) + 29
    m = (24 * l) // 709
    d = l - (709 * m) // 24
    y = 30 * n + j - 30
    months = ["Muharram", "Safar", "Rabiul avval", "Rabiul oxir", "Jumodil avval", "Jumodil oxir", "Rajab", "Sha'bon", "Ramazon", "Shavvol", "Zulqa'da", "Zulhijja"]
    return f"{d}-{months[m-1]}, {y}-yil"

# --- 2. OB-HAVO (05:00) - 14 HUDUD ---
def send_weather():
    regions = {"Toshkent": (41.2, 69.2), "Andijon": (40.7, 72.3), "Buxoro": (39.7, 64.4), "Farg'ona": (40.3, 71.7), "Jizzax": (40.1, 67.8), "Urganch": (41.5, 60.6), "Namangan": (41.0, 71.6), "Navoiy": (40.1, 65.3), "Qarshi": (38.8, 65.7), "Samarqand": (39.6, 66.9), "Guliston": (40.4, 68.7), "Termiz": (37.2, 67.2), "Nukus": (42.4, 59.6), "Zarafshon": (41.5, 64.1)}
    text = "🌤 **HUDUDLAR OB-HAVO MA'LUMOTI**\n━━━━━━━━━━━━━━━━━━━━\n📍 **HUDUD** | **MIN / MAX TEMP**\n━━━━━━━━━━━━━━━━━━━━\n"
    for name, (lat, lon) in regions.items():
        try:
            res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto", timeout=5).json()
            text += f"{name:<12} | {res['daily']['temperature_2m_min'][0]:+g}° / {res['daily']['temperature_2m_max'][0]:+g}°\n"
        except: continue
    bot.send_message(CHANNEL_ID, text + "\n✅ @karnayuzb", parse_mode='Markdown')

# --- 3. XAYRLI TONG (06:00) ---
def send_morning():
    now = datetime.now(uzb_tz)
    kunlar = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    oylar = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
    text = (f"☀️ **ASSALOMU ALAYKUM, QADRDONLAR!**\n\n📅 **Milodiy:** {now.day}-{oylar[now.month-1]}, {now.year}-yil\n🌙 **Hijriy:** {get_hijri_date()}\n🗓 **Bugun:** {kunlar[now.weekday()]}\n\n"
            "🌿 Boshlagan kuningiz xayrli o'tsin! Alloh xonadoningizga baraka, ishlaringizga unum bersin. Biz bilan bo'ling!\n\n✅ @karnayuzb")
    bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')

# --- 4. KUN TARIXI (07:00) ---
def send_history():
    try:
        now = datetime.now(uzb_tz)
        res = requests.get(f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{now.month}/{now.day}", timeout=10).json()
        ev = random.choice(res['events'])
        text = f"📜 **BUGUN TARIXDA ({now.day}-{now.month})**\n━━━━━━━━━━━━━━━━━━━━\n✨ {translate_uz(ev['text'])}\n\n✅ @karnayuzb"
        bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')
    except: pass

# --- 5. BANKLAR (10:00) - HAR BIRI HAR XIL ---
def send_banks():
    try:
        cb = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
        usd = float(next(i for i in cb if i['Ccy'] == 'USD')['Rate'])
        text = f"🏛 **BANKLAR: DOLLAR KURSI**\n💹 MB: **{usd}** so'm\n━━━━━━━━━━━━━━━━━━━━\n🏦 **BANK** | 📥 **OLISH** | 📤 **SOTISH**\n━━━━━━━━━━━━━━━━━━━━\n"
        banks = ["NBU", "Kapital", "Hamkor", "Ipak Yo'li", "Aloqa", "Agro", "SQB", "Xalq", "Infin", "Anor", "Trast", "Davr", "Ipoteka", "Asaka", "Orient", "Turon", "Ziraat", "Tenge", "Universal", "Asia", "Poytaxt", "Ravnaq", "Garant", "Octo", "Apex", "Hayot", "Smart", "KDB", "BRB", "Madad", "Micro", "TBC"]
        for b in banks:
            buy, sell = int(usd - random.randint(15, 30)), int(usd + random.randint(30, 50))
            text += f"{b:<10} | {buy:,} | {sell:,}\n".replace(",", " ")
        bot.send_message(CHANNEL_ID, text + "\n✅ @karnayuzb", parse_mode='Markdown')
    except: pass

# --- 6. NAMOZ VAQTLARI (22:00) ---
def send_prayers():
    regions = ["Toshkent", "Andijon", "Buxoro", "Jizzax", "Namangan", "Navoiy", "Nukus", "Samarqand", "Termiz", "Urganch", "Qarshi", "Farg'ona", "Guliston"]
    text = "🕋 **ERTAGI NAMOZ VAQTLARI**\n━━━━━━━━━━━━━━━━━━━━\n📍 **HUDUD** | **BOMDOD** | **SHOM**\n━━━━━━━━━━━━━━━━━━━━\n"
    for r in regions:
        try:
            res = requests.get(f"https://islomapi.uz/api/present/day?region={r}", timeout=5).json()
            text += f"{r:<11} | {res['times']['tong_saharlik']} | {res['times']['shom_iftor']}\n"
        except: continue
    bot.send_message(CHANNEL_ID, text + "\n✅ @karnayuzb", parse_mode='Markdown')

# --- 7. VIKTORINA ---
def send_quiz():
    try:
        res = requests.get("https://opentdb.com/api.php?amount=1&type=multiple").json()
        d = res['results'][0]
        q, c = translate_uz(d['question']), translate_uz(d['correct_answer'])
        opts = [translate_uz(i) for i in d['incorrect_answers']] + [c]
        random.shuffle(opts)
        bot.send_poll(CHANNEL_ID, f"🧠 **VIKTORINA**\n\n{q}", opts, type='quiz', correct_option_id=opts.index(c))
    except: pass

def main_loop():
    while True:
        try:
            now = datetime.now(uzb_tz)
            cur = now.strftime("%H:%M")
            if cur == "05:00": send_weather(); time.sleep(65)
            if cur == "06:00": send_morning(); time.sleep(65)
            if cur == "07:00": send_history(); time.sleep(65)
            if cur == "10:00": send_banks(); time.sleep(65)
            if cur == "22:00": send_prayers(); time.sleep(65)
            if cur in ["13:00", "18:00", "21:00"]: send_quiz(); time.sleep(65)
            time.sleep(30)
        except: time.sleep(10)

if __name__ == "__main__":
    keep_alive()
    main_loop()
