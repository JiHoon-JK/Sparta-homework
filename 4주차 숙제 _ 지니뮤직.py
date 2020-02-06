import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
# 사용자 계정을 등록 ("User-Agent"를 활용)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = 'https://www.genie.co.kr/chart/top200'
data = requests.get(url, headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

rank = 1
#  insert 할 데이터 셋트를 만듦
music_data = {
    'rank': rank,
    'image': '',
    'title': '',
    'artist': ''
}

for music in musics:
    #크롤링으로,  이미지 가져오기
    image = str(music.select_one('img').attrs['src']).replace('//','')
    # strip() : 띄워쓰기 다 붙여주는 함수 -> 문자열일때만 사용가능 ('str'을 씌워줘야함)
    title = str(music.select_one('td.info > a.title.ellipsis').text).strip()
    artist = music.select_one('a.artist.ellipsis').text

    music_data = {
        'rank': rank,
        'image': image,
        'title': title,
        'artist': artist
    }

    db.musics.insert_one(music_data)
    rank += 1

# 원활한 크롤링 Tip !
# 진행하다가 error가 발견될 경우
# 1. 에러가 나는 라인을 누르고 오른쪽 클릭 (Debug '4주차 숙제_지니뮤직' 클릭)
# 2. 가져온 url에서 크롤링이 정확하게 되는지 일일이 하나씩 쳐보기 -> 바로 칠때마다의 결과값들이 나옴
# 3. 원하는 값들을 찾을 때까지 검색 -> 해당하는 정보를 찾으면 붙여넣기
