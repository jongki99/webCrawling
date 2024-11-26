"""
네이버 증권 홈.
https://finance.naver.com/sise/

검색창에 쿼리...

https://ac.stock.naver.com/ac?q=https%3A%2F%2Ffinance.naver.com%2Fsise%2F&target=index%2Cstock%2Cmarketindicator

https://ac.stock.naver.com/ac?q=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%901&target=index%2Cstock%2Cmarketindicator


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

,9/9, 월
제룡전기
화성밸브
폴라리스오피스
대봉엘에스
실리콘투
셀리드
샤페론
인벤티지랩
SAMG엔터
블루엠텍
네오이뮨텍

,9/6, 금
셀루메드
DB금융투자
LK삼양
한컴라이프케어
퓨런티어

,9/5, 목
덱스터,VFX,덱스터, 韓 스튜디오 최초 美 '아마존프라임' 프로젝트 맡아, (디지털데일리, 2024.09.05 09:50)
원텍,건강관리장비와용품,원텍 ‘올리지오X’, 브라질 의료기기 판매 인증 획득, (매일경제, 2일 전)
엑스게이트,소프트웨어,엑스게이트 주가 방긋... 양자암호 기반 가상사설망 상용화 성공, (핀포인트뉴스, 13시간 전)
아이씨티케이,통신장비,딥페이크
대봉엘에스,제약,피부친환신기술.
KCTC,항공화물운송과물류

모니터랩, 소프트웨어, 5520, +29.88, 315억, 딥페이크
에스오에스랩, 전자장비와기기, 7820, +11.55, 270억, 
선익시스템, 디스플레이장비및부품, 50000, +9.89, 198억
에스피소프트, IT서비스, 9480, +8.34, 528억
롯데에너지머티리얼즈, 전자장비와기기, 43000, +8.31, 481억
강원랜드, 호텔.레스토랑.레저, 17730, +7.85, 3013억

,9/4, 수
시너지이노베이션
셀루메드
한전산업

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
    stocks = rl.getTop40()

    for index, stock in enumerate(stocks):
        stock.print()
        stock.save_md()

    rl.merge_txt_order_md(stocks)
    rl.merge_txt_order_sum(stocks)

