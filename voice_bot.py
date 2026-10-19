import os
import time
import threading
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. سيرفر الويب الوهمي لإرضاء Render ومنع خطأ المنفذ
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord Voice Bots are Alive!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# 2. دالة تشغيل البوت لكل حساب
def run_discord_bot(token, bot_name):
    voice_channel_url = "https://discord.com/channels/902273871133163530/1560296177033941014"

    if not token:
        print(f"[{bot_name}] خطأ: التوكن غير موجود!")
        return

    print(f"[{bot_name}] جاري بدء تشغيل المتصفح...")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--window-size=800,600")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://discord.com/login")
        print(f"[{bot_name}] جاري فتح ديسكورد...")
        time.sleep(5)

        script = f"""
        let token = "{token}";
        let iframe = document.createElement('iframe');
        document.body.appendChild(iframe);
        iframe.contentWindow.localStorage.setItem('token', JSON.stringify(token));
        document.body.removeChild(iframe);
        """
        driver.execute_script(script)
        print(f"[{bot_name}] تم حقن التوكن بنجاح!")

        driver.refresh()
        time.sleep(8)

        driver.get(voice_channel_url)
        print(f"[{bot_name}] جاري الانضمام إلى الفويس...")

        wait = WebDriverWait(driver, 40)
        join_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Join Voice')]"))
        )
        time.sleep(3)
        join_button.click()
        print(f"[{bot_name}] تم الانضمام بنجاح وفعل الاتصال الصوتي!")

        # إبقاء الحساب متصلاً للأبد
        while True:
            time.sleep(60)

    except Exception as e:
        print(f"[{bot_name}] حدث خطأ: {e}")
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    # تشغيل سيرفر الويب في الخلفية
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    # سحب التوكنات من متغيرات البيئة
    token1 = os.getenv("TOKEN_1")
    token2 = os.getenv("TOKEN_2")

    # تشغيل الحساب الأول في خيط منفصل
    if token1:
        t1 = threading.Thread(target=run_discord_bot, args=(token1, "البوت الأول"))
        t1.start()

    # تأخير بسيط لكي لا يضغطوا على السيرفر في نفس الميلي ثانية
    time.sleep(5)

    # تشغيل الحساب الثاني في خيط منفصل
    if token2:
        t2 = threading.Thread(target=run_discord_bot, args=(token2, "البوت الثاني"))
        t2.start()
