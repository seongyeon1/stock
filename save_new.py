import requests
from bs4 import BeautifulSoup
import time
import re
import os

## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zoozoo.settings")
## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()

# NewsData를 import해옵니다
from news.models import News
from ticker.models import Ticker

def parse_news(name):
    url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={name}'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    # 해당 주식에 관한 뉴스기사 10개 크롤링하기
    table = soup.find('ul', { 'class' : 'list_news' })
    li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
    area_list = [li.find('div', {'class' : 'news_area'}) for li in li_list]
    a_list = [area.find('a', {'class':'news_tit'}) for area in area_list]

    # 뉴스날짜 뽑아내기
    #news_dts = [area.find('span', {'class':'info'}).get_text() for area in area_list]
    # 정규식을 이용해 뉴스날짜 뽑아내기
    news_dts = [area.find_all('span', {'class': 'info'}) for area in area_list]
    dts = [news_dt[-1].get_text() for news_dt in news_dts]
    d = re.compile('\d{4}.\d{2}.\d{2}.')
    releases = [time.strftime('%Y-%m-%d', time.localtime(time.time())) if d.match(dt) == None else dt.rstrip('.').replace('.', '-')
     for dt in dts]

    # 뉴스내용 미리보기
    contents = [area.find('a', {'class':'api_txt_lines dsc_txt_wrap'}).get_text() for area in area_list]

    # 딕셔너리 생성
    news = {}
    for idx, (n, content, release) in enumerate(zip(a_list, contents, releases)):
        news[idx] = {'title' : n.get('title'),
                      'content' : content,
                      'url' : n.get('href'),
                     'released_date' : release,
                     }
    return news

## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    tickers = Ticker.objects.all()
    for ticker in tickers:
        news_dict = parse_news(name=ticker.name)
        for news in news_dict.values():
            #News.ticker.add(Ticker.objects.get(id=1))
            News(title=news['title'],
                 content=news['content'],
                 link=news['url'],
                 released_date=news['released_date'].rstrip('.').replace('.','-'),
                 ticker=ticker
                 ).save()