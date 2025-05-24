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

# 날짜 계산
today = datetime.today()
last_year = today.year - 1
month = today.month
filename = f"noise_{last_year}_{month:02d}.xlsx"

# 다운로드 폴더 및 저장 경로
download_dir = os.path.abspath("downloads")
os.makedirs(download_dir, exist_ok=True)
final_path = os.path.join(download_dir, filename)

# 임시 user-data-dir 경로 생성
user_data_dir = tempfile.mkdtemp()

# 크롬 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True
})

# 드라이버 실행
driver = webdriver.Chrome(service=Service(), options=options)
