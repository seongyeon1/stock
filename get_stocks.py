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
    df_stocks = list_df_stocks[0]
    return df_stocks

import requests
from bs4 import BeautifulSoup

def get_reports(ticker):
    res = requests.get(f'http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701')
    soup = BeautifulSoup(res.content, 'lxml')
    table = soup.find_all('table')
    df = pd.read_html(str(table))
    return df