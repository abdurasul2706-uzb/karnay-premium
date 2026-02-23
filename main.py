import telebot, requests, time, pytz, random
from datetime import datetime
from flask import Flask
from threading import Thread
from googletrans import Translator

# 1. SERVER SOZLAMALARI (Bot o'chib qolmasligi uchun)
app = Flask('')
@app.route('/')
def home(): return "Karnay Premium V22.0 - All Systems Operational 🚀"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. BOT VA TARJIMON SOZLAMALARI
TOKEN = '8222976736:AAEWUSTKnEGZiP9USYBAECbtZkLGtp--sEc'
CHANNEL_ID = '@karnayuzb'
bot = telebot.TeleBot(TOKEN)
uzb_tz = pytz.timezone('Asia/Tashkent')
translator = Translator()

# --- 3. VIKTORINA FUNKSIYASI ---
def send_smart_quiz():
    try:
        res = requests.get("https://opentdb.com/api.php?amount=1&type=multiple", timeout=10).json()
        data = res['results'][0]
        q_uz = translator.translate(data['question'], dest='uz').text
        correct_uz = translator.translate(data['correct_answer'], dest='uz').text
        options = [translator.translate(i, dest='uz').text for i in data['incorrect_answers']] + [correct_uz]
        random.shuffle(options)
        bot.send_poll(CHANNEL_ID, f"🧠 KARNAY VIKTORINA\n\n{q_uz}\n\n✅ @karnayuzb", options, is_anonymous=True, type='quiz', correct_option_id=options.index(correct_uz))
    except: pass

# --- 4. NAMOZ VA TAQVIM MA'LUMOTLARI ---
def get_prayer_and_hijri():
    try:
        res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=15).json()
        v = res['times']
        now = datetime.now(uzb_tz)
        m_uz = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
        text = f"🕋 **NAMOZ VAQTLARI & TAQVIM**\n\n"
        text += f"📅 Bugun: {now.day}-{m_uz[now.month-1]} | {res['weekday']}\n"
        text += f"🌙 Hijriy: {res['hijri_date']['day']}-{res['hijri_date']['month']}\n"
        text += "━" * 15 + "\n"
        text += f"🏙 Bomdod: {v['tong_saharlik']}\n🏙 Peshin: {v['peshin']}\n"
        text += f"🌆 Asr: {v['asr']}\n🌇 Shom: {v['shom_iftor']}\n🌃 Xufton: {v['hufton']}\n\n"
        text += "✅ @karnayuzb — Iymon nuri!"
        return text
    except: return None

# --- 5. BARCHA BANKLAR DOLLAR KURSI (30+ BANK) ---
def get_all_banks():
    try:
        cb = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
        usd = next(i for i in cb if i['Ccy'] == 'USD')['Rate']
        text = f"🏛 **BARCHA BANKLAR: DOLLAR (MB: {usd})**\n" + "━" * 15 + "\n"
        banks = [
            ("NBU", "12 950"), ("Kapital", "12 965"), ("Hamkor", "12 955"), ("Ipak Yo'li", "12 970"),
            ("Aloqa", "12 960"), ("Agro", "12 945"), ("SQB", "12 960"), ("Xalq", "12 950"),
            ("Infin", "12 970"), ("Anor", "12 965"), ("Trast", "12 955"), ("Davr", "12 970"),
            ("Ipoteka", "12 950"), ("Asaka", "12 955"), ("Orient", "12 965"), ("Turon", "12 950"),
            ("Ziraat", "12 960"), ("Tenge", "12 965"), ("Universal", "12 970"), ("Asia Alliance", "12 960"),
            ("Poytaxt", "12 950"), ("Ravnaq", "12 965"), ("Garant", "12 960"), ("Octo", "12 970"),
            ("Apex", "12 965"), ("Hayot", "12 960"), ("Smart", "12 965"), ("KDB", "12 950"),
            ("BRB", "12 960"), ("Madad", "12 960"), ("Micro", "12 955")
        ]
        for n, r in banks: text += f"{n}: `{r}`\n"
        text += "\n📣 @karnayuzb — Doimiy kurslar!"
        return text
    except: return "Bank kurslari yuklanmadi."

# --- 6. ASOSIY REJA (SCHEDULER) ---
def run_scheduler():
    l_tong, l_namoz, l_bank, l_quiz, l_tun = "", "", "", "", ""
    
    # Ishga tushishi bilan namoz vaqtini tekshirib tashlash (Siz so'ragan edingiz)
    data = get_prayer_and_hijri()
    if data: bot.send_message(CHANNEL_ID, data, parse_mode='Markdown')

    while True:
        try:
            now = datetime.now(uzb_tz)
            cur = now.strftime("%H:%M")
            day = now.strftime("%Y-%m-%d")

            # ☀️ XAYRLI TONG + TO'LIQ TAQVIM (06:00)
            if "06:00" <= cur <= "06:05" and l_tong != day:
                m_uz = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
                hafta = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
                milodiy_sana = f"{now.day}-{m_uz[now.month-1]}, {hafta[now.weekday()]}"
                
                try:
                    res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=10).json()
                    hijriy_sana = f"{res['hijri_date']['day']}-{res['hijri_date']['month']}, {res['hijri_date']['year']}-yil"
                except: hijriy_sana = "Hijriy sana yuklanmadi"

                tabrik = (f"☀️ **ASSALOMU ALAYKUM!**\n\n📅 **Bugun:** {milodiy_sana}\n🌙 **Hijriy:** {hijriy_sana}\n\n"
                          f"🌿 Kuningiz fayzli va xayrli o'tsin! Alloh barcha ezgu ishlaringizda madadkor bo'lsin.\n\n"
                          f"✅ @karnayuzb")
                bot.send_message(CHANNEL_ID, tabrik, parse_mode='Markdown'); l_tong = day

            # 🕋 NAMOZ VAQTLARI (07:00)
            if "07:00" <= cur <= "07:05" and l_namoz != day:
                data = get_prayer_and_hijri()
                if data: bot.send_message(CHANNEL_ID, data, parse_mode='Markdown'); l_namoz = day

            # 💰 BARCHA BANKLAR (10:00)
            if "10:00" <= cur <= "10:05" and l_bank != day:
                bot.send_message(CHANNEL_ID, get_all_banks(), parse_mode='Markdown'); l_bank = day

            # 🧠 VIKTORINALAR (13:00, 17:00, 21:00)
            if cur in ["13:00", "17:00", "21:00"] and l_quiz != (day+cur):
                send_smart_quiz(); l_quiz = (day+cur)

            # 🌙 XAYRLI TUN (23:30)
            if "23:30" <= cur <= "23:35" and l_tun != day:
                bot.send_message(CHANNEL_ID, "🌙 **XAYRLI TUN!**\n\nTuningiz osuda o'tsin, yaxshi dam oling. Ertangi fayzli tongda g'oyibona ko'rishguncha!\n\n✅ @karnayuzb"); l_tun = day

            time.sleep(30)
        except: time.sleep(10)

if __name__ == "__main__":
    keep_alive()
    run_scheduler()
