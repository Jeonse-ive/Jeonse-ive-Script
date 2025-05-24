# -*- coding: utf-8 -*-
import subprocess
import os

base_path = os.path.dirname(os.path.abspath(__file__))
download_script = os.path.join(base_path, "download.py")
upload_script = os.path.join(base_path, "upload.py")

print("Starting download...")
subprocess.run(["python3", download_script], check=True)

print("Starting upload...")
subprocess.run(["python3", upload_script], check=True)

print("All tasks completed successfully.")
