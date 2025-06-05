# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import time
import shutil
import tempfile
import uuid
import glob

# 1. Date calculation
today = datetime.today()
last_year = today.year - 1
month = today.month
filename = f"noise_{last_year}_{month:02d}.xlsx"

# 2. Download folder (absolute path)
download_dir = "/home/ec2-user/Jeonse-ive-Script/downloads"
os.makedirs(download_dir, exist_ok=True)

# 3. Target file path
final_path = os.path.join(download_dir, filename)

# 3.2 Chrome profile directory
user_data_dir = f"/tmp/chrome-profile-{uuid.uuid4()}"

# 4. Chrome options
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True
})

try:
    print("[INFO] Launching Chrome WebDriver...")
    driver = webdriver.Chrome(service=Service(), options=options)
    wait = WebDriverWait(driver, 10)

    print("[INFO] Navigating to noiseinfo.or.kr...")
    driver.get("https://www.noiseinfo.or.kr/noise/statistics.do")

    # 6. Select year
    print(f"[INFO] Selecting year: {last_year}")
    year_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "MM_measdt-button")))
    year_dropdown.click()
    time.sleep(1)

    year_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul#MM_measdt-menu li div")))
    matched = False
    for item in year_items:
        if item.text.strip() == f"{last_year}년":
            print(f"[INFO] Clicking year item: {item.text.strip()}")
            item.click()
            matched = True
            break
    if not matched:
        raise Exception(f"[ERROR] Year {last_year} not found in dropdown")

    time.sleep(1)

    # 7. Click search and download Excel
    print("[INFO] Clicking search button...")
    driver.find_element(By.ID, "searchList").click()
    time.sleep(2)

    print("[INFO] Clicking Excel download button...")
    wait.until(EC.element_to_be_clickable((By.ID, "getStatisticsExcel"))).click()

    print("[INFO] Waiting for Excel file to download...")
    timeout = time.time() + 30
    downloaded_file = None
    while time.time() < timeout:
        xlsx_files = glob.glob(os.path.join(download_dir, "*.xlsx"))
        if xlsx_files:
            downloaded_file = max(xlsx_files, key=os.path.getctime)
            break
        time.sleep(1)

    if not downloaded_file:
        raise TimeoutError("[ERROR] File download timed out after 30 seconds.")

    # 8. Rename and move file
    shutil.move(downloaded_file, final_path)
    print(f"[SUCCESS] Download completed: {final_path}")

except Exception as e:
    print(f"[FATAL] {str(e)}")

finally:
    # 9. Clean up
    print("[INFO] Cleaning up browser and temp profile...")
    try:
        driver.quit()
    except Exception as e:
        print(f"[WARN] WebDriver quit failed: {e}")
    shutil.rmtree(user_data_dir, ignore_errors=True)
