import os
import time
from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==================== الأمان أولاً ====================
# يتم سحب التوكنات بسلامة من إعدادات سحابة Render السرية
ACCOUNT_1_TOKEN = os.getenv("TOKEN_1")
ACCOUNT_2_TOKEN = os.getenv("TOKEN_2")

# رابط الروم الصوتي المراد الدخول إليه
VOICE_CHANNEL_URL = "https://discord.com/channels/902273871133163530/1560296177033941014"
# =========================================================

def run_bot(token, bot_name):
    if not token:
        print(f"[{bot_name}] خطأ: لم يتم العثور على التوكن في متغيرات البيئة!")
        return

    print(f"[{bot_name}] جاري بدء تشغيل المتصفح...")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--use-fake-ui-for-media-stream")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://discord.com/login")
        print(f"[{bot_name}] جاري فتح ديسكورد...")
        time.sleep(4)

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
        time.sleep(6)

        driver.get(VOICE_CHANNEL_URL)
        print(f"[{bot_name}] جاري الانتظار للانضمام إلى الفويس...")

        wait = WebDriverWait(driver, 35)
        join_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Join Voice')]"))
        )
        time.sleep(2)
        join_button.click()
        print(f"[{bot_name}] تم الانضمام بنجاح! الحساب متصل الآن.")

        while True:
            time.sleep(60)

    except Exception as e:
        print(f"[{bot_name}] حدث خطأ: {e}")

if __name__ == "__main__":
    p1 = Process(target=run_bot, args=(ACCOUNT_1_TOKEN, "الحساب الأول"))
    p2 = Process(target=run_bot, args=(ACCOUNT_2_TOKEN, "الحساب الثاني"))

    p1.start()
    p2.start()

    p1.join()
    p2.join()