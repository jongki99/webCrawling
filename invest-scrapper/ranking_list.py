import requests, re, datetime, time, os
from bs4 import BeautifulSoup

import code_news
import stock_info
from stock_info import MarketType

import util.util_common as uc


def getStockCode(url):
    code = re.search(r'code=(\d+)', url).group(1)
    return code


def get_stock_details(url, market_type=MarketType.KOSDAK):

    print("start loading...", stock_info.getTypeName(market_type))

    stockList = []

    print ( market_type )

    if ( market_type == MarketType.KOSDAK ):
        max_count = 30
    else:
        max_count = 10

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    stock_links = soup.select('a.tltle')
    
    for index, link in enumerate(stock_links):
        if ( max_count > index ):
            stock_raise_per = float(re.findall( r'\d+\.\d+', link.parent.parent.select_one("span.red01").text )[0])

            # if ( stock_raise_per > min_per): ## 그냥 30개만...
            stock_url = 'https://finance.naver.com' + link['href']
            stock_code = getStockCode(stock_url)
            ## print(link.text, link.parent.parent.select_one("span.red01"))
            # print("상세 페이지:", stock_url, "종목:", link.text, "등락률:", stock_raise_per)
            # 여기서 해당 링크를 이용하여 상세 정보를 수집하는 코드를 추가할 수 있습니다.

            stock = stock_info.StockInfo(market_type, link.text, stock_code)
            stockList.append(stock)
    
    return stockList


def getTop40():
    url = "https://finance.naver.com/sise/sise_rise.naver?sosok=1" # 코스닥.
    stockList = get_stock_details(url, MarketType.KOSDAK)
    url = "https://finance.naver.com/sise/sise_rise.naver?sosok=0" # 코스피.
    stockList = stockList + get_stock_details(url, MarketType.KOSPI)

    return stockList


def getTop40_main():
    stockList = getTop40()
    for index, stock in enumerate(stockList):
        stock.print()


def merge_txt():
    dd = datetime.datetime.now().strftime('%Y%m%d')
    file_name = f"{uc.base_data_path}/stock_info/d{dd}.txt"
    source_dir = f"{uc.base_data_path}/stock_info/d{dd}/"

    with open(file_name, 'w', encoding='utf-8') as list_file:
        # 디렉토리 내의 모든 파일에 대해 반복
        for 파일명 in os.listdir(source_dir):
            # .txt 파일만 대상으로 함
            if 파일명.endswith('.txt'):
                # 파일을 읽어와 결과 파일에 쓰기
                with open(os.path.join(source_dir, 파일명), 'r', encoding='utf-8') as 파일:
                    list_file.write(파일.read())
                    list_file.write('\n\n\n====================n')  # 각 파일 사이에 개행 추가

def merge_txt_order(stocks):
    dd = datetime.datetime.now().strftime('%Y%m%d')
    file_name = f"{uc.base_data_path}/stock_info/d{dd}.txt"
    source_dir = f"{uc.base_data_path}/stock_info/d{dd}/"

    with open(file_name, 'w', encoding='utf-8') as list_file:
        # 디렉토리 내의 모든 파일에 대해 반복
        for stock in stocks:
            파일명 = os.path.join(source_dir, f"{stock.code}_{stock.name}_{dd}.txt")
            # 파일을 읽어와 결과 파일에 쓰기
            with open(파일명, 'r', encoding='utf-8') as 파일:
                list_file.write(파일.read())
                list_file.write('\n\n\n=========================n')  # 각 파일 사이에 개행 추가


def merge_txt_order_md2(stocks):
    dd = datetime.datetime.now().strftime('%Y%m%d')
    file_name = f"{uc.base_data_path}/stock_info/s{dd}.md"
    source_dir = f"{uc.base_data_path}/stock_info/s{dd}/"
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)

    with open(file_name, 'w', encoding='utf-8') as list_file:
        list_file.write(f"# top40 daily : {dd}\n")
        # 디렉토리 내의 모든 파일에 대해 반복
        for stock in stocks:
            dd_file_path = os.path.join(source_dir, f"{stock.code}_{stock.name}_{dd}.md")
            # 파일을 읽어와 결과 파일에 쓰기
            with open(dd_file_path, 'r', encoding='utf-8') as dd_file_name:
                list_file.write(dd_file_name.read())
                list_file.write('\n')  # 각 파일 사이에 개행 추가


def merge_txt_order_md(stocks):
    dd = datetime.datetime.now().strftime('%Y%m%d')
    file_name = f"{uc.base_data_path}/stock_info/d{dd}.md"
    source_dir = f"{uc.base_data_path}/stock_info/d{dd}/"

    with open(file_name, 'w', encoding='utf-8') as list_file:
        list_file.write(f"# top40 daily : {dd}\n")
        # 디렉토리 내의 모든 파일에 대해 반복
        for stock in stocks:
            파일명 = os.path.join(source_dir, f"{stock.code}_{stock.name}_{dd}.md")
            # 파일을 읽어와 결과 파일에 쓰기
            with open(파일명, 'r', encoding='utf-8') as 파일:
                list_file.write(파일.read())
                list_file.write('\n')  # 각 파일 사이에 개행 추가

def merge_txt_order_sum(stocks, type=1):
    dd = datetime.datetime.now().strftime('%Y%m%d')

    current_folder_name = os.path.basename(os.getcwd())
    print("현재 폴더명:", current_folder_name)

    if current_folder_name == 'webCrawling':
        os.chdir('invest-scrapper')

    path = os.getcwd()
    file_name_csv = os.path.join(path, f"./comp_sum/s{type}_{dd}.csv")
    file_name = os.path.join(path, f"./comp_sum/ss{type}_{dd}.csv")

    with open(file_name, 'w', encoding='utf-8') as list_file:
        list_file.write(stock_info.StockInfo.getCsvSummaryTitle(type))
        list_file.write('\n')

        # 디렉토리 내의 모든 파일에 대해 반복
        for stock in stocks:
            # 파일을 읽어와 결과 파일에 쓰기
            list_file.write(stock.getCsvSummary(type))
            list_file.write('\n')

    with open(file_name_csv, 'w', encoding='utf-8') as list_file:
        list_file.write(stock_info.StockInfo.getCsvSummaryTitle(type))
        list_file.write('\n')

        # 디렉토리 내의 모든 파일에 대해 반복
        for stock in stocks:
            # 파일을 읽어와 결과 파일에 쓰기
            list_file.write(stock.getSummary(type))
            list_file.write('\n')


def merge_txt_order_sum2(stocks, type=1):
    dd = datetime.datetime.now().strftime('%Y%m%d')

    current_folder_name = os.path.basename(os.getcwd())
    print("현재 폴더명:", current_folder_name)

    if current_folder_name == 'webCrawling':
        os.chdir('invest-scrapper')

    path = os.getcwd()
    file_name = os.path.join(path, f"./comp_sum/sss{type}_{dd}.csv")

    with open(file_name, 'w', encoding='utf-8') as list_file:
        list_file.write(stock_info.StockInfo.getCsvSummaryTitle(type))
        list_file.write('\n')

        # 디렉토리 내의 모든 파일에 대해 반복
        for stock in stocks:
            # 파일을 읽어와 결과 파일에 쓰기
            list_file.write(stock.getCsvSummary2(type))
            list_file.write('\n')



def getDetailTest():
#    stock = StockInfo(1, "SOL 유럽탄소배출권선물S&P(H)", "400580")
    stock = stock_info.StockInfo(1, "CJ대한통운", "000120")
    stock.toPrint()
    #stock.save_md()



if __name__ == "__main__2":
    print('split', ''.join('12,123'.split(',')))
    print('strip', '12,123'.strip(','))
if __name__ == "__main__":
#    getTop40_main()
#    getDetailTest()
    current_folder_name = os.path.basename(os.getcwd())
    print("현재 폴더명:", current_folder_name)

    if current_folder_name == 'webCrawling':
        os.chdir('invest-scrapper')

    stocks = getTop40()

    merge_txt_order_sum(stocks)

    # stocks = getTop40()
    # merge_txt_order(stocks)

#    stocks = getTop40()
#    merge_txt_order_md(stocks)