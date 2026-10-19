import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# سحب التوكنات من متغيرات البيئة السرية
ACCOUNT_1_TOKEN = os.getenv("TOKEN_1")
ACCOUNT_2_TOKEN = os.getenv("TOKEN_2")

# رابط الروم الصوتي المراد الدخول إليه
VOICE_CHANNEL_URL = "https://discord.com/channels/902273871133163530/1560296177033941014"

def login_and_join(token, bot_name):
    if not token:
        print(f"[{bot_name}] خطأ: التوكن غير موجود!")
        return

    print(f"[{bot_name}] جاري بدء تشغيل المتصفح...")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--use-fake-ui-for-media-stream")
    # تقليص استهلاك الذاكرة لمنع الـ Out of Memory
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,720")

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
        print(f"[{bot_name}] تم الانضمام بنجاح وفعل الاتصال!")

        # إبقاء المتصفح شغال في الخلفية لهذا الحساب
        while True:
            time.sleep(60)

    except Exception as e:
        print(f"[{bot_name}] حدث خطأ: {e}")
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    # تشغيل الحساب الأول ثم الحساب الثاني بشكل متتابع لمنع استهلاك الذاكرة المفاجئ
    print("بدء تشغيل الحساب الأول...")
    login_and_join(ACCOUNT_1_TOKEN, "الحساب الأول")
