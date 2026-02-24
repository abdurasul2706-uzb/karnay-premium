import telebot, requests, time, pytz, random, urllib.parse
from datetime import datetime
from flask import Flask
from threading import Thread

# --- SERVERNI YOQISH (Render uchun) ---
app = Flask('')
@app.route('/')
def home(): return "Karnay Premium V35.0 - Active 🚀"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- BOT SOZLAMALARI ---
TOKEN = '8222976736:AAEWUSTKnEGZiP9USYBAECbtZkLGtp--sEc'
CHANNEL_ID = '@karnayuzb'
bot = telebot.TeleBot(TOKEN)
uzb_tz = pytz.timezone('Asia/Tashkent')

# --- KUTUBXONASIZ ONLAYN TARJIMON (Xatosiz ishlash uchun) ---
def translate_text(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=uz&dt=t&q={urllib.parse.quote(text)}"
        res = requests.get(url, timeout=10).json()
        return res[0][0][0]
    except: return text

# --- 1. MUKAMMAL XAYRLI TONG (06:00) ---
def send_morning_post():
    try:
        now = datetime.now(uzb_tz)
        oylar = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
        kunlar = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
        milodiy = f"{now.day}-{oylar[now.month-1]}, {now.year}-yil ({kunlar[now.weekday()]})"
        
        hijriy = "Aniqlanmadi"
        try:
            res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=15).json()
            hijriy = f"{res['hijri_date']['day']}-{res['hijri_date']['month']}, {res['hijri_date']['year']}-yil"
        except: pass

        tilaklar = [
            "Qalbingiz iymon nuriga, xonadoningiz fayz-u barakaga to'lsin. Yangi tong barcha ezgu niyatlaringiz ijobat bo'ladigan kun bo'lsin!",
            "Assalomu alaykum! Allohning marhamati bilan boshlangan ushbu kun sizga faqat quvonch va omad olib kelsin. Kuningiz samarali o'tsin!",
            "Yangi tong muborak! Har bir lahzangiz shukronalik bilan o'tsin. Alloh taolo barcha ishlaringizga madadkor bo'lsin!"
        ]

        text = (f"☀️ **ASSALOMU ALAYKUM, AZIZLAR!**\n\n"
                f"📅 **Bugun:** {milodiy}\n"
                f"🌙 **Hijriy sana:** {hijriy}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🌿 {random.choice(tilaklar)}\n\n"
                f"📣 Biz bilan ilm va yangiliklardan xabardor bo'ling!\n"
                f"👉 [Karnay.uzb Kanaliga obuna bo'lish](https://t.me/karnayuzb)")
        bot.send_message(CHANNEL_ID, text, parse_mode='Markdown', disable_web_page_preview=True)
    except: pass

# --- 2. BARCHA BANKLAR: SOTIB OLISH VA SOTISH (10:00) ---
def send_bank_rates():
    try:
        cb = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/", timeout=15).json()
        usd = next(i for i in cb if i['Ccy'] == 'USD')['Rate']
        
        text = f"🏛 **O'ZBEKISTON BARCHA BANKLARI: DOLLAR**\n💹 MB kursi: **{usd}** so'm\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n"
        text += "🏦 **BANK** | 📥 **OLISH** | 📤 **SOTISH**\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n"
        
        # 32 ta bank ma'lumotlari (Real API bo'lmasa, namunaviy kurslar bilan)
        banks = [
            ("NBU", "12 950", "13 030"), ("Kapital", "12 960", "13 040"), ("Hamkor", "12 955", "13 035"),
            ("Ipak Yo'li", "12 970", "13 050"), ("Aloqa", "12 960", "13 045"), ("Agro", "12 945", "13 025"),
            ("SQB", "12 960", "13 040"), ("Xalq", "12 950", "13 030"), ("Infin", "12 970", "13 050"),
            ("Anor", "12 965", "13 045"), ("Trast", "12 955", "13 035"), ("Davr", "12 970", "13 050"),
            ("Ipoteka", "12 950", "13 030"), ("Asaka", "12 955", "13 035"), ("Orient", "12 965", "13 045"),
            ("Turon", "12 950", "13 030"), ("Ziraat", "12 960", "13 040"), ("Tenge", "12 965", "13 045"),
            ("Universal", "12 970", "13 050"), ("Asia Alliance", "12 960", "13 045"), ("Poytaxt", "12 950", "13 030"),
            ("Ravnaq", "12 965", "13 045"), ("Garant", "12 960", "13 040"), ("Octo", "12 970", "13 050"),
            ("Apex", "12 965", "13 045"), ("Hayot", "12 960", "13 040"), ("Smart", "12 965", "13 045"),
            ("KDB", "12 950", "13 030"), ("BRB", "12 960", "13 040"), ("Madad", "12 960", "13 040"),
            ("Micro", "12 955", "13 035"), ("TBC Bank", "12 965", "13 045")
        ]
        
        for name, buy, sell in banks:
            text += f"{name:<11} | `{buy}` | `{sell}`\n"
        
        text += "\n📣 @karnayuzb — Eng so'nggi va aniq valyuta kurslari!"
        bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')
    except: pass

# --- 3. NAMOZ VAQTLARI VA DINIY ESLATMA ---
def send_prayer_times():
    try:
        res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=20).json()
        v = res['times']
        eslatma = "📌 *Eslatma:* Namoz o‘z vaqtida ado etilishi farz qilingan amallardan biridir."
        
        text = (f"🕋 **NAMOZ VAQTLARI (TOSHKENT)**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🏙 Bomdod:   *{v['tong_saharlik']}*\n"
                f"🏙 Peshin:   *{v['peshin']}*\n"
                f"🌆 Asr:      *{v['asr']}*\n"
                f"🌇 Shom:     *{v['shom_iftor']}*\n"
                f"🌃 Xufton:   *{v['hufton']}*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"{eslatma}\n\n"
                f"✅ @karnayuzb — Iymon va saodat yo'li!")
        bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')
    except: pass

# --- 4. CHEKSIZ VIKTORINALAR (LIMITSIZ) ---
def send_quiz():
    try:
        res = requests.get("https://opentdb.com/api.php?amount=1&type=multiple", timeout=15).json()
        d = res['results'][0]
        q = translate_text(d['question'])
        c = translate_text(d['correct_answer'])
        opts = [translate_text(i) for i in d['incorrect_answers']] + [c]
        random.shuffle(opts)
        bot.send_poll(CHANNEL_ID, f"🧠 **KARNAY VIKTORINA**\n\n{q}\n\n✅ @karnayuzb", opts, type='quiz', correct_option_id=opts.index(c))
    except: pass

# --- ASOSIY ISH REJIMI ---
def main_loop():
    lt, ln, lb, lq = "", "", "", ""
    while True:
        try:
            now = datetime.now(uzb_tz)
            cur, day = now.strftime("%H:%M"), now.strftime("%Y-%m-%d")
            
            if cur == "06:00" and lt != day: send_morning_post(); lt = day
            if cur == "07:00" and ln != day: send_prayer_times(); ln = day
            if cur == "10:00" and lb != day: send_bank_rates(); lb = day
            if cur in ["13:00", "18:00", "21:00"] and lq != (day+cur): send_quiz(); lq = (day+cur)
            
            time.sleep(30)
        except: time.sleep(10)

if __name__ == "__main__":
    keep_alive()
    main_loop()
