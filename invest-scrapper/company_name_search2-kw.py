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
KT&G
아이씨티케이
,공장 - 좀 길게... 100% 이상을 보고... 일단 관찰 부터...
태성
하이젠알앤엠
, 관찰. ( 트럼프, 재건주. )
삼부토건, 급상승 - 급락중(1120), 5일선 돌파를 봐봐? 무리일것 같은데... 코드닥이 좋지 않기도 하고...


분	신	종목명	거래대금	현재가	등락률	거래량	종목코드
2024-11-15. 금							
신		전진건설로봇	"55,595"	"29,550"	"-1.50"	"1,816,935"	'079900
증		펩트론	"171,281"	"105,200"	"1.45"	"1,732,715"	'087010
신		에스와이	"17,027"	"4,475"	"4.07"	"3,824,468"	'109610
증		SG	"56,866"	"3,415"	"5.08"	"16,816,493"	'255220
신		에스와이스틸텍	"236,438"	"8,700"	"2.47"	"26,268,750"	'365330
신		원익홀딩스	"90,145"	"2,870"	"6.69"	"29,048,323"	'030530
신		루닛	"319,034"	"54,900"	"-14.88"	"5,376,451"	'328130
		다산네트웍스	"24,089"	"4,035"	"8.91"	"6,101,376"	'039560
		유진로봇	"6,157"	"6,700"	"-4.15"	"893,777"	'056080
		차이커뮤니케이션	"6,012"	"9,470"	"1.83"	"613,276"	'351870
2024-11-18. 월.							
증		HLB	"94,416"	"73,300"	"2.37"	"1,299,811"	'028300
증		HLB테라퓨틱스	"18,046"	"10,510"	"6.27"	"1,739,435"	'115450
		와이제이링크	"61,262"	"12,570"	"2.36"	"4,631,597"	'209640
신		루닛	"319,034"	"54,900"	"-14.88"	"5,376,451"	'328130
신		SG글로벌	"35,838"	"4,020"	"0.37"	"8,597,468"	'001380
증		신성델타테크	"20,297"	"50,900"	"-0.78"	"391,065"	'065350
증		HLB생명과학	"9,598"	"10,010"	"1.42"	"966,716"	'067630
증		휴마시스	"11,971"	"1,862"	"-3.52"	"6,248,322"	'205470
신		퓨런티어	"41,190"	"27,650"	"1.10"	"1,486,378"	'370090
신		SK이터닉스	"3,719"	"13,760"	"-1.71"	"268,861"	'475150
2024-11-19. 화.							
신		우리바이오	"142,136"	"3,320"	"5.73"	"42,394,551"	'082850
신		비에이치아이	"42,863"	"16,900"	"-2.14"	"2,502,540"	'083650
신		아톤	"27,040"	"5,450"	"-6.84"	"4,872,792"	'158430
신		하이젠알앤엠	"23,258"	"11,350"	"0.44"	"2,058,241"	'160190
신		SK이노베이션	"67,693"	"118,900"	"5.04"	"570,143"	'096770
		로보티즈	"6,155"	"19,420"	"-1.47"	"314,312"	'108490
2024-11-20. 수.							
		한일단조	"41,642"	"3,005"	"-6.68"	"13,691,437"	'024740
신		셀바스헬스케어	"10,923"	"4,725"	"-2.28"	"2,325,949"	'208370
신		셀바스AI	"8,862"	"11,480"	"-2.05"	"763,201"	'108860
		쓰리빌리언	"225,016"	"3,900"	"1.30"	"52,348,152"	'394800
신		바이오플러스	"9,716"	"5,540"	"-0.18"	"1,749,070"	'099430
증		셀리드	"69,904"	"6,400"	"-8.44"	"9,843,295"	'299660
		에이럭스	"14,185"	"7,580"	"-7.56"	"1,776,860"	'475580
2024-11-21. 목							
신		대동	"173,380"	"11,700"	"18.18"	"15,271,953"	'000490
관		삼부토건	"115,619"	"1,274"	"30.00"	"99,430,142"	'001470
신		한미글로벌	"221,961"	"19,740"	"25.81"	"11,741,789"	'053690
		대동기어	"62,753"	"10,800"	"29.96"	"6,533,746"	'008830
		컴투스홀딩스	"53,959"	"29,250"	"15.84"	"1,795,637"	'063080
증		강스템바이오텍	"61,855"	"2,685"	"18.81"	"22,339,562"	'217730


"""

daily_check = """
, no..
20241-11-20

관		삼부토건	"45,116"	"980"	"-10.09"	"45,451,356"	'001470
신		아이씨티케이	"836"	"5,680"	"-4.70"	"144,508"	'456010
신		KT&G	"35,542"	"115,500"	"-0.35"	"307,003"	'033780
신		하이젠알앤엠	"23,163"	"11,300"	"-5.75"	"2,022,593"	'160190


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
