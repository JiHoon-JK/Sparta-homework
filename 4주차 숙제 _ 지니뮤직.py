import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

rank = 1
for music in musics:
    # movie 안에 a 가 있으면,
    a_tag = music.select_one('td.info > a.title.ellipsis')
    if a_tag is not None:
        music_title = a_tag.text
        singer = music.select_one('a.artist.ellipsis').text
        # a의 text를 찍어본다.
        doc = {
            'rank': rank,
            'music_title': music_title,
            'singer': singer
        }
        db.musics.insert_one(doc)
        rank += 1
