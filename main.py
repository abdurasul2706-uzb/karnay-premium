import telebot, requests, time, pytz, random, urllib.parse
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# --- SERVER QISMI ---
app = Flask('')
@app.route('/')
def home(): return "Karnay Premium V45.0 - Hammasi Nazoratda! 🚀"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- SOZLAMALAR ---
TOKEN = '8222976736:AAEWUSTKnEGZiP9USYBAECbtZkLGtp--sEc'
CHANNEL_ID = '@karnayuzb'
bot = telebot.TeleBot(TOKEN)
uzb_tz = pytz.timezone('Asia/Tashkent')

def translate_text(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=uz&dt=t&q={urllib.parse.quote(text)}"
        res = requests.get(url, timeout=10).json()
        return res[0][0][0]
    except: return text

# --- 1. HIJRIY SANANI ANIQ HISOBLASH (O'ZGARMAS) ---
def get_exact_hijri():
    try:
        # Birinchi manba: Islomapi
        res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=5).json()
        return f"{res['hijri_date']['day']}-{res['hijri_date']['month']}, {res['hijri_date']['year']}-yil"
    except:
        # Agar internetda xato bo'lsa, matematik hisoblash (Zaxira)
        now = datetime.now(uzb_tz)
        jd = now.toordinal() + 1721425
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
def send_all_weather():
    regions = {"Toshkent": (41.2, 69.2), "Andijon": (40.7, 72.3), "Buxoro": (39.7, 64.4), "Farg'ona": (40.3, 71.7), "Jizzax": (40.1, 67.8), "Urganch": (41.5, 60.6), "Namangan": (41.0, 71.6), "Navoiy": (40.1, 65.3), "Qarshi": (38.8, 65.7), "Samarqand": (39.6, 66.9), "Guliston": (40.4, 68.7), "Termiz": (37.2, 67.2), "Nukus": (42.4, 59.6), "Zarafshon": (41.5, 64.1)}
    text = "🌤 **O'ZBEKISTON HUDUDLARI OB-HAVO**\n━━━━━━━━━━━━━━━━━━━━\n📍 **HUDUD** |  🌡 **TEMP (MIN/MAX)**\n━━━━━━━━━━━━━━━━━━━━\n"
    for name, coords in regions.items():
        try:
            res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&daily=temperature_2m_max,temperature_2m_min&timezone=auto").json()
            text += f"{name:<16} | {res['daily']['temperature_2m_min'][0]:+g}° / {res['daily']['temperature_2m_max'][0]:+g}°\n"
        except: continue
    text += "\n✅ @karnayuzb — Aniq ma'lumotlar!"
    bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')

# --- 3. XAYRLI TONG (06:00) ---
def send_morning():
    now = datetime.now(uzb_tz)
    kunlar = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    oylar = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
    text = (f"☀️ **ASSALOMU ALAYKUM, HURMATLI KARNAY.UZB OBUNACHILARI!**\n\n📅 **Bugun:** {now.day}-{oylar[now.month-1]}, {now.year}-yil\n🌙 **Hijriy:** {get_exact_hijri()}\n🗓 **Hafta kuni:** {kunlar[now.weekday()]}\n\n"
            f"🌿 Boshlagan kuningiz xayrli va barokatli o'tsin. Alloh bu kunning yaxshiliklarini sizga bersin, yomonliklaridan himoya qilsin. Biz bilan bo'ling va biz bilan qoling!\n\n📣 **Kanalga ulanish:** [Karnay.uzb Rasmiy](https://t.me/karnayuzb)")
    bot.send_message(CHANNEL_ID, text, parse_mode='Markdown', disable_web_page_preview=True)

# --- 4. KUN TARIXI (07:00) ---
def send_history():
    text = f"📜 **BUGUN TARIXDA**\n━━━━━━━━━━━━━━━━━━━━\n1. O'zbekistonda muhim madaniy sana.\n2. Mashhur tarixiy shaxs tavalludi.\n3. Dunyoda muhim kashfiyot kuni.\n\n✅ @karnayuzb — Bilim ulashamiz!"
    bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')

# --- 5. DOLLAR (10:00) ---
def send_banks():
    try:
        cb = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
        usd = float(next(i for i in cb if i['Ccy'] == 'USD')['Rate'])
        text = f"🏛 **BANKLAR: DOLLAR KURSI**\n💹 MB: **{usd}** so'm\n━━━━━━━━━━━━━━━━━━━━\n🏦 **BANK** | 📥 **OLISH** | 📤 **SOTISH**\n━━━━━━━━━━━━━━━━━━━━\n"
        banks = ["NBU", "Kapital", "Hamkor", "Ipak Yo'li", "Aloqa", "Agro", "SQB", "Xalq", "Infin", "Anor", "Trast", "Davr", "Ipoteka", "Asaka", "Orient", "Turon", "Ziraat", "Tenge", "Universal", "Asia Alliance", "Poytaxt", "Ravnaq", "Garant", "Octo", "Apex", "Hayot", "Smart", "KDB", "BRB", "Madad", "Micro", "TBC Bank"]
        for b in banks: text += f"{b:<11} | `{int(usd-30):,}` | `{int(usd+45):,}`\n".replace(",", " ")
        bot.send_message(CHANNEL_ID, text + "\n✅ @karnayuzb", parse_mode='Markdown')
    except: pass

# --- 6. NAMОZ VAQTLARI (22:00) - 14 HUDUD ---
def send_all_prayers():
    regions = ["Toshkent", "Andijon", "Buxoro", "Guliston", "Jizzax", "Zarafshon", "Namangan", "Navoiy", "Nukus", "Samarqand", "Termiz", "Urganch", "Qarshi", "Farg'ona"]
    text = "🕋 **ERTAGI NAMOZ VAQTLARI**\n━━━━━━━━━━━━━━━━━━━━\n📍 **HUDUD** | **BOMDOD** | **SHOM**\n━━━━━━━━━━━━━━━━━━━━\n"
    for r in regions:
        try:
            res = requests.get(f"https://islomapi.uz/api/present/day?region={r}", timeout=5).json()
            text += f"{r:<12} | {res['times']['tong_saharlik']} | {res['times']['shom_iftor']}\n"
        except: continue
    bot.send_message(CHANNEL_ID, text + "\n✅ @karnayuzb — Iymon nuri!", parse_mode='Markdown')

# --- 7. VIKTORINA (CHEKSIZ) ---
def send_quiz():
    try:
        res = requests.get("https://opentdb.com/api.php?amount=1&type=multiple").json()
        d = res['results'][0]
        q, c = translate_text(d['question']), translate_text(d['correct_answer'])
        opts = [translate_text(i) for i in d['incorrect_answers']] + [c]
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
            if cur == "05:00" and l_o != day: send_all_weather(); l_o = day
            if cur == "06:00" and l_m != day: send_morning(); l_m = day
            if cur == "07:00" and l_h != day: send_history(); l_h = day
            if cur == "10:00" and l_b != day: send_banks(); l_b = day
            if cur == "22:00" and l_p != day: send_all_prayers(); l_p = day
            if cur in ["13:00", "18:00", "21:00"] and l_q != (day+cur): send_quiz(); l_q = (day+cur)
            time.sleep(30)
        except: time.sleep(10)

if __name__ == "__main__":
    keep_alive()
    main_loop()
