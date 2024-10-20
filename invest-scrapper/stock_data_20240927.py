from types import NoneType
import requests, re, datetime, time, os
from bs4 import BeautifulSoup

import code_news
import comp_news_keyword as kk
import util.util_common as uc
import stock_info as sti

from enum import Enum


if __name__ == "__main__11": # ai 
    # local html save & load
    dd = dd = datetime.datetime.now().strftime('%Y%m%d')
    name = "삼성전자"
    code = "005930"

    def get_stock_html():
        url = getCodeUrl(code)
        response = requests.get(url)
        return response.text
     
    html = uc.file_cache_write(f"/test_data/stock_{name}_{code}-{dd}-source.txt", get_stock_html )
    


if __name__ == "__main__1": # ai 연동을 위한 데이터 가져오기.
    dd = dd = datetime.datetime.now().strftime('%Y%m%d')
    name = "삼성전자"
    code = "005930"
     
    current_folder_name = os.path.basename(os.getcwd())
    print("현재 폴더명:", current_folder_name)

    if current_folder_name == 'webCrawling':
        os.chdir('invest-scrapper')

    file_path = f"./test_data/stock_{name}_{code}-{dd}-source.txt"
    if not os.path.exists(file_path):
        uc.logger.debug(f"no file {file_path}")
        sd = StockDetail(1, name, code)
        key_text = sd.comp_issue_keys()

        # w 덮어쓰기, a 추가하기.
        with open(file_path, "w", encoding='utf-8') as file: 
            file.write(key_text)

        html_text = key_text
    else:
        uc.logger.debug(f"exists file {file_path}")
        with open(file_path, "r", encoding='utf-8') as file:
            html_text = file.read()

    # ai
    print(html_text)
    # keys, summerize = kk.summarize_and_extract_keywords(html_text)
    # print(keys)
    # print(summerize)


if __name__ == "__main__2": # 회사정보를 parsing 테스트 할때 사용하는 코드.

    current_folder_name = os.path.basename(os.getcwd())
    print("현재 폴더명:", current_folder_name)

    if current_folder_name == 'webCrawling':
        os.chdir('invest-scrapper')

    name = "삼성스팩6호"
    code = "425290"

    name = "삼성전자"
    code = "005930"

    file_path = f"./test_data/naver_{name}_{code}-{dd}-html.txt"
    html_text = ""

    if not os.path.exists(file_path):
        response = requests.get(f"https://finance.naver.com/item/main.naver?code={code}")
        # w 덮어쓰기, a 추가하기.
        with open(file_path, "w", encoding='utf-8') as file: 
            file.write(response.text)

        html_text = response.text
    else:
        with open(file_path, "r", encoding='utf-8') as file:
            html_text = file.read()

    sdso = StockDetailSoupObject(name, code, html_text)
    print(sdso)


if __name__ == "__main__": # ai 
    dd = dd = datetime.datetime.now().strftime('%Y%m%d')
    name = "삼성전자"
    code = "005930"
    sd = sti.StockDetail(1, name, code)

    # print("종가:", sd.today_price)

    # sd.to_md_file()
    sd.to_file_memo()
    # print(sd.to_file())
    # print(sd.to_md_file2())

