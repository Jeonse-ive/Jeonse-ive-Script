import pandas as pd

# ▼ 1. CSV 파일 불러오기
df = pd.read_csv("downloads/fraud/total_crime_by_area.csv")

# ▼ 2. 한글 → 영어 매핑 정의
gu_map = {
    "강남구": "Gangnam-gu", "강동구": "Gangdong-gu", "강북구": "Gangbuk-gu", "강서구": "Gangseo-gu",
    "관악구": "Gwanak-gu", "광진구": "Gwangjin-gu", "구로구": "Guro-gu", "금천구": "Geumcheon-gu",
    "노원구": "Nowon-gu", "도봉구": "Dobong-gu", "동대문구": "Dongdaemun-gu", "동작구": "Dongjak-gu",
    "마포구": "Mapo-gu", "서대문구": "Seodaemun-gu", "서초구": "Seocho-gu", "성동구": "Seongdong-gu",
    "성북구": "Seongbuk-gu", "송파구": "Songpa-gu", "양천구": "Yangcheon-gu", "영등포구": "Yeongdeungpo-gu",
    "은평구": "Eunpyeong-gu", "종로구": "Jongno-gu", "용산구": "Yongsan-gu", "중구": "Jung-gu",
    "중랑구": "Jungnang-gu"
}

city_map = {
    "서울시": "Seoul"
}

gu_to_city_kor = {
    "강남구": "서울시", "강동구": "서울시", "강북구": "서울시", "강서구": "서울시",
    "관악구": "서울시", "광진구": "서울시", "구로구": "서울시", "금천구": "서울시",
    "노원구": "서울시", "도봉구": "서울시", "동대문구": "서울시", "동작구": "서울시",
    "마포구": "서울시", "서대문구": "서울시", "서초구": "서울시", "성동구": "서울시",
    "성북구": "서울시", "송파구": "서울시", "양천구": "서울시", "영등포구": "서울시",
    "은평구": "서울시", "종로구": "서울시", "용산구": "서울시", "중구": "서울시",
    "중랑구": "서울시"
}

# ▼ 3. 지역 정보 전처리
def process_region(region):
    region = region.strip()
    if " " in region:
        parts = region.split()
        if len(parts) == 2:
            return parts[0], parts[1]
    elif region.endswith(("시", "군")):
        return region, "Total"
    elif region.endswith("구"):
        gu_kor = region
        city_kor = gu_to_city_kor.get(gu_kor)
        if city_kor:
            return city_kor, gu_kor
    return None, None

df[['city_kor', 'gu_kor']] = df['시군구'].apply(lambda x: pd.Series(process_region(x)))

# ▼ 4. 영어로 매핑
def map_to_eng(row):
    city_eng = city_map.get(row['city_kor'])
    gu_eng = "Total" if row['gu_kor'] == "Total" else gu_map.get(row['gu_kor'])
    return pd.Series([city_eng, gu_eng])

df[['city', 'gu']] = df.apply(map_to_eng, axis=1)

# ▼ 5. 최종 컬럼 구성 및 저장
df['damagedHouses'] = df['피해주택수']
df_final = df.dropna(subset=['city', 'gu'])[['city', 'gu', 'damagedHouses']]

df_final.to_csv("downloads/fraud/converted_crime_data.csv", index=False, encoding='utf-8-sig')
print("✅ 전처리 완료: downloads/converted_crime_data.csv 저장됨")