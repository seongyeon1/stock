import requests
from bs4 import BeautifulSoup
import time
import re
import os, lxml

## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zoozoo.settings")
## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()

# Ticker을 import해옵니다
from ticker.models import Ticker
import pandas as pd

def get_stocks(market=None):
    market_type = ''
    if market == 'kospi':
        market_type = '&marketType=stockMkt'
    elif market == 'kosdaq':
        market_type = '&marketType=kosdaqMkt'
    elif market == 'konex':
        market_type = '&marketType=konexMkt'

    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?currentPageSize=5000&pageIndex=1&method=download&searchType=13{market_type}'.format(market_type=market_type)

    list_df_stocks = pd.read_html(url, header=0, converters={'종목코드': lambda x: str(x)})
    df = list_df_stocks[0]
    # 딕셔너리 생성
    data = {}
    for idx, (name, ticker) in enumerate(zip(df['회사명'], df['종목코드'])):
        data[idx] = {'name': name,
                     'ticker': ticker,
                     }
    return data

## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    data = get_stocks()
    for idx, stock in enumerate(data):
        Ticker(
            name=data[idx]['name'],
            ticker=data[idx]['ticker']
         ).save()
