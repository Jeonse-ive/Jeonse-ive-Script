import requests
from datetime import datetime
import os

# 1. Calculate target year/month
today = datetime.today()
last_year = today.year - 1
month = today.month
filename = f"noise_{last_year}_{month:02d}.xlsx"

# 2. Set file path
file_path = os.path.abspath(f"downloads/{filename}")
print(f"[INFO] Target file to upload: {file_path}")

# 3. Set API endpoint
url = "http://localhost:8080/api/readings/upload"  # Change to prod URL if needed
print(f"[INFO] Uploading to URL: {url}")

# 4. Check if file exists
if not os.path.exists(file_path):
    print(f"[ERROR] File not found: {file_path}")
    exit(1)

# 5. Upload file
try:
    print("[INFO] Sending POST request with file...")
    with open(file_path, 'rb') as f:
        files = {
            'noiseFile': (filename, f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        data = {
            'year': last_year
        }

        response = requests.post(url, files=files, data=data)

    # 6. Print result
    if response.status_code == 200:
        print("[SUCCESS] Upload completed successfully.")
    else:
        print("[FAILURE] Upload failed.")
        print(f"[RESPONSE CODE] {response.status_code}")
        print(f"[RESPONSE TEXT] {response.text}")

except requests.exceptions.RequestException as e:
    print(f"[FATAL] Request failed due to network or server error: {e}")
except Exception as e:
    print(f"[FATAL] Unexpected error occurred: {e}")
