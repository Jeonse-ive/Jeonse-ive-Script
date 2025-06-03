import os
import pandas as pd

# 현재 스크립트 기준 상위 폴더 탐색
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_dir, "downloads", "fraud", "total_crime_by_area.csv")

# 읽기
df = pd.read_csv(csv_path, encoding='utf-8-sig')
print("✅ CSV 로드 성공")
print(df.head())

# ▼ 2. 한글 → 영어 매핑 정의
gu_map = {
    "강남구": "Gangnam-gu", "강동구": "Gangdong-gu", "강북구": "Gangbuk-gu", "강서구": "Gangseo-gu",
    "관악구": "Gwanak-gu", "광진구": "Gwangjin-gu", "구로구": "Guro-gu", "금천구": "Geumcheon-gu",
    "노원구": "Nowon-gu", "도봉구": "Dobong-gu", "동대문구": "Dongdaemun-gu", "동작구": "Dongjak-gu",
    "마포구": "Mapo-gu", "서대문구": "Seodaemun-gu", "서초구": "Seocho-gu", "성동구": "Seongdong-gu",
    "성북구": "Seongbuk-gu", "송파구": "Songpa-gu", "양천구": "Yangcheon-gu", "영등포구": "Yeongdeungpo-gu",
    "은평구": "Eunpyeong-gu", "종로구": "Jongno-gu", "용산구": "Yongsan-gu", "중랑구": "Jungnang-gu",
    # 경기 고양시
    "덕양구": "Deogyang-gu", "일산동구": "Ilsandong-gu", "일산서구": "Ilsanseo-gu",
    # 경기 성남시
    "분당구": "Bundang-gu", "수정구": "Sujeong-gu", "중원구": "Jungwon-gu",
    # 경기 수원시
    "권선구": "Gwonseon-gu", "영통구": "Yeongtong-gu", "장안구": "Jangan-gu", "팔달구": "Paldal-gu",
    # 경기 용인시
    "기흥구": "Giheung-gu", "수지구": "Suji-gu", "처인구": "Cheoin-gu",
    # 경기 안산시
    "단원구": "Danwon-gu", "상록구": "Sangnok-gu",
    # 경기 안양시
    "동안구": "Dongan-gu", "만안구": "Manan-gu",
    # 부산광역시
    "해운대구": "Haeundae-gu", "금정구": "Geumjeong-gu", "부산진구": "Busanjin-gu","수영구": "Suyeong-gu",
    # 대구광역시
    "수성구": "Suseong-gu", "달서구": "Dalseo-gu",
    # 인천시
    "계양구": "Gyeyang-gu", "남동구": "Namdong-gu", "부평구": "Bupyeong-gu", 
    "연수구": "Yeonsu-gu", "미추홀구": "Michuhol-gu",
    # 광주시
    "광산구": "Gwangsan-gu",
    # 대전시
    "유성구": "Yuseong-gu",
    "연제구": "Yeonje-gu",
    "영도구": "Yeongdo-gu",
    "사상구": "Sasang-gu",
    "사하구": "Saha-gu",
    "동래구": "Dongnae-gu",
    "성산구": "Seongsan-gu",
    "덕진구": "Deokjin-gu",
    "완산구": "Wansan-gu"
}

city_map = {
    "서울시": "Seoul",
    "고양시": "Goyang",
    "성남시": "Seongnam",
    "수원시": "Suwon",
    "용인시": "Yongin",
    "안산시": "Ansan",
    "안양시": "Anyang",
    "부산시": "Busan",
    "대구시": "Daegu",
    "인천시": "Incheon",
    "광주시": "Gwangju",
    "대전시": "Daejeon",
    "전주시":"Jeonju",
    "창원시":"Changwon",
    #Total처리 대상
    "가평군": "Gapyeong",
    "강릉시": "Gangneung",
    "광주시": "GwangjuGyeonggi",  # ← 광역시 광주와 구분 필요!
    "김포시": "Gimpo",
    "나주시": "Naju",
    "세종시": "Sejong",
    "여주시": "Yeoju",
    "원주시": "Wonju",
    "화성시": "Hwaseong",
    "양평군": "Yangpyeong",
    "거제시":"Geoje",
    "경산시": "Gyeongsan",
    "경주시": "Gyeongju",
    "곡성군": "Gokseong",
    "과천시": "Gwacheon",
    "광명시": "Gwangmyeong",
    "광양시": "Gwangyang",
    "구리시": "Guri",
    "구미시": "Gumi",
    "군포시": "Gunpo",
    "김천시": "Gimcheon",
    "김해시": "Gimhae",
    "남양주시": "Namyangju",
    "남원시": "Namwon",
    "논산시": "Nonsan",
    "당진시": "Dangjin",
    "목포시": "Mokpo",
    "무안군": "Muan",
    "보령시": "Boryeong",
    "보은군": "Boeun",
    "서귀포시": "Seogwipo",
    "서산시": "Seosan",
    "서천군": "Seocheon",
    "속초시": "Sokcho",
    "순천시": "Suncheon",
    "시흥시": "Siheung",
    "아산시": "Asan",
    "안성시": "Anseong",
    "양산시": "Yangsan",
    "양주시": "Yangju",
    "여수시": "Yeosu",
    "예천군": "Yecheon",
    "오산시": "Osan",
    "음성군": "Eumseong",
    "의왕시": "Uiwang",
    "의정부시": "Uijeongbu",
    "이천시": "Icheon",
    "익산시": "Iksan",
    "제주시": "Jeju",
    "증평군": "Jeungpyeong",
    "진주시": "Jinju",
    "칠곡군": "Chilgok",
    "파주시": "Paju",
    "평택시": "Pyeongtaek",
    "포천시": "Pocheon",
    "하남시": "Hanam",
    "홍천군": "Hongcheon",
    "화순군": "Hwasun"
}

gu_to_city_kor = {
    "강남구": "서울시", "강동구": "서울시", "강북구": "서울시", "강서구": "서울시",
    "관악구": "서울시", "광진구": "서울시", "구로구": "서울시", "금천구": "서울시",
    "노원구": "서울시", "도봉구": "서울시", "동대문구": "서울시", "동작구": "서울시",
    "마포구": "서울시", "서대문구": "서울시", "서초구": "서울시", "성동구": "서울시",
    "성북구": "서울시", "송파구": "서울시", "양천구": "서울시", "영등포구": "서울시",
    "은평구": "서울시", "종로구": "서울시", "용산구": "서울시", "중랑구": "서울시",
    # 고양시
    "덕양구": "고양시", "일산동구": "고양시", "일산서구": "고양시",
    # 성남시
    "분당구": "성남시", "수정구": "성남시", "중원구": "성남시",
    # 수원시
    "권선구": "수원시", "영통구": "수원시", "장안구": "수원시", "팔달구": "수원시",
    # 용인시
    "기흥구": "용인시", "수지구": "용인시", "처인구": "용인시",
    # 안산시
    "단원구": "안산시", "상록구": "안산시",
    # 안양시
    "동안구": "안양시", "만안구": "안양시",
    # 부산시
    "해운대구": "부산시", "금정구": "부산시", "부산진구": "부산시","수영구": "부산시", "연제구": "부산시",
    "영도구": "부산시", "사상구": "부산시", "사하구": "부산시", "동래구": "부산시",
    # 대구시
    "수성구": "대구시", "달서구": "대구시",
    # 인천시
    "계양구": "인천시", "남동구": "인천시", "부평구": "인천시",
    "연수구": "인천시", "미추홀구": "인천시",
    # 광주시
    "광산구": "광주시",
    # 대전시
    "유성구": "대전시",
    "성산구": "창원시",
    "덕진구": "전주시",
    "완산구": "전주시"
    
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

# total_crime_by_area.csv와 동일한 디렉토리에 저장
save_path = os.path.join(os.path.dirname(csv_path), "converted_crime_data.csv")
df_final.to_csv(save_path, index=False, encoding='utf-8-sig')
print(f"✅ 전처리 완료: {save_path} 저장됨")