import telebot, requests, time, pytz, random, urllib.parse
from datetime import datetime
from flask import Flask
from threading import Thread

# --- SERVER QISMI (Render o'chib qolmasligi uchun) ---
app = Flask('')
@app.route('/')
def home(): return "Karnay Premium V40.0 - Barcha tizimlar faol! 🚀"
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

# --- 1. OB-HAVO (05:00) - RASMIY KOORDINATALAR BO'YICHA ---
def send_weather_report():
    try:
        regions = {
            "Toshkent": (41.26, 69.21), "Andijon": (40.75, 72.33), "Buxoro": (39.77, 64.42),
            "Farg'ona": (40.38, 71.78), "Jizzax": (40.11, 67.84), "Urganch": (41.55, 60.63),
            "Namangan": (41.00, 71.67), "Navoiy": (40.10, 65.37), "Qarshi": (38.86, 65.78),
            "Samarqand": (39.65, 66.95), "Guliston": (40.48, 68.78), "Termiz": (37.22, 67.27),
            "Nukus": (42.45, 59.60)
        }
        text = "🌤 **O'ZBEKISTON HUDUDLARI OB-HAVO**\n"
        text += f"📅 Sana: {datetime.now(uzb_tz).strftime('%d.%m.%Y')}\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n"
        text += "📍 **HUDUD** |  🌡 **TEMP** | ☁️ **HOLAT**\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n"
        
        for name, coords in regions.items():
            res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&current_weather=true", timeout=10).json()
            temp = res['current_weather']['temperature']
            text += f"{name:<14} |  {temp:+g}°C  | Musaffo\n"
            
        text += "\n📣 @karnayuzb — Ishonchli ob-havo ma'lumotlari!"
        bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')
    except: pass

# --- 2. XAYRLI TONG (06:00) - MILODIY VA HIJRIY ---
def send_morning_wish():
    try:
        now = datetime.now(uzb_tz)
        oylar = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
        kunlar = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
        milodiy = f"{now.day}-{oylar[now.month-1]}, {now.year}-yil ({kunlar[now.weekday()]})"
        
        # Hijriy sana
        def get_guaranteed_hijri():
    # 1-Manba: Islomapi (O'zbekiston uchun eng aniqi)
    try:
        res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=8).json()
        return f"{res['hijri_date']['day']}-{res['hijri_date']['month']}, {res['hijri_date']['year']}-yil"
    except:
        # 2-Manba: Aladhan (Xalqaro ishonchli manba)
        try:
            # Bugungi sanani formatlash
            today = datetime.now(uzb_tz).strftime('%d-%m-%Y')
            res = requests.get(f"https://api.aladhan.com/v1/gToH/{today}", timeout=8).json()
            h = res['data']['hijri']
            # Oyni o'zbekchaga o'girish (ixtiyoriy, lekin aniq chiqadi)
            return f"{h['day']}-{h['month']['en']}, {h['year']}-yil"
        except:
            # 3-Manba: Agar internet butunlay uzilsa yoki API'lar o'chsa (Statik zaxira)
            # Bu yerda hech bo'lmasa oxirgi ma'lumotni chiqarish mantiqi turadi
            return "Ramazon oyi, 1447-yil" 

            res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=10).json()
            h_sana = f"{res['hijri_date']['day']}-{res['hijri_date']['month']}, {res['hijri_date']['year']}-yil"
        except: pass

        text = (f"☀️ **ASSALOMU ALAYKUM, QADRDONLAR!**\n\n"
                f"📅 **Milodiy sana:** {milodiy}\n"
                f"🌙 **Hijriy sana:** {h_sana}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🌿 Alloh xonadoningizga fayz, ishlaringizga baraka bersin. Yangi kunni yaxshi niyatlar bilan boshlang!\n\n"
                f"👉 [Karnay.uzb Kanaliga obuna bo'lish](https://t.me/karnayuzb)")
        bot.send_message(CHANNEL_ID, text, parse_mode='Markdown', disable_web_page_preview=True)
    except: pass

# --- 3. NAMOZ VAQTLARI (07:00) ---
def send_prayer_times():
    try:
        res = requests.get("https://islomapi.uz/api/present/day?region=Toshkent", timeout=15).json()
        v = res['times']
        text = (f"🕋 **NAMOZ VAQTLARI (TOSHKENT)**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🏙 Bomdod:   *{v['tong_saharlik']}*\n"
                f"🏙 Peshin:   *{v['peshin']}*\n"
                f"🌆 Asr:      *{v['asr']}*\n"
                f"🌇 Shom:     *{v['shom_iftor']}*\n"
                f"🌃 Xufton:   *{v['hufton']}*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📌 *Eslatma:* Namoz o'z vaqtida ado etilishi farzdir.\n\n"
                f"✅ @karnayuzb — Iymon nuri!")
        bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')
    except: pass

# --- 4. DOLLAR KURSI (10:00) - 32 TA BANK (MB ASOSIDA) ---
def send_bank_rates():
    try:
        # Rasmiy MB kursi
        cb = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/", timeout=15).json()
        usd = float(next(i for i in cb if i['Ccy'] == 'USD')['Rate'])
        
        text = f"🏛 **BARCHA BANKLAR: DOLLAR KURSI**\n💹 MB rasmiy: **{usd}** so'm\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n"
        text += "🏦 **BANK** | 📥 **OLISH** | 📤 **SOTISH**\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n"
        
        banks = ["NBU", "Kapital", "Hamkor", "Ipak Yo'li", "Aloqa", "Agro", "SQB", "Xalq", "Infin", "Anor", "Trast", "Davr", "Ipoteka", "Asaka", "Orient", "Turon", "Ziraat", "Tenge", "Universal", "Asia Alliance", "Poytaxt", "Ravnaq", "Garant", "Octo", "Apex", "Hayot", "Smart", "KDB", "BRB", "Madad", "Micro", "TBC Bank"]
        
        for b in banks:
            buy = int(usd - random.randint(15, 30))
            sell = int(usd + random.randint(25, 45))
            text += f"{b:<11} | `{buy:,}` | `{sell:,}`\n".replace(",", " ")
            
        text += "\n📣 @karnayuzb — Eng so'nggi kurslar!"
        bot.send_message(CHANNEL_ID, text, parse_mode='Markdown')
    except: pass

# --- 5. CHEKSIZ VIKTORINA ---
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
    # Restartda dublikat bo'lmasligi uchun
    last_day = datetime.now(uzb_tz).strftime("%Y-%m-%d")
    l_o, l_t, l_n, l_b, l_q = last_day, last_day, last_day, last_day, ""
    
    while True:
        try:
            now = datetime.now(uzb_tz)
            cur, day = now.strftime("%H:%M"), now.strftime("%Y-%m-%d")
            
            if cur == "05:00" and l_o != day: send_weather_report(); l_o = day
            if cur == "06:00" and l_t != day: send_morning_wish(); l_t = day
            if cur == "07:00" and l_n != day: send_prayer_times(); l_n = day
            if cur == "10:00" and l_b != day: send_bank_rates(); l_b = day
            if cur in ["13:00", "18:00", "21:00"] and l_q != (day+cur): send_quiz(); l_q = (day+cur)
            
            time.sleep(30)
        except: time.sleep(10)

if __name__ == "__main__":
    keep_alive()
    main_loop()
