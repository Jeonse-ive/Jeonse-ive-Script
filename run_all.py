import subprocess

# 1. 다운로드 실행
print("다운로드 시작...")
subprocess.run(["python", "download.py"], check=True)

# 2. 업로드 실행
print("업로드 시작...")
subprocess.run(["python", "upload.py"], check=True)

print("모든 작업 완료")
