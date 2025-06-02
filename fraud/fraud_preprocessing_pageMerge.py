import os
import glob
import re
import pandas as pd

# 1. 가장 최신 crime_data_YYYYMMDD.xlsx 파일 자동 탐색
download_dir = "downloads/fraud"
xlsx_files = glob.glob(os.path.join(download_dir, "crime_data_*.xlsx"))

def extract_date_from_filename(filename):
    match = re.search(r"crime_data_(\d{8})\.xlsx", os.path.basename(filename))
    return match.group(1) if match else None

latest_file = None
if xlsx_files:
    dated_files = [
        (extract_date_from_filename(f), f)
        for f in xlsx_files
        if extract_date_from_filename(f)
    ]
    if dated_files:
        latest_file = sorted(dated_files, reverse=True)[0][1]

if latest_file is None:
    raise FileNotFoundError("crime_data_YYYYMMDD.xlsx 형식의 파일을 찾을 수 없습니다.")

print(f"✅ 최신 파일 선택됨: {latest_file}")

# 2. 모든 시트 불러오기
sheets = pd.read_excel(latest_file, sheet_name=None)

# 3. 병합 + 시군구 기준 합산
df_list = []
for df in sheets.values():
    df = df[['시군구', '피해주택수']]  # 필요한 열만 추출
    df_list.append(df)

merged_df = pd.concat(df_list, ignore_index=True)
grouped_df = merged_df.groupby('시군구', as_index=False).sum()

# 4. 저장
output_path = os.path.join(download_dir, "total_crime_by_area.csv")
grouped_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"✅ 최종 결과 저장 완료: {output_path}")
