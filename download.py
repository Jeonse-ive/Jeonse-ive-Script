from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import time
import shutil

# 날짜 계산
today = datetime.today()
last_year = today.year - 1
month = today.month
filename = f"noise_{last_year}_{month:02d}.xlsx"

# 다운로드 폴더 및 저장 경로
download_dir = os.path.abspath("downloads")
os.makedirs(download_dir, exist_ok=True)
final_path = os.path.join(download_dir, filename)

# 크롬 옵션 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True
})

# 크롬 드라이버 실행
driver = webdriver.Chrome(service=Service(), options=options)
driver.get("https://www.noiseinfo.or.kr/noise/statistics.do")
wait = WebDriverWait(driver, 10)

# 연도 선택 (드롭다운 열고)
year_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "MM_measdt-button")))
year_dropdown.click()
time.sleep(1)

# 연도 항목 클릭 (텍스트 기반으로 선택)
year_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul#MM_measdt-menu li div")))
for item in year_items:
    if item.text.strip() == f"{last_year}년":
        item.click()
        break
time.sleep(1)

# 조회 버튼 클릭
search_button = driver.find_element(By.ID, "searchList")
search_button.click()
time.sleep(2)

# 엑셀 다운로드 클릭
excel_button = wait.until(EC.element_to_be_clickable((By.ID, "getStatisticsExcel")))
excel_button.click()

# 다운로드 대기 및 파일 이름 확인
print("엑셀 파일 다운로드 중...")
time.sleep(10)

# 가장 최근에 다운로드된 .xlsx 파일 찾기
downloaded_file = max(
    [os.path.join(download_dir, f) for f in os.listdir(download_dir) if f.endswith(".xlsx")],
    key=os.path.getctime
)

# 이름 변경 및 이동
shutil.move(downloaded_file, final_path)
print(f"다운로드 완료: {final_path}")

# 브라우저 종료
driver.quit()
