import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import time
from urllib.parse import quote_plus
import os

def ex_tag(team, page):

    # 야구 구단(team)과 페이지(page)를 입력받아 그에 대한 링크들을 리스트로 추출
    url = (
        f"https://m.sports.naver.com/kbaseball/news"
        f"?sectionId=kbo"
        f"&team={team}"
        f"&page={page}"
    )
    # 기아 타이거즈(HT) / 삼성 라이온즈(SS) / 두산 베어스(OB) / SSG 랜더스(SK) / 한화 이글스(HH)
    # 키움 히어로즈(WO) / LG 트윈스(LG) / KT 위즈(KT) / 롯데 자이언츠(LT) / NC 다이노스(NC)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/110.0.0.0 Safari/537.36"
        )
    }
    
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    
    # 모든 <a> 태그 중, team=… 과 article 이 둘 다 포함된 href를 추출
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if f"team={team}" in href and "article" in href:
            links.append(href)
    return links
