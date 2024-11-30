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

# re
re_try = True ### 당일 top not retry.

stocks = f"""
윙입푸드
루닛, 시총. 2조???
셀바스AI, 시총. 4천억.
"""

re_try = False ### 당일 top.

stocks = f"""
분	신	종목명	거대금	현재가	등락률	거래량	종목코드
,보유
KT&G
아이씨티케이
하이젠알앤엠
,공장 - 좀 길게... 100% 이상을 보고... 일단 관찰 부터...
태성
, 관찰. ( 트럼프, 재건주. )

, 테마. 우크라. 재건.
삼부토건, 급상승 - 급락중(1120), 5일선 돌파를 봐봐? 무리일것 같은데... 코드닥이 좋지 않기도 하고...
대동
한미글로벌	"221,961"	"19,740"	"25.81"	"11,741,789"	'053690
대동기어	"62,753"	"10,800"	"29.96"	"6,533,746"	'008830

, 테마. 우크라. 전쟁. -- 이쪽은 트럼프로 재외.

, 테마. 전기, 전선, ... 우크라 재건.
LS ELECTRIC
가온전선
, 테마. 바이오 - 는 어렵다.
, 테마. 바이오, AI 는 아직... 일단은 추세 시작인 듯한데... 셀바스가 대장인가? 일단 분산? 머스크, AI의료진단. 이게 영향도가 있나? 일단 이슈기는 한데... 테마로써는 애매...
루닛, 시총. 2조???
셀바스AI, 시총. 4천억.
, 테마. 배터리는 모르겠는데... 분야별로 조금씩.
, 테마. 양자컴퓨터. 양자보안. 팁페이크 등...
아이씨티케이
, 뭔가 있는데... 이름을 매번... -_-;;
, 테마. 원자력.
, 비에이치아이, 너무 가서 추가로 가기가... 일단 두고 보는 걸로...
, 테마. 잠수함. 조선.
, 성광벤드, 아직 좀 살아있나? 일단 전쟁 테마는 죽었으니..
, 테마. 대북? 통일교.
, 일신석재, (007110), 대북 이슈는 트럼프...?? 이건..
, 테마. STO 토큰 증권. 일단 때가 지났고, 주도 테마로는 미약.
, 핑거

2024-11-26. 화.
, 코콤, cctv, 드론... 흠... 이것 만으론...
, 제이씨현시스템, gpu 매입주관사? 매출은 많겠는데... 4조 라...
, 비보존 제약, 기존 오피란제린. FDA 승인 기대감. 트럼프.
, 에이럭스 신규, 로봇교육, 로봇드론.
, 테마. 드론은 좀...
2024-11-27. 수.							
, 일신석재	"126,228"	"1,900"	"14.94"	"64,332,193"	'007110 -- 남북 경협???
폴라리스AI	"119,795"	"2,925"	"30.00"	"44,279,502"	'039980 -- 우크라 재건주??? 이거 4조..
, 폴라리스오피스	"251,859"	"6,890"	"17.78"	"37,753,853"	'041020 -- AI 기반 문서 솔루션
이스트소프트	"156,772"	"21,200"	"28.02"	"7,979,831"	'047560 -- AI, 딥파인.
, 아난티	"81,017"	"5,770"	"12.26"	"14,038,847"	'025980 -- 대북주.
, M83	"92,570"	"15,320"	"24.76"	"6,283,274"	'476080 -- 신규, 중.일 서 신규프로젝트 ???
, 나이벡	"50,722"	"16,110"	"14.74"	"3,074,921"	'138610 -- 텝타이드, 비만약... 지난 뉴스.
, 이오플로우	"75,362"	"9,300"	"23.67"	"8,385,354"	'294090 -- 인슐린 패치. 지난 뉴스.
, 차이커뮤니케이션	"50,782"	"12,770"	"29.91"	"4,364,576"	'351870 -- AI 차르직
자람테크놀로지	"56,770"	"35,150"	"27.59"	"1,696,656"	'389020 -- AGI

2024-11-28. 목.							
신		DS단석	"280,347"	"57,000"	"19.50"	"5,082,385"	'017860
신		넥스트바이오메디컬	"219,368"	"43,850"	"17.88"	"4,875,215"	'389650
신		이엔셀	"129,061"	"16,930"	"17.33"	"7,661,119"	'456070
신		에스오에스랩	"132,278"	"9,610"	"17.63"	"14,836,184"	'464080
신		셀트리온제약	"76,898"	"58,300"	"10.00"	"1,311,442"	'068760
증		금양	"93,093"	"31,850"	"15.82"	"2,986,841"	'001570
		에어레인	"67,955"	"13,220"	"25.43"	"5,386,738"	'163280
신		인스피언	"59,304"	"10,540"	"29.96"	"6,023,603"	'465480

분	신	종목명	거래대금	현재가	등락률	거래량	종목코드
2024-11-29. 금. 장이애매허내							
		LK삼양	"226,503"	"3,470"	"26.64"	"68,668,481"	'225190
신		자람테크놀로지	"116,716"	"39,950"	"19.79"	"3,003,751"	'389020
신		모나리자	"54,907"	"3,080"	"13.65"	"16,965,224"	'012690
신		나노팀	"92,759"	"9,000"	"12.64"	"9,895,378"	'417010


"""

daily_check = """
, no..
20241-11-20

삼부토건	"45,116"	"980"	"-10.09"	"45,451,356"	'001470
아이씨티케이	"836"	"5,680"	"-4.70"	"144,508"	'456010
KT&G	"35,542"	"115,500"	"-0.35"	"307,003"	'033780
하이젠알앤엠	"23,163"	"11,300"	"-5.75"	"2,022,593"	'160190

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
    if not re_try:
        stocks = rl.getTop40()

        for index, stock in enumerate(stocks):
            stock.print()
            stock.save_md()

    rl.merge_txt_order_md(stocks)
    rl.merge_txt_order_sum(stocks)


if __name__ == "__main__kiwoomFormat":

    result = kiwoomCopyReplace(stocks)
    print(result)
