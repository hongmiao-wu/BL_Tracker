import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_container_number(bl_number):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://www.msc.com/en/track-a-shipment")

        # 接受 cookies（如果弹出）
        try:
            wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        except:
            pass

        # 输入提单号
        input_box = wait.until(EC.presence_of_element_located((By.ID, "trackingNumber")))
        input_box.send_keys(bl_number)
        input_box.send_keys(Keys.ENTER)

        time.sleep(10)  # 等待页面渲染

        # 抓取 container numbers
        spans = driver.find_elements(By.XPATH, '//span[@x-text="container.ContainerNumber"]')
        return [span.text.strip() for span in spans if span.text.strip()]

    except Exception as e:
        print(f"❌ Error: {e}")
        return []

    finally:
        driver.quit()
