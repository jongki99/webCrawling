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
import util.util_common as uc


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
def save_local_data(company_name, company_object):
    print(company_name, company_object)
    source_dir = f"{uc.base_data_path}/company_name/"
    file_name = f"{source_dir}/name_{company_name}.json"

    if not os.path.exists(source_dir):
        os.makedirs(source_dir)

    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(company_object, file, indent=4, ensure_ascii=False)


def get_local_data(company_name):
    parsed_json = None
    source_dir = f"{uc.base_data_path}/company_name/"
    file_name = f"{source_dir}/name_{company_name}.json"

    if not os.path.exists(source_dir):
        os.makedirs(source_dir)

    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            parsed_json = json.loads(content)

    return parsed_json

def get_invest_code(company_name):
    company_json = get_local_data(company_name)
    if company_json:
        return company_json['code']

    print(f"get naver, company name ={company_name}")
    enName = urllib.parse.quote(company_name)
    url = f"https://ac.stock.naver.com/ac?q={enName}&target=index%2Cstock%2Cmarketindicator"
    response = requests.get(url)

    parsed_json = json.loads(response.text)

    # 주어진 company_name과 일치하는 기업의 code 조회
    company_code = None
    for company in parsed_json['items']:
        if company['name'] == company_name:
            save_local_data(company_name, company)
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

def read_csv_file_kw(file_path):
    stockList = []

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

"""
    string 입력을 받아서...
    replaces 대상을 "" 으로 replace.
    adds 대상을 trim 후 "," + str 처리 하는 함수.
    모두 변환 처리를 한 후에 해당 값을 리턴.
"""
def kiwoomCopyReplace(kiwoom_str):
    replaces = []
    replaces.append("""분	신	종목명	거래대금	현재가	등락률	거래량	종목코드
""")
    replaces.append('''
			""	""	""	""	''')
    replaces.append("""신		""")
    replaces.append("""경		""")
    replaces.append("""증		""")
    replaces.append("""주		""")
    replaces.append("""열		""")
    replaces.append("""		""")

    adds = []
    adds.append("2024")
    adds.append('	"')
    adds.append("	'")

    trans_str = kiwoom_str

    # replaces의 각 요소에 대해 문자열에서 제거
    for replace_str in replaces:
        trans_str = trans_str.replace(replace_str, "")
        print("--------------------------------------------"+replace_str+"""
"""+trans_str)

     # adds의 각 요소에 대해 문자열을 추가 (trim 후 ",str" 형식으로 추가)
    for add_str in adds:
        trans_str = trans_str.replace(add_str, ","+add_str.strip())
        # trans_str = ",".join([line.strip() + add_str for line in trans_str.splitlines() if line.strip()])
        print("--------------------------------------------"+add_str+"""
"""+trans_str)

    return trans_str

stocks = f"""
분	신	종목명	거래대금	현재가	등락률	거래량	종목코드
,보유
비에이치
아이씨티케이
원준
KT&G
삼성전자
하이닉스
,관심.
노을

2024-10-17. 상승인가?							
신		제일일렉트릭	"31,644"	"10,110"	"4.44"	"3,131,386"	'199820
신		한독	"112,085"	"16,420"	"11.85"	"6,718,528"	'002390
		제넥신	"213,907"	"9,350"	"14.44"	"23,167,065"	'095700
신		일진전기	"104,566"	"26,100"	"16.26"	"4,174,733"	'103590
신		모비스	"176,584"	"3,855"	"23.56"	"45,372,677"	'250060
		셀비온	"445,188"	"26,800"	"29.78"	"18,596,914"	'308430
신		이엔셀	"183,735"	"24,050"	"20.67"	"7,839,053"	'456070
신		우진엔텍	"120,504"	"18,460"	"10.74"	"6,076,471"	'457550
신		에이직랜드	"70,559"	"36,850"	"29.98"	"2,114,179"	'445090


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

    file_path = os.path.join(path, f"company_name_csv/s{dd}-v4.csv")

    print(file_path)

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        kiwoom = kiwoomCopyReplace(stocks)
        file.write(kiwoom)

    read_csv_file_kw(file_path)


    ### 코스닥 30, 코스피 10
    ### 한번에 실행... 음... 뭐로 나누지?
    stocks = rl.getTop40()

    for index, stock in enumerate(stocks):
        stock.print()
        stock.save_md()

    rl.merge_txt_order_md(stocks)
    rl.merge_txt_order_sum(stocks)


if __name__ == "__main__kiwoomFormat":

    result = kiwoomCopyReplace(stocks)
    print(result)
