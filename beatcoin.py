import requests
from bs4 import BeautifulSoup
import pandas as pd

keyword = '비트코인'
url = f'https://search.naver.com/search.naver?where=news&query={keyword}'

# 1) 브라우저와 같은 User-Agent 헤더 추가
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers)
print("Status code:", response.status_code)      # 200 이 떠야 정상
soup = BeautifulSoup(response.text, 'html.parser')

# 2) 좀 더 구체적인 CSS 셀렉터 사용
#    (뉴스 제목은 <a class="news_tit"> 태그에 있음)
articles = soup.select("ul.list_news > li > div.news_wrap > a.news_tit")

print(f"Found {len(articles)} articles")

# 3) 빈 리스트 방어 처리
if not articles:
    # HTML 구조를 확인해 보고, 실제 어떤 클래스가 쓰였는지 살펴봅시다.
    print(soup.prettify()[:1000])
else:
    # 첫 번째 기사
    article = articles[0]
    print("첫 번째 기사 제목:", article.get_text(strip=True))

    # 데이터프레임 생성
    titles = [a.get_text(strip=True) for a in articles]
    df = pd.DataFrame(titles, columns=['title'])
    print(df.head())
