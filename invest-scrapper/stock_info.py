from types import NoneType
import requests, re, datetime, time, os
from bs4 import BeautifulSoup

import code_news
import comp_news_keyword as kk

from enum import Enum


class MarketType(Enum):
    KOSPI = 0,
    KOSDAK = 1,
    SEARCH = 99,


def getCodeUrl(code):
    return f"https://finance.naver.com/item/main.naver?code={code}"


def getTypeName(type=MarketType.KOSDAK):
    if type == MarketType.KOSDAK:
        return "코스닥"
    if type == MarketType.SEARCH:
        return "검색"
    if type == MarketType.KOSPI:
        return "코스피"
    return "코스피"


class StockDetailSoupObject:
    def __init__(self, name, code, html_text):
        self.name = name
        self.code = code
        self.url = getCodeUrl(code)

        self.html = html_text
        self.soup = BeautifulSoup(html_text, "html.parser")
        self.url = getCodeUrl(code)

        self.loading()


    def select_one(self, select):
        s = self.soup
        h = s.select_one(select)
        print(f"h={h}")
        if ( h and h.attrs ):
            print(f"attrs={h.attrs}")
        return h


    def select_one2(self, html, select):
        s = self.soup
        h = html.select_one(select)
        print(f"h={h}")
        if ( h and h.attrs ):
            print(f"attrs={h.attrs}")
        return h


    def select(self, select):
        s = self.soup
        h = s.select(select)
        print(f"h={h}")
        return h


    #############################################################################################

    def marketName(self):
        h = self.select_one('div.description img')
        self.market_name = h.attrs['alt']
    

    def upjongName(self):
        trade_compare = self.select_one('div.trade_compare')
        if trade_compare:
            upjong = trade_compare.select_one('em a')
            self.upjong_name = upjong.text
            self.upjong_code = re.search(r'no=(\d+)', upjong.attrs["href"]).group(1)
        else:
            self.upjong_name = ""
            self.upjong_code = ""


    def companyPriceSelect(self):
        sel = self.select_one('div.today p.no_today em.no_up span.blind')
        if sel:
            self.company_price = sel.text
        else:
            self.company_price = ''

        sel_p = self.select_one('div.today p.no_exday em.no_up')
        print("sel_p", sel_p)

        sel2 = self.select_one('div.today p.no_exday em.no_up span.blind')
        if (sel2):
            self.company_price_up = sel2.text.strip().strip('\n')
        else:
            self.company_price_up = ''

        sel2 = self.select('div.today p.no_exday em.no_up')
        if sel2 and len(sel2) > 1:
            sel2 = sel2[1]

        if sel2:
            self.company_price_up_per = sel2.select_one('span.plus').text + sel2.select_one('span.blind').text
        else:
            self.company_price_up_per = ''


    def tradePrice(self):
        self.trade_price = ""
        s2 = self.select("table.no_info tr")

        if ( len(s2) > 1 ):
            tr = s2[1]

            td3 = tr.select("td")
            if ( len(td3) > 2 ):
                self.select_one2(td3[2], "em")

                bl = td3[2].select_one("em span.blind")
                print("bl", bl)

                self.trade_price = bl.text
                if self.trade_price:
                    self.trade_price = ".".join(self.trade_price.split(','))


    def loading(self):
        self.marketName()
        self.upjongName()

        self.market_sum = self.select_one('#_market_sum').text.strip().strip(' ') + ' 억원'
        self.market_sum = " ".join(self.market_sum.split())

        self.companyPriceSelect()

        sel = self.select_one('#summary_info.summary_info')
        if sel:
            self.company_info = sel.text.strip()
        else:
            self.company_info = ''

        self.tradePrice()


    def __str__(self):
        return f"""
회사명 : {self.name}({self.code})
시  장 : {self.market_name}
업 종 : {self.upjong_name}({self.upjong_code})
시가총액 : {self.market_sum}
거래대금 : {self.trade_price} 백만.
금일 가격 : {self.company_price}, 전일대비 {self.company_price_up}, 상승율 {self.company_price_up_per}

{self.company_info}
, """





class StockInfo:
    def __init__(self, type, name, code):
        self.type = type
        self.name = name
        self.code = code
        self.url = getCodeUrl(code)
        self.__detail = None ### TODO.

        self.news_keys = None

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
        if not( self.__detail ):
            self.__detail = StockDetail(type=self.type, name=self.name, code=self.code)
        return self.__detail
    

    def news_ai(self):
        if ( not self.news_keys):
            self.news_keys = ""
            self.news_summary = ""

            html_text = self.__detail.comp_issue_keys()

            keys, summerize = kk.summarize_and_extract_keywords(html_text)
            self.news_keys = keys
            self.news_summary = summerize
    
    def getCsvSummaryTitle(type=1):
        
        dd = datetime.datetime.now().strftime('%Y%m%d')
        comp_code = ''
        if ( type == 1 ):
            comp_code = ', 회사코드'
        else:
            comp_code = ''
        return f"회사명{comp_code}, 업종명, 시총, 상승률, 거래대금, 종합평가, 이슈, 차트분석, {dd}\n"


    def getSummary(self, type=1):
        # rainbow csv
        detail = self.getDetail()
        # self.news_ai()
        company_price = '.'.join(detail.company_price.split(','))
        upjong_name = '.'.join(detail.upjong_name.split(','))
        trade_price = detail.trade_price


        if ( len(self.__detail.news_list) > 10 ):
            nn = self.__detail.news_list[:10]
        else:
            nn = self.__detail.news_list
        news_str = '\n      , '.join(str(news) for news in nn)
        naver_news_str = '\n        , '.join(str(news) for news in self.__detail.news_list_naver)
        if ( type == 1 ):
            return f"{self.name}, {self.code}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}"
        else:
            return f"{self.name}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}"


    def getCsvSummary(self, type=1):
        # rainbow csv
        detail = self.getDetail()
        self.news_ai()
        company_price = '.'.join(detail.company_price.split(','))
        upjong_name = '.'.join(detail.upjong_name.split(','))
        trade_price = detail.trade_price


        if ( len(self.__detail.news_list) > 10 ):
            nn = self.__detail.news_list[:10]
        else:
            nn = self.__detail.news_list
        news_str = '\n      , '.join(str(news) for news in nn)
        naver_news_str = '\n        , '.join(str(news) for news in self.__detail.news_list_naver)

        if ( type == 1 ):
            return f"""{self.name}, {self.code}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}
    , keywords : {self.news_keys}
    , summary : {self.news_summary}
    , stock news : {news_str}
    , naver news : {naver_news_str}
"""
        else:
            return f"""{self.name}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}
    , keywords : {self.news_keys}
    , summary : {self.news_summary}
    , stock news : {news_str}
    , naver news : {naver_news_str}
"""



    def getCsvSummary2(self, type=1):
        # rainbow csv
        detail = self.getDetail()
        self.news_ai()
        company_price = '.'.join(detail.company_price.split(','))
        upjong_name = '.'.join(detail.upjong_name.split(','))
        trade_price = detail.trade_price


        if ( len(self.__detail.news_list) > 10 ):
            nn = self.__detail.news_list[:10]
        else:
            nn = self.__detail.news_list
        news_str = '\n      , '.join(str(news) for news in nn)
        naver_news_str = '\n        , '.join(str(news) for news in self.__detail.news_list_naver)

        if ( type == 1 ):
            return f"""{self.name}, {self.code}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}
    , keywords : {self.news_keys}
    , summary : {self.news_summary}
"""
        else:
            return f"""{self.name}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}
    , keywords : {self.news_keys}
    , summary : {self.news_summary}
"""


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
        self.naver_html = response.text
        soup = BeautifulSoup(response.text, "html.parser")

        self.bean = StockDetailSoupObject(self.name, self.code, response.text)
        b = self.bean

        self.upjong_name = b.upjong_name
        self.upjong_code = b.upjong_code


        self.market_sum = b.market_name

        self.news_list = code_news.getNaverCodeNewsList(self.code)
        self.date = datetime.datetime.now()
        self.news_list_naver = code_news.getNaverNewsList(self.name)

        self.company_info = b.company_info
        self.company_price = b.company_price
        self.company_price_up = b.company_price_up
        self.company_price_up_per = b.company_price_up_per

        self.trade_price = b.trade_price


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
거래대금 : {self.trade_price}
금일 가격 : {self.company_price}, 전일대비 {self.company_price_up}, 상승율 {self.company_price_up_per}
기업개요 : {self.company_info}
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
    

    def comp_issue_keys(self):
        if ( len(self.news_list) > 10 ):
            nn = self.news_list[:10]
        else:
            nn = self.news_list
        news_str = '\n'.join(str(news.md_format()) for news in nn)
        naver_new_str = '\n'.join(str(news.md_format()) for news in self.news_list_naver)

        return f"""
회사명(증권코드):{self.name}({self.code})
news1:
{news_str}
news2:
{naver_new_str}
"""


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
    거래대금 : {self.trade_price}
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



if __name__ == "__main__1": # ai 연동을 위한 데이터 가져오기.
    dd = dd = datetime.datetime.now().strftime('%Y%m%d')
    name = "삼성전자"
    code = "005930"
     
    current_folder_name = os.path.basename(os.getcwd())
    print("현재 폴더명:", current_folder_name)

    if current_folder_name == 'webCrawling':
        os.chdir('invest-scrapper')

    file_path = f"./test_data/stock_{name}_{code}-{dd}-ai.txt"
    if not os.path.exists(file_path):
        sd = StockDetail(1, name, code)
        key_text = sd.comp_issue_keys()

        # w 덮어쓰기, a 추가하기.
        with open(file_path, "w") as file: 
            file.write(key_text)

        html_text = key_text
    else:
        with open(file_path, "r") as file:
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
        with open(file_path, "w") as file: 
            file.write(response.text)

        html_text = response.text
    else:
        with open(file_path, "r") as file:
            html_text = file.read()

    sdso = StockDetailSoupObject(name, code, html_text)
    print(sdso)

