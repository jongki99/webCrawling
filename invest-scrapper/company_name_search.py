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

stocks = f"""

,9/3, 화
갤럭시아머니트리
뱅크웨어글로벌
라메디텍
"""

stocks1 = f"""

,9/3, 화
갤럭시아머니트리
뱅크웨어글로벌
라메디텍

KCTC
한국정보인증
위메이드맥스
케이옥션
이브이첨단소재
에이디테크놀로지
브릿지바이오테라퓨틱스

,9,2 월
한국화장품제조
포스코엠텍
DS단석
포스코DX
하이젠알엔엠
엔켐
피엔에스미캐닉스
티디에스팜

,8,30 금
이엔셀
라메디텍
M83

라온시큐어
비에이치
노브랜드
엑스게이트

지아이이노베이션
HLB생명과학


,8,29 목
라파스,1,여드름패치FDA
블루엠텍,2,코로나진단
한빛레이저,2,너무올랐어 계속갈련가?,전기차 배터리 안전. 화재 예방용 마킹.
이엔셀,2,신규
이수스페셜티케미컬,2,전기차안전...

,8,28 수
유한양행,1,렉라자
대봉엘에스,1,피부친화 접착성 신소개 상용화
디앤디파마텍,1,GLP-1 경구용 비만치료제.
필에너지,1,배터리 공장 증축.

현대바이오,2,증100,코로나19치료제3상
티디에스팜,2,신규
M83,2,신규

,8,27 화
에스피소프트
롯데이노베이트
이스트소프트
폴라리스AI
한싹
NE능률

,8,26 월
에이프릴바이오,1,
보로노이,1,자가면역질환 치료제 미국계약.
케이엔솔,1,배터리 액침냉각.
삼성공조

,8,23 금
아이씨티케이,2,양자 물리 보안.
GS글로벌
화성밸브
에스와이스틸텍

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

