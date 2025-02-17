# Description: 영화 제목을 기반으로 KMDB API를 사용하여 영화 제목을 검색하고 CSV 파일을 업데이트
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
API_KEY = os.getenv("KMDB_API_KEY")

# 파일 경로 설정
INPUT_CSV = "final_boxoffice_data.csv"
OUTPUT_CSV = "chart/final_boxoffice_data.csv"
API_URL = "https://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp"

def read_movie_titles():
    """CSV 파일에서 영화 제목을 읽어 리스트로 반환"""
    if not os.path.exists(INPUT_CSV):
        print(f"오류: 입력 파일 {INPUT_CSV}이(가) 존재하지 않습니다.")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(INPUT_CSV, encoding="utf-8-sig")
        return df
    except Exception as e:
        print(f"CSV 파일 읽기 오류: {e}")
        return pd.DataFrame()

def fetch_movie_data(title):
    """KMDB API에서 영화 정보를 검색하여 반환"""
    params = {
        "collection": "kmdb_new2",
        "ServiceKey": API_KEY,
        "title": title,
        "listCount": 1,
        "detail": "Y"
    }
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "Data" in data and data["Data"] and "Result" in data["Data"][0]:
            movie = data["Data"][0]["Result"][0]
            genre = movie.get("genre", "장르 없음")
            poster_urls = movie.get("posters", "").split("|")
            poster_url = poster_urls[0] if poster_urls else "포스터 없음"
            return genre, poster_url
        
        print(f"⚠️ '{title}'에 대한 검색 결과가 없습니다.")
        return "검색 결과 없음", "검색 결과 없음"
    except requests.exceptions.RequestException as e:
        print(f"API 요청 오류 ({title}): {e}")
        return "오류 발생", "오류 발생"

def update_csv():
    """CSV 파일을 업데이트하여 장르 및 포스터 URL 추가"""
    df = read_movie_titles()
    if df.empty:
        print("❌ 처리할 영화 데이터가 없습니다.")
        return
    
    genres = []
    poster_urls = []
    for title in df["movieNm"]:
        genre, poster_url = fetch_movie_data(title)
        genres.append(genre)
        poster_urls.append(poster_url)
    
    df["genre"] = genres
    df["posterUrl"] = poster_urls
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"CSV 파일 업데이트 완료: {OUTPUT_CSV}")

if __name__ == "__main__":
    update_csv()
