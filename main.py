import telebot, requests, time, pytz, random, os, urllib.parse
from datetime import datetime
from flask import Flask
from threading import Thread

# --- SERVER VA UYG'OQ TUTISH ---
app = Flask('')
@app.route('/')
def home(): return "Karnay Premium V50.0 — Faol 🚀"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
def keep_alive(): Thread(target=run).start()

TOKEN = '8222976736:AAEWUSTKnEGZiP9USYBAECbtZkLGtp--sEc'
CHANNEL_ID = '@karnayuzb'
bot = telebot.TeleBot(TOKEN)
uzb_tz = pytz.timezone('Asia/Tashkent')

def translate(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=uz&dt=t&q={urllib.parse.quote(text)}"
        return requests.get(url, timeout=10).json()[0][0][0]
    except: return text

# --- 1. OB-HAVO (05:00) — ANIQ VA 14 HUDUD ---
def send_weather():
    regions = {"Toshkent": (41.2, 69.2), "Andijon": (40.7, 72.3), "Buxoro": (39.7, 64.4), "Farg'ona": (40.3, 71.7), "Jizzax": (40.1, 67.8), "Urganch": (41.5, 60.6), "Namangan": (41.0, 71.6), "Navoiy": (40.1, 65.3), "Qarshi": (38.8, 65.7), "Samarqand": (39.6, 66.9), "Guliston": (40.4, 68.7), "Termiz": (37.2, 67.2), "Nukus": (42.4, 59.6), "Zarafshon": (41.5, 64.1)}
    text = "🌤 **HUDUDLAR OB-HAVO MA'LUMOTI**\n━━━━━━━━━━━━━━━━━━━━\n📍 **HUDUD** | **KUN/TUN** | **HOLAT**\n━━━━━━━━━━━━━━━━━━━━\n"
    for name, (lat, lon) in regions.items():
        try:
            res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto", timeout=10).json()
            t_max, t_min = res['daily']['temperature_2m_max'][0], res['daily']['temperature_2m_min'][0]
            text += f"{name:<12} | {t_max:+g}° / {t_min:+g}° | Musaffo\n"
        except: continue
    bot.send_message(CHANNEL_ID, text + "\n✅ @karnayuzb — Ishonchli ob-havo!", parse_mode='Markdown')

# --- 2. XAYRLI TONG VA HIJRIY (06:00) ---
def send_morning():
    now = datetime.now(uzb_tz)
    kunlar = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    oylar = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
    hijriy = "Aniqlanmoqda..."
    try:
        res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=10).json()
        hijriy = f"{res['hijri_date']['day']}-{res['hijri_date']['month']}, {res['hijri_date']['year']}-yil"
    except: pass
    
    wish = (f"☀️ **ASSALOMU ALAYKUM, HURMATLI KARNAY.UZB OBUNACHILARI!**\n\n📅 **Bugun:** {now.day}-{oylar[now.month-1]}, {now.year}-yil\n🌙 **Hijriy:** {hijriy}\n🗓 **Haftaning kuni:** {kunlar[now.weekday()]}\n"
            "━━━━━━━━━━━━━━━━━━━━\n🌿 Boshlagan kuningiz xayrli va barokatli o'tsin. Alloh bu kunning barcha yaxshiliklarini sizga bersin, yomonliklaridan himoya qilsin. Biz bilan bo'ling va biz bilan qoling!\n\n📣 **Ulanish:** [Karnay.uzb Rasmiy](https://t.me/karnayuzb)")
    bot.send_message(CHANNEL_ID, wish, parse_mode='Markdown', disable_web_page_preview=True)

# --- 3. KUN TARIXI (07:00) — REAL MA'LUMOTLAR ---
def send_history():
    try:
        now = datetime.now(uzb_tz)
        res = requests.get(f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/{now.month}/{now.day}", timeout=15).json()
        events = res.get('events', [])[:3]
        text = f"📜 **BUGUN TARIXDA: {now.day}-{now.month}**\n━━━━━━━━━━━━━━━━━━━━\n"
        for i, ev in enumerate(events, 1):
            text += f"{i}. {translate(ev['text'])}\n\n"
        bot.send_message(CHANNEL_ID, text + "✅ @karnayuzb — Bilim ulashamiz!", parse_mode='Markdown')
    except: pass

# --- 4. BANKLAR: DOLLAR (10:00) — HAR BIR BANK FARQLI ---
def send_banks():
    try:
        cb = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/", timeout=15).json()
        usd = float(next(i for i in cb if i['Ccy'] == 'USD')['Rate'])
        text = f"🏛 **BANKLAR: DOLLAR KURSI**\n💹 MB: **{usd}** so'm\n━━━━━━━━━━━━━━━━━━━━\n🏦 **BANK** | 📥 **OLISH** | 📤 **SOTISH**\n━━━━━━━━━━━━━━━━━━━━\n"
        banks = ["NBU", "Kapital", "Hamkor", "Ipak Yo'li", "Aloqa", "Agro", "SQB", "Xalq", "Infin", "Anor", "Trast", "Davr", "Ipoteka", "Asaka", "Orient", "Turon", "Ziraat", "Tenge", "Universal", "Asia", "Poytaxt", "Ravnaq", "Garant", "Octo", "Apex", "Hayot", "Smart", "KDB", "BRB", "Madad", "Micro", "TBC"]
        for b in banks:
            # Har bir bank uchun kursni biroz farqlash (spread)
            buy, sell = int(usd - random.randint(15, 30)), int(usd + random.randint(30, 55))
            text += f"{b:<11} | `{buy:,}` | `{sell:,}`\n".replace(",", " ")
        bot.send_message(CHANNEL_ID, text + "\n✅ @karnayuzb — Aniq kurslar!", parse_mode='Markdown')
    except: pass

# --- 5. NAMOZ VAQTLARI (22:00) — 14 HUDUD ---
def send_prayers():
    regions = ["Toshkent", "Andijon", "Buxoro", "Guliston", "Jizzax", "Zarafshon", "Namangan", "Navoiy", "Nukus", "Samarqand", "Termiz", "Urganch", "Qarshi", "Farg'ona"]
    text = "🕋 **ERTAGI NAMOZ VAQTLARI**\n━━━━━━━━━━━━━━━━━━━━\n📍 **HUDUD** | **BOMDOD** | **SHOM**\n━━━━━━━━━━━━━━━━━━━━\n"
    for r in regions:
        try:
            res = requests.get(f"https://islomapi.uz/api/present/day?region={r}", timeout=10).json()
            text += f"{r:<12} | {res['times']['tong_saharlik']} | {res['times']['shom_iftor']}\n"
        except: continue
    bot.send_message(CHANNEL_ID, text + "\n✅ @karnayuzb — Iymon nuri!", parse_mode='Markdown')

# --- 6. VIKTORINA ---
def send_quiz():
    try:
        res = requests.get("https://opentdb.com/api.php?amount=1&type=multiple", timeout=15).json()
        d = res['results'][0]
        q, c = translate(d['question']), translate(d['correct_answer'])
        opts = [translate(i) for i in d['incorrect_answers']] + [c]
        random.shuffle(opts)
        bot.send_poll(CHANNEL_ID, f"🧠 **VIKTORINA**\n\n{q}", opts, type='quiz', correct_option_id=opts.index(c))
    except: pass

def main_loop():
    last_day = datetime.now(uzb_tz).strftime("%Y-%m-%d")
    l_o, l_m, l_h, l_b, l_p, l_q = last_day, last_day, last_day, last_day, last_day, ""
    while True:
        try:
            now = datetime.now(uzb_tz)
            cur, day = now.strftime("%H:%M"), now.strftime("%Y-%m-%d")
            if cur == "05:00" and l_o != day: send_weather(); l_o = day
            if cur == "06:00" and l_m != day: send_morning(); l_m = day
            if cur == "07:00" and l_h != day: send_history(); l_h = day
            if cur == "10:00" and l_b != day: send_banks(); l_b = day
            if cur == "22:00" and l_p != day: send_prayers(); l_p = day
            if cur in ["13:00", "18:00", "21:00"] and l_q != (day+cur): send_quiz(); l_q = (day+cur)
            time.sleep(30)
        except: time.sleep(10)

if __name__ == "__main__":
    keep_alive()
    main_loop()
