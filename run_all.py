# -*- coding: utf-8 -*-
import subprocess
import os

base_path = os.path.dirname(os.path.abspath(__file__))
noise_download_script = os.path.join(base_path, "noise_download.py")
noise_upload_script = os.path.join(base_path, "noise_upload.py")

# Fraud
fraud_download_script = os.path.join(base_path, "fraud/fraud_download.py")
fraud_merge_script = os.path.join(base_path, "fraud/fraud_preprocessing_pageMerge.py")
fraud_convert_script = os.path.join(base_path, "fraud/fraud_preprocessing_page.py")
fraud_upload_script = os.path.join(base_path, "fraud/fraud_upload.py") 

print("Starting noise_download...")
subprocess.run(["python3", noise_download_script], check=True)

print("Starting noise_upload...")
subprocess.run(["python3", noise_upload_script], check=True)

print("▶️ fraud_download 실행...")
subprocess.run(["python3", fraud_download_script], check=True)

print("▶️ fraud_merge 실행...")
subprocess.run(["python3", fraud_merge_script], check=True)

print("▶️ fraud_convert 실행...")
subprocess.run(["python3", fraud_convert_script], check=True)

print("▶️ fraud_upload 실행...")
subprocess.run(["python", fraud_upload_script], check=True)

print("All tasks completed successfully.")
