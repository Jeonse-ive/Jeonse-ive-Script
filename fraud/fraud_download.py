from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
#팝업창 확인
from selenium.common.exceptions import UnexpectedAlertPresentException
import os
import time
import shutil
import tempfile
import uuid
import glob

# ▼ 파일 이름 설정 (지금은 날짜 기준으로 예시)
today = datetime.today()

# ▼ 다운로드 폴더 설정
download_dir = os.path.abspath("downloads/fraud")
os.makedirs(download_dir, exist_ok=True)

# ▼ 고유 Chrome 프로필 생성
user_data_dir = f"/tmp/chrome-profile-{uuid.uuid4()}"

# ▼ Chrome 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True
})

try:
    # ▼ 드라이버 실행
    driver = webdriver.Chrome(service=Service(), options=options)
    wait = WebDriverWait(driver, 15)

    # ▼ 페이지 접속
    driver.get("https://www.data.go.kr/data/15139145/fileData.do")

    # ▼ 다운로드 버튼 기다렸다가 클릭
    download_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@onclick, 'fileDetailObj.fn_fileDataDown')]")
        )
    )
    download_button.click()
    # 팝업 확인 처리
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("팝업 내용:", alert.text)
        alert.accept()  # 확인 버튼 누르기
        print("팝업 확인 완료.")
    except:
        print("팝업이 뜨지 않았습니다.")

    print("다운로드 시작됨...")
    downloaded_file = None
    # ▼ 다운로드 완료 대기
    timeout = time.time() + 30
    # 다운로드 완료 대기 중 .crdownload 제외
    while True:
        files = glob.glob(os.path.join(download_dir, "*"))
        completed_files = [f for f in files if not f.endswith(".crdownload")]
        if completed_files:
            downloaded_file = max(completed_files, key=os.path.getctime)
            break
        if time.time() > timeout:
            raise TimeoutError("다운로드 타임아웃 발생")
        time.sleep(1)

    if downloaded_file is None:
        raise RuntimeError("다운로드된 파일을 찾지 못했습니다.")

    # ▼ 확장자 감지 및 저장
    ext = os.path.splitext(downloaded_file)[1]
    filename = f"crime_data_{today.strftime('%Y%m%d')}{ext}"
    final_path = os.path.join(download_dir, filename)
    shutil.move(downloaded_file, final_path)

finally:
    try:
        driver.quit()
    except:
        pass
    shutil.rmtree(user_data_dir, ignore_errors=True)
