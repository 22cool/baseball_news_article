import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import time
import urllib.parse


#검색어로 URL 만들기

#requests.get("api주소")로 데이터 response 가져오기
response = requests.get('http://spartacodingclub.shop/sparta_api/seoulair')