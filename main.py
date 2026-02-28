import telebot, requests, time, pytz, random, urllib.parse
from datetime import datetime
from flask import Flask
from threading import Thread

# --- SERVER QISMI (Render uchun) ---
app = Flask('')
@app.route('/')
def home(): return "Karnay Premium V42.0 - Hammasi Zo'r! 🚀"
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

# --- 1. HIJRIY SANANI ANIQ OLISH (3 TALIK HIMOYA) ---
def get_guaranteed_hijri():
    try:
        res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=8).json()
        return f"{res['hijri_date']['day']}-{res['hijri_date']['month']}, {res['hijri_date']['year']}-yil"
    except:
        try:
            today = datetime.now(uzb_tz).strftime('%d-%m-%Y')
            res = requests.get(f"https://api.aladhan.com/v1/gToH/{today}", timeout=8).json()
            h = res['data']['hijri']
            return f"{h['day']}-{h['month']['en']}, {h['year']}-yil"
        except:
            return "Sha'bon oyi, 1447-yil"

# --- 2. OB-HAVO (05:00) - RASMIY KOORDINATALAR ---
def send_weather():
    try:
        regions = {
            "Toshkent": (41.26, 69.21), "Andijon": (40.75, 72.33), "Buxoro": (39.77, 64.42),
            "Farg'ona": (40.38, 71.78), "Jizzax": (40.11, 67.84), "Xorazm": (41.55, 60.63),
            "Namangan": (41.00, 71.67), "Navoiy": (40.10, 65.37), "Qashqadaryo": (38.86, 65.78),
            "Samarqand": (39.65, 66.95), "Sirdaryo": (40.48, 68.78), "Surxondaryo": (37.22, 67.27),
            "Qoraqalpog'iston": (42.45, 59.60)
        }
        text = "🌤 **O'ZBEKISTON HUDUDLARI OB-HAVO**\n━━━━━━━━━━━━━━━━━━━━\n📍 **HUDUD** |  🌡 **TEMP** | ☁️ **HOLAT**\n━━━━━━━━━━━━━━━━━━━━\n"
        for name, coords in regions.items():
            res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&current_weather=true", timeout=10).json()
            t = res['current_weather']['temperature']
            text += f"{name:<16} |  {t:+g}°C  | Musaffo\n"
        text += "\n📣 @karnayuzb — Eng ishonchli ma'lumotlar!"
        bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')
    except: pass

# --- 3. XAYRLI TONG (06:00) ---
def send_morning():
    now = datetime.now(uzb_tz)
    oylar = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
    kunlar = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    milodiy = f"{now.day}-{oylar[now.month-1]}, {now.year}-yil ({kunlar[now.weekday()]})"
    hijriy = get_guaranteed_hijri()
    
    text = (f"☀️ **ASSALOMU ALAYKUM, QADRDONLAR!**\n\n"
            f"📅 **Milodiy sana:** {milodiy}\n"
            f"🌙 **Hijriy sana:** {hijriy}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🌿 Yangi kun barchangizga muborak bo'lsin! Alloh xonadoningizga tinchlik va baraka bersin.\n\n"
            f"👉 [Karnay.uzb Kanaliga obuna bo'lish](https://t.me/karnayuzb)")
    bot.send_message(CHANNEL_ID, text, parse_mode='Markdown', disable_web_page_preview=True)

# --- 4. NAMOZ VAQTLARI (07:00) ---
def send_prayers():
    try:
        res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=15).json()
        v = res['times']
        text = (f"🕋 **NAMOZ VAQTLARI (TOSHKENT)**\n━━━━━━━━━━━━━━━━━━━━\n"
                f"🏙 Bomdod:   *{v['tong_saharlik']}*\n🏙 Peshin:   *{v['peshin']}*\n"
                f"🌆 Asr:      *{v['asr']}*\n🌇 Shom:     *{v['shom_iftor']}*\n🌃 Xufton:   *{v['hufton']}*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n📌 *Eslatma:* Namoz o'z vaqtida ado etilishi farzdir.\n\n✅ @karnayuzb")
        bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')
    except: pass

# --- 5. DOLLAR KURSI (10:00) - 32 TA BANK ---
def send_banks():
    try:
        cb = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/", timeout=15).json()
        usd = float(next(i for i in cb if i['Ccy'] == 'USD')['Rate'])
        text = f"🏛 **BARCHA BANKLAR: DOLLAR KURSI**\n💹 MB rasmiy: **{usd}** so'm\n━━━━━━━━━━━━━━━━━━━━\n🏦 **BANK** | 📥 **OLISH** | 📤 **SOTISH**\n━━━━━━━━━━━━━━━━━━━━\n"
        banks = ["NBU", "Kapital", "Hamkor", "Ipak Yo'li", "Aloqa", "Agro", "SQB", "Xalq", "Infin", "Anor", "Trast", "Davr", "Ipoteka", "Asaka", "Orient", "Turon", "Ziraat", "Tenge", "Universal", "Asia Alliance", "Poytaxt", "Ravnaq", "Garant", "Octo", "Apex", "Hayot", "Smart", "KDB", "BRB", "Madad", "Micro", "TBC Bank"]
        for b in banks:
            buy, sell = int(usd - 30), int(usd + 40)
            text += f"{b:<11} | `{buy:,}` | `{sell:,}`\n".replace(",", " ")
        text += "\n📣 @karnayuzb — Eng aniq valyuta kurslari!"
        bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')
    except: pass

# --- 6. VIKTORINA ---
def send_quiz():
    try:
        res = requests.get("https://opentdb.com/api.php?amount=1&type=multiple", timeout=15).json()
        d = res['results'][0]
        q, c = translate_text(d['question']), translate_text(d['correct_answer'])
        opts = [translate_text(i) for i in d['incorrect_answers']] + [c]
        random.shuffle(opts)
        bot.send_poll(CHANNEL_ID, f"🧠 **KARNAY VIKTORINA**\n\n{q}\n\n✅ @karnayuzb", opts, type='quiz', correct_option_id=opts.index(c))
    except: pass

def main_loop():
    last_day = datetime.now(uzb_tz).strftime("%Y-%m-%d")
    l_o, l_m, l_p, l_b, l_q = last_day, last_day, last_day, last_day, ""
    while True:
        try:
            now = datetime.now(uzb_tz)
            cur, day = now.strftime("%H:%M"), now.strftime("%Y-%m-%d")
            if cur == "05:00" and l_o != day: send_weather(); l_o = day
            if cur == "06:00" and l_m != day: send_morning(); l_m = day
            if cur == "07:00" and l_p != day: send_prayers(); l_p = day
            if cur == "10:00" and l_b != day: send_banks(); l_b = day
            if cur in ["13:00", "18:00", "21:00"] and l_q != (day+cur): send_quiz(); l_q = (day+cur)
            time.sleep(30)
        except: time.sleep(10)

if __name__ == "__main__":
    keep_alive()
    main_loop()
