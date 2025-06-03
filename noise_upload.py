import requests
from datetime import datetime
import os

# 날짜 설정 (작년 기준)
today = datetime.today()
last_year = today.year - 1
month = today.month
filename = f"noise_{last_year}_{month:02d}.xlsx"

# 파일 경로
file_path = os.path.abspath(f"downloads/{filename}")

# Spring Boot API 엔드포인트
url = "http://localhost:8080/api/readings/upload"  # 필요하면 도메인/포트 수정

# 업로드 요청
with open(file_path, 'rb') as f:
    files = {'noiseFile': (filename, f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    data = {'year': last_year}

    response = requests.post(url, files=files, data=data)

# 결과 출력
if response.status_code == 200:
    print("업로드 성공!")
else:
    print("업로드 실패!")
    print(f"응답 코드: {response.status_code}")
    print(response.text)
