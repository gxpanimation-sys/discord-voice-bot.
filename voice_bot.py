import os
import sys
import time
import asyncio
import threading
from flask import Flask
import discord
from discord.ext import commands

# إجبار إخراج الطباعة فوراً على Logs خادم Render
sys.stdout.reconfigure(line_buffering=True)

# 1. سيرفر الويب الوهمي لإرضاء Render ومنع خطأ المنفذ (Port)
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord Voice Bots are Alive!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# آيدي الروم الصوتي المراد الدخول إليه
VOICE_CHANNEL_ID = 1560296177033941014

def start_single_bot(token, bot_name):
    if not token:
        print(f"[{bot_name}] خطأ: التوكن غير موجود!")
        return

    # إنشاء حلقة أحداث (Event Loop) مستقلة لكل خيط
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bot = commands.Bot(command_prefix="!", self_bot=True, loop=loop)

    @bot.event
    async def on_ready():
        print(f"[{bot_name}] تم تسجيل الدخول بنجاح باسم: {bot.user}")
        
        # الانتظار قليلاً لضمان تحميل قنوات السيرفرات بالكامل
        await asyncio.sleep(3)
        
        try:
            channel = bot.get_channel(VOICE_CHANNEL_ID)
            if not channel:
                # محاولة بحث بديلة في كل السيرفرات المشتركة
                for guild in bot.guilds:
                    channel = guild.get_channel(VOICE_CHANNEL_ID)
                    if channel:
                        break

            if channel:
                await channel.connect()
                print(f"[{bot_name}] دخل الروم الصوتي بنجاح وتم تفعيل الاتصال!")
            else:
                print(f"[{bot_name}] خطأ: لم يتم العثور على الروم الصوتي! تأكد أن الحساب موجود في السيرفر الذي يضم الروم.")
        except Exception as e:
            print(f"[{bot_name}] خطأ أثناء الاتصال بالفويس: {e}")

    try:
        loop.run_until_complete(bot.start(token))
    except Exception as e:
        print(f"[{bot_name}] انقطع البوت أو حدث خطأ: {e}")

if __name__ == "__main__":
    # تشغيل سيرفر الويب في خلفية منفصلة
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()

    token1 = os.getenv("TOKEN_1")
    token2 = os.getenv("TOKEN_2")

    # تشغيل الحساب الثاني في خيط مستقل
    if token2:
        t2 = threading.Thread(target=start_single_bot, args=(token2, "البوت الثاني"), daemon=True)
        t2.start()

    time.sleep(3)

    # تشغيل الحساب الأول في الخيط الرئيسي
    if token1:
        start_single_bot(token1, "البوت الأول")
    else:
        while True:
            time.sleep(60)
