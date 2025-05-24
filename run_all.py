# -*- coding: utf-8 -*-
import subprocess
import os

base_path = os.path.dirname(os.path.abspath(__file__))
download_script = os.path.join(base_path, "download.py")
upload_script = os.path.join(base_path, "upload.py")

print("📥 다운로드 시작...")
subprocess.run(["python3", download_script], check=True)

print("📤 업로드 시작...")
subprocess.run(["python3", upload_script], check=True)

print("✅ 모든 작업 완료")
