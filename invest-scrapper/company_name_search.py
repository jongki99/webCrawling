"""
네이버 증권 홈.
https://finance.naver.com/sise/

검색창에 쿼리...

https://ac.stock.naver.com/ac?q=https%3A%2F%2Ffinance.naver.com%2Fsise%2F&target=index%2Cstock%2Cmarketindicator

https://ac.stock.naver.com/ac?q=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%901&target=index%2Cstock%2Cmarketindicator


q=? urlEncoder 가 있나?
&target=index,marketindicator : 이건 상수로 입력. 혹시 모르니.

jsonParser 가 있겠지?

회사명으로 검색해서 코드를 가져온다.

"""
import requests, re, datetime, time, os
from bs4 import BeautifulSoup

import csv
import json
import urllib.parse

import stock_info as st
import ranking_list as rl


def find_company_code(json_data, company_name):
    # JSON 데이터 파싱
    data = json.loads(json_data)
    
    # 주어진 company_name과 일치하는 기업의 code 조회
    company_code = None
    for company in data:
        if company['name'] == company_name:
            company_code = company['code']
            break
    
    return company_code


def get_invest_code(company_name):
    print(f"company name ={company_name}")
    enName = urllib.parse.quote(company_name)
    url = f"https://ac.stock.naver.com/ac?q={enName}&target=index%2Cstock%2Cmarketindicator"
    response = requests.get(url)

    parsed_json = json.loads(response.text)

    # 주어진 company_name과 일치하는 기업의 code 조회
    company_code = None
    for company in parsed_json['items']:
        if company['name'] == company_name:
            company_code = company['code']
            break
    
    return company_code


    # print(parsed_json)

def read_csv_file(file_path):
    stockList = []
#    try:
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue # 공백행 스킵.
            elif not row[0]:
                continue # 첫행이 회사명.

            name = row[0]
            code = get_invest_code(name)
            print(f"company={name} code={code}")

            if code:
                stock = st.StockInfo(2, name, code)
                stockList.append(stock)
    if stockList:
        
        for index, stock in enumerate(stockList):
            stock.print()
            stock.save_md2()

        rl.merge_txt_order_md2(stockList)

        rl.merge_txt_order_sum(stockList, 2)

        rl.merge_txt_order_sum2(stockList, 2)
        # todo ai 는 일단 제외하자... 볼수가 없네. 개선도 못하고... 방법도...


#    except FileNotFoundError:
#        print("파일을 찾을 수 없습니다.")
#    except Exception as e:
#        print("오류 발생:", e, e)
stocks_old = f"""
, 이 목록 관리를 잘하는 것도 중요한데...
, 이렇게 보면 정리 할게 엄청많다. 어떤 녀석이 내마음에 들지... 골르고 골라보자.

"""

stocks = f"""
엘앤에프,	"78,179"	"119,400"	"11.07"	"670,387"	'066970
시프트업,	"53,671"	"64,500"	"14.77"	"859,859"	'462870
"""


if __name__ == "__main__":
    # file_path = input("CSV 파일 경로를 입력하세요: ")
    nn = datetime.datetime.now()
    # nn = nn - datetime.timedelta(days=1) # 하루전.
    dd = nn.strftime('%Y%m%d')
    
    current_folder_name = os.path.basename(os.getcwd())
    print("현재 폴더명:", current_folder_name)

    if current_folder_name == 'webCrawling':
        os.chdir('invest-scrapper')

    path = os.getcwd()

    file_path = os.path.join(path, f"company_name_csv/s{dd}-2.csv")

    print(file_path)

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        file.write(stocks)

    read_csv_file(file_path)


    ### 코스닥 30, 코스피 10
    ### 한번에 실행... 음... 뭐로 나누지?
    # stocks = rl.getTop40()

    # for index, stock in enumerate(stocks):
    #     stock.print()
    #     stock.save_md()

    # rl.merge_txt_order_md(stocks)
    # rl.merge_txt_order_sum(stocks)

