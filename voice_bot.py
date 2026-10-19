import os
import threading
from flask import Flask
import discord
from discord.ext import commands

# 1. سيرفر ويب وهمي لإرضاء منصة Render ومنع خطأ المنفذ
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord Voice Bots are Alive!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# 2. إعداد البوت الأول (الحساب الأول)
bot1 = commands.Bot(command_prefix="!", self_bot=True)
VOICE_CHANNEL_ID = 1560296177033941014

@bot1.event
async def on_ready():
    print(f"[البوت الأول] تم تسجيل الدخول بنجاح باسم: {bot1.user}")
    try:
        channel = bot1.get_channel(VOICE_CHANNEL_ID)
        if channel:
            await channel.connect()
            print("[البوت الأول] دخل الروم الصوتي بنجاح!")
        else:
            print("[البوت الأول] خطأ: لم يتم العثور على الروم الصوتي!")
    except Exception as e:
        print(f"[البوت الأول] خطأ أثناء الاتصال بالفويس: {e}")

# 3. إعداد البوت الثاني (الحساب الثاني)
bot2 = commands.Bot(command_prefix="!", self_bot=True)

@bot2.event
async def on_ready():
    print(f"[البوت الثاني] تم تسجيل الدخول بنجاح باسم: {bot2.user}")
    try:
        channel = bot2.get_channel(VOICE_CHANNEL_ID)
        if channel:
            await channel.connect()
            print("[البوت الثاني] دخل الروم الصوتي بنجاح!")
        else:
            print("[البوت الثاني] خطأ: لم يتم العثور على الروم الصوتي!")
    except Exception as e:
        print(f"[البوت الثاني] خطأ أثناء الاتصال بالفويس: {e}")

if __name__ == "__main__":
    # تشغيل سيرفر الويب في الخلفية
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    token1 = os.getenv("TOKEN_1")
    token2 = os.getenv("TOKEN_2")

    # تشغيل الحساب الثاني في خيط منفصل
    if token2:
        threading.Thread(target=lambda: bot2.run(token1 if False else token2, bot=False)).start()

    # تشغيل الحساب الأول
    if token1:
        bot1.run(token1, bot=False)
