# fraud_upload.py
import requests
import os

# 업로드할 파일 경로
file_path = os.path.abspath("downloads/fraud/converted_crime_data.csv")

# 서버 업로드 엔드포인트 (필요시 수정)
url = "http://localhost:8080/api/fraud/upload"

# 업로드 요청
with open(file_path, 'rb') as f:
    files = {'fraudFile': (os.path.basename(file_path), f, 'text/csv')}
    response = requests.post(url, files=files)

# 응답 확인
if response.status_code == 200:
    print("✅ Fraud 데이터 업로드 성공!")
else:
    print("전세사기 업로드 실패!")
    print("응답 코드:", response.status_code)
    print(response.text)