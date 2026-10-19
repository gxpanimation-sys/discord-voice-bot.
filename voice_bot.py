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

# 1. إنشاء سيرفر ويب وهمي لإرضاء منصة Render ومنع خطأ المنفذ (Port)
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord Voice Bot is Alive!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# 2. دالة تشغيل البوت عبر كروم الخفيف
def run_discord_bot():
    token = os.getenv("TOKEN_1") # تشغيل الحساب الأول لضمان عدم استهلاك الذاكرة
    voice_channel_url = "https://discord.com/channels/902273871133163530/1560296177033941014"

    if not token:
        print("[Bot] خطأ: التوكن غير موجود!")
        return

    print("[Bot] جاري بدء تشغيل متصفح كروم الخفيف...")
    
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
        print("[Bot] جاري فتح ديسكورد...")
        time.sleep(4)

        script = f"""
        let token = "{token}";
        let iframe = document.createElement('iframe');
        document.body.appendChild(iframe);
        iframe.contentWindow.localStorage.setItem('token', JSON.stringify(token));
        document.body.removeChild(iframe);
        """
        driver.execute_script(script)
        print("[Bot] تم حقن التوكن بنجاح!")

        driver.refresh()
        time.sleep(6)

        driver.get(voice_channel_url)
        print("[Bot] جاري الانتظار للانضمام إلى الفويس...")

        wait = WebDriverWait(driver, 35)
        join_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Join Voice')]"))
        )
        time.sleep(2)
        join_button.click()
        print("[Bot] تم الانضمام بنجاح وفعل الاتصال الصوتي!")

        # إبقاء السكربت شغّالاً
        while True:
            time.sleep(60)

    except Exception as e:
        print(f"[Bot] حدث خطأ: {e}")
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    # تشغيل سيرفر الويب في خلفية منفصلة
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    # تشغيل بوت ديسكورد
    bot_thread = threading.Thread(target=run_discord_bot)
    bot_thread.start()
    bot_thread.join()
