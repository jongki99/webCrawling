import requests, re, datetime, time, os
from bs4 import BeautifulSoup

import code_news


def getTypeName(type):
    if type == 1:
        return "코스닥"
    if type == 2:
        return "검색"
    return "코스피"


def getStockCode(url):
    code = re.search(r'code=(\d+)', url).group(1)
    return code


def getCodeUrl(code):
    return f"https://finance.naver.com/item/main.naver?code={code}"

def get_stock_details(url, type):

    print("start loading...", getTypeName(type))

    stockList = []

    if ( type == 1 ):
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

            stock = StockInfo(type, link.text, stock_code)
            stockList.append(stock)
    
    return stockList


def getTop40():
    url = "https://finance.naver.com/sise/sise_rise.naver?sosok=1" # 코스닥.
    stockList = get_stock_details(url, 1)
    url = "https://finance.naver.com/sise/sise_rise.naver?sosok=0" # 코스피.
    stockList = stockList + get_stock_details(url, 0)

    return stockList


def getTop40_main():
    stockList = getTop40()
    for index, stock in enumerate(stockList):
        stock.print()


class StockInfo:
    def __init__(self, type, name, code):
        self.type = type
        self.name = name
        self.code = code
        self.url = getCodeUrl(code)

    def __str__(self):
        typeName = getTypeName(self.type)
        return f"{typeName},name={self.name}, link={self.url}"
    
    def print(self):
        print(self)

    def toPrint(self):
        detail = self.getDetail()
        print(detail)

    def save(self):
        detail = self.getDetail()
        detail.to_file()

    def save_md(self):
        detail = self.getDetail()
        detail.to_md_file()

    def save_md2(self):
        detail = self.getDetail()
        detail.to_md_file2()

    def getDetail(self):
        detail = StockDetail(type=self.type, name=self.name, code=self.code)
        return detail
    
def merge_txt():
    dd = datetime.datetime.now().strftime('%Y%m%d')
    file_name = f"./stock_info/d{dd}.txt"
    source_dir = f"./stock_info/d{dd}/"

    with open(file_name, 'w') as list_file:
        # 디렉토리 내의 모든 파일에 대해 반복
        for 파일명 in os.listdir(source_dir):
            # .txt 파일만 대상으로 함
            if 파일명.endswith('.txt'):
                # 파일을 읽어와 결과 파일에 쓰기
                with open(os.path.join(source_dir, 파일명), 'r') as 파일:
                    list_file.write(파일.read())
                    list_file.write('\n\n\n====================n')  # 각 파일 사이에 개행 추가

def merge_txt_order(stocks):
    dd = datetime.datetime.now().strftime('%Y%m%d')
    file_name = f"./stock_info/d{dd}.txt"
    source_dir = f"./stock_info/d{dd}/"

    with open(file_name, 'w') as list_file:
        # 디렉토리 내의 모든 파일에 대해 반복
        for stock in stocks:
            파일명 = os.path.join(source_dir, f"{stock.code}_{stock.name}_{dd}.txt")
            # 파일을 읽어와 결과 파일에 쓰기
            with open(파일명, 'r') as 파일:
                list_file.write(파일.read())
                list_file.write('\n\n\n=========================n')  # 각 파일 사이에 개행 추가


def merge_txt_order_md2(stocks):
    dd = datetime.datetime.now().strftime('%Y%m%d')
    file_name = f"./stock_info/s{dd}.md"
    source_dir = f"./stock_info/s{dd}/"

    with open(file_name, 'w') as list_file:
        list_file.write(f"# top40 daily : {dd}\n")
        # 디렉토리 내의 모든 파일에 대해 반복
        for stock in stocks:
            파일명 = os.path.join(source_dir, f"{stock.code}_{stock.name}_{dd}.md")
            # 파일을 읽어와 결과 파일에 쓰기
            with open(파일명, 'r') as 파일:
                list_file.write(파일.read())
                list_file.write('\n')  # 각 파일 사이에 개행 추가


def merge_txt_order_md(stocks):
    dd = datetime.datetime.now().strftime('%Y%m%d')
    file_name = f"./stock_info/d{dd}.md"
    source_dir = f"./stock_info/d{dd}/"

    with open(file_name, 'w') as list_file:
        list_file.write(f"# top40 daily : {dd}\n")
        # 디렉토리 내의 모든 파일에 대해 반복
        for stock in stocks:
            파일명 = os.path.join(source_dir, f"{stock.code}_{stock.name}_{dd}.md")
            # 파일을 읽어와 결과 파일에 쓰기
            with open(파일명, 'r') as 파일:
                list_file.write(파일.read())
                list_file.write('\n')  # 각 파일 사이에 개행 추가



def getDetailTest():
#    stock = StockInfo(1, "SOL 유럽탄소배출권선물S&P(H)", "400580")
    stock = StockInfo(1, "CJ대한통운", "000120")
    stock.toPrint()
    #stock.save_md()



class StockDetail:
    def __init__(self, type, name, code):
        self.type = type
        self.name = name
        self.code = code
        self.url = getCodeUrl(code)

        self.loading()


    def to_file(self):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        file_name = f"./stock_info/d{dd}/{self.code}_{self.name}_{dd}.txt"
        dir = os.path.dirname(file_name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        with open(file_name, 'w') as file:
            file.write(str(self))
            self.save_chart_day_candle()

    def to_md_file(self):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        file_name = f"./stock_info/d{dd}/{self.code}_{self.name}_{dd}.md"
        dir = os.path.dirname(file_name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        with open(file_name, 'w') as file:
            file.write(str(self.md_format()))
            self.save_chart_day_candle()

    def to_md_file2(self):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        file_name = f"./stock_info/s{dd}/{self.code}_{self.name}_{dd}.md"
        dir = os.path.dirname(file_name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        with open(file_name, 'w') as file:
            file.write(str(self.md_format()))
            self.save_chart_day_candle()

    def save_file_common(self, url, type):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        response = requests.get(url)
        if response.status_code == 200:
            file_name = f"./stock_info/d{dd}/{self.code}_{self.name}_{dd}_{type}.png"
            dir = os.path.dirname(file_name)
            if not os.path.exists(dir):
                os.makedirs(dir)
            
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"이미지 다운로드가 완료되었습니다.({type})")
        else:
            print(f"이미지를 다운로드할 수 없습니다.({type})")
        

    def save_chart_day_candle(self):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        url = f"https://ssl.pstatic.net/imgfinance/chart/item/candle/day/{self.code}.png"
        self.save_file_common(url, 'd')
        url = f"https://ssl.pstatic.net/imgfinance/chart/item/candle/week/{self.code}.png"
        self.save_file_common(url, 'w')
        url = f"https://ssl.pstatic.net/imgfinance/chart/item/candle/month/{self.code}.png"
        self.save_file_common(url, 'm')



    def loading(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        trade_compare = soup.select_one('div.trade_compare')
        if trade_compare:
            upjong = trade_compare.select_one('em a')
            self.upjong_name = upjong.text
            self.upjong_code = re.search(r'no=(\d+)', upjong.attrs["href"]).group(1)
        else:
            self.upjong_name = ""
            self.upjong_code = ""

        self.market_sum = soup.select_one('#_market_sum').text.strip().strip(' ') + ' 억원'
        self.market_sum = " ".join(self.market_sum.split())

        self.news_list = code_news.getNaverCodeNewsList(self.code)
        self.date = datetime.datetime.now()
        self.news_list_naver = code_news.getNaverNewsList(self.name)

        sel = soup.select_one('#summary_info.summary_info')
        if sel:
            self.company_info = sel.text.strip()
        else:
            self.company_info = ''

        sel = soup.select_one('div.today p.no_today em.no_up span.blind')
        if sel:
            self.company_price = sel.text
        else:
            self.company_price = ''

        sel = soup.select_one('div.today p.no_exday em.no_up span.up_price')
        sel2 = soup.select_one('div.today p.no_exday em.no_up span.blind')
        if (sel and sel2):
            self.company_price_up = sel.text + sel2.text.strip().strip('\n')
        else:
            self.company_price_up = ''

        sel2 = soup.select('div.today p.no_exday em.no_up')
        if sel2:
            sel2 = sel2[1]
        if sel2:
            self.company_price_up_per = sel2.select_one('span.plus').text + sel2.select_one('span.blind').text
        else:
            self.company_price_up_per = ''


    def __str__(self):
        typeName = getTypeName(self.type)
        news_str = '\n'.join(str(news) for news in self.news_list)
        naver_new_str = '\n'.join(str(news) for news in self.news_list_naver)

        if ( self.upjong_name ):
            upjong_str = f"업종 : {self.upjong_name}({self.upjong_code})"
        else:
            upjong_str = ""

        re = f"""{typeName} : {self.name}({self.code})
url : {self.url}
{upjong_str}
시가총액 : {self.market_sum}
기업개요 : {self.company_info}
금일 가격 : {self.company_price}, 전일대비 {self.company_price_up}, 상승율 {self.company_price_up_per}
------------------------------------------------------------------

종목 뉴스
------------------------------------------------------------------
{news_str}


네이버 뉴스 : {self.date}
------------------------------------------------------------------
{naver_new_str}

------------------------------------------------------------------
차트: https://ssl.pstatic.net/imgfinance/chart/item/candle/day/033790.png
"""
        
        return re
    

    def md_format(self):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        typeName = getTypeName(self.type)
        news_str = '\n'.join(str(news.md_format()) for news in self.news_list)
        naver_new_str = '\n'.join(str(news.md_format()) for news in self.news_list_naver)

        if ( self.upjong_name ):
            upjong_str = f"업종 : {self.upjong_name}({self.upjong_code})"
        else:
            upjong_str = ""

        return f"""
## {typeName} : [{self.name}({self.code})]({self.url})

    {upjong_str}
    시가총액 : {self.market_sum}
    금일 가격 : {self.company_price}, 전일대비 {self.company_price_up}, 상승율 {self.company_price_up_per}
    기업개요 : {self.company_info}

*****

* 종목 뉴스

*****

{news_str}

*****

* 네이버 뉴스 : {self.date}

*****

{naver_new_str}

*****

차트 이미지: https://ssl.pstatic.net/imgfinance/chart/item/candle/day/033790.png
차트 이미지 d: 

![{self.code}_{self.name}_{dd}.png](./{self.code}_{self.name}_{dd}_d.png)

차트 이미지 w: 

![{self.code}_{self.name}_{dd}.png](./{self.code}_{self.name}_{dd}_w.png)

차트 이미지 m: 

![{self.code}_{self.name}_{dd}.png](./{self.code}_{self.name}_{dd}_m.png)

차트 이미지 d: 

![{self.code}_{self.name}_{dd}.png](./d{dd}/{self.code}_{self.name}_{dd}_d.png)

차트 이미지 w: 

![{self.code}_{self.name}_{dd}.png](./d{dd}/{self.code}_{self.name}_{dd}_w.png)

차트 이미지 m: 

![{self.code}_{self.name}_{dd}.png](./d{dd}/{self.code}_{self.name}_{dd}_m.png)

"""

if __name__ == "__main__":
#    getTop40_main()
    getDetailTest()
    # stocks = getTop40()
    # merge_txt_order(stocks)

#    stocks = getTop40()
#    merge_txt_order_md(stocks)