from types import NoneType
import requests, re, datetime, time, os
from bs4 import BeautifulSoup

import code_news
import comp_news_keyword as kk
import util.util_common as uc

from enum import Enum



class MarketType(Enum):
    KOSPI = 0,
    KOSDAK = 1,
    SEARCH = 99,


def getCodeUrl(code):
    return f"https://finance.naver.com/item/main.naver?code={code}"
def getCodeJongUrl(code):
    return f"https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}"

def blind_text(name, soup):
    # 전일,시가,고가,저가,거래량,거래대금 blind 찾기
    # uc.logger.fatal(f"{name}:tag start")
    # prev_price_tag = soup.find('div.rate_info', text=lambda text: text and '전일가' in text)
    # prev_day = soup.select_one(f'div.rate_info table span:contains("{name}")').parent
    prev_day = soup.select_one(f'div.rate_info table span:-soup-contains("{name}")')
    if prev_day:
        prev_day = prev_day.parent
        prev_day = prev_day.select_one('span.blind')
        if prev_day:
            prev_day = prev_day.text
            prev_day = ''.join(prev_day.split(','))
            # uc.logger.fatal(f"{name}:tag find end {prev_day}")
            return prev_day
        
    # uc.logger.fatal(f"{name}:tag no find end")
    return ''
    
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


    def get_soup(self):
        return self.soup

    def find(self, select):
        return self.soup.find(select)

    def select_one(self, select):
        s = self.soup
        h = s.select_one(select)
        # print(f"h={h}")
        # if ( h and h.attrs ):
        #     print(f"attrs={h.attrs}")
        return h


    def select_one2(self, html, select):
        s = self.soup
        h = html.select_one(select)
        # print(f"h={h}")
        # if ( h and h.attrs ):
        #     print(f"attrs={h.attrs}")
        return h


    def select(self, select):
        s = self.soup
        h = s.select(select)
        # print(f"h={h}")
        return h


    #############################################################################################

    def marketName(self):
        self.market_name = ''
        h = self.select_one('div.description img')
        if h:
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
        soup = self.get_soup()


        uc.logger.info(f"현재가. 3가지 -+0 start")
        self.company_price = ''
        tr_tag = soup.select_one('p.no_today')
        uc.logger.debug(f"현재가 : {tr_tag}")

        if tr_tag:
            td_tag = tr_tag.select_one("span.blind")
            if td_tag:
                pp = td_tag.get_text(strip=True).strip(',')
                pp = ''.join(pp.split(','))
                uc.logger.debug(pp)
                self.company_price = pp
        uc.logger.info(f"현재가 : {self.company_price}")



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

        # 현재가.
        # uc.logger.info(f"현재가격:today_price start")
        self.today_price = ''
        today_price = self.select_one('div.today p.no_today span.blind')
        # print('현재가격 찾기...', today_price)
        if today_price:
            self.today_price = ''.join(today_price.text.split(','))
        # uc.logger.info(f"현재가격:{self.today_price}")

        self.price_prev = blind_text('전일', soup)
        self.price_start = blind_text('시가', soup)
        self.price_high = blind_text('고가', soup)
        self.price_low = blind_text('저가', soup)
        self.trade_amt = blind_text('거래량', soup)
        self.tradePrice()
        
    def tradePrice(self):
        self.trade_price = blind_text('거래대금', self.soup)
        self.trade_price = uc.pretty_format_number(self.trade_price + "000000")


    def loading(self):
        self.marketName()
        self.upjongName()

        self.market_sum = self.select_one('#_market_sum').text.strip().strip(' ') + ' 억원'
        self.market_sum = " ".join(self.market_sum.split())
        # print('self.market_sum', self.market_sum)

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
        pass
        # 2024-05-30 : 일단 지금은 사용하지 않는 걸로...

        # if ( not self.news_keys):
        #     self.news_keys = ""
        #     self.news_summary = ""

        #     html_text = self.__detail.comp_issue_keys()

        #     keys, summerize = kk.summarize_and_extract_keywords(html_text)
        #     self.news_keys = keys
        #     self.news_summary = summerize
    
    def getCsvSummaryTitle(type=1):
        
        dd = datetime.datetime.now().strftime('%Y%m%d')
        comp_code = ''
        if ( type == 1 ):
            comp_code = ', 회사코드'
        else:
            comp_code = ''
        return f"회사명{comp_code}, 업종명, 시총, 상승률, 거래대금, 거래일자, 거래금액, 종합평가, 이슈, 차트분석, {dd}\n"


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
        dd = datetime.datetime.now().strftime('%Y%m%d')
        detail = self.getDetail()
        # self.news_ai()
        company_price = '.'.join(detail.company_price.split(','))
        upjong_name = '.'.join(detail.upjong_name.split(','))
        trade_price = detail.trade_price


        if ( len(detail.news_list) > 10 ):
            nn = detail.news_list[:10]
        else:
            nn = detail.news_list
        news_str = '\n      , '.join(str(news) for news in nn)
        naver_news_str = '\n        , '.join(str(news) for news in detail.news_list_naver)

#         if ( type == 1 ):
#             return f"""{self.name}, {self.code}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}
#     , keywords : {self.news_keys}
#     , summary : {self.news_summary}
#     , stock news : {news_str}
#     , naver news : {naver_news_str}
# """
#         else:
#             return f"""{self.name}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}
#     , keywords : {self.news_keys}
#     , summary : {self.news_summary}
#     , stock news : {news_str}
#     , naver news : {naver_news_str}
# """
        trade_dt = dd
        today_price = detail.today_price

        if ( type == 1 ):
            return f"""{self.name}, {self.code}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}, {trade_dt}, {today_price}
    , stock news : {news_str}
    , naver news : {naver_news_str}
"""
        else:
            return f"""{self.name}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}, {trade_dt}, {today_price}
    , stock news : {news_str}
    , naver news : {naver_news_str}
"""



    def getCsvSummary2(self, type=1):
        # rainbow csv
        dd = datetime.datetime.now().strftime('%Y%m%d')
        detail = self.getDetail()
        # self.news_ai()
        company_price = '.'.join(detail.company_price.split(','))
        upjong_name = '.'.join(detail.upjong_name.split(','))
        trade_price = detail.trade_price


        if ( len(detail.news_list) > 10 ):
            nn = detail.news_list[:10]
        else:
            nn = detail.news_list
        news_str = '\n      , '.join(str(news) for news in nn)
        naver_news_str = '\n        , '.join(str(news) for news in detail.news_list_naver)

        trade_dt = dd
        today_price = detail.today_price

        if ( type == 1 ):
            return f"""{self.name}, {self.code}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}, {trade_dt}, {today_price}"""
        else:
            return f"""{self.name}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}, {trade_dt}, {today_price}"""

#         if ( type == 1 ):
#             return f"""{self.name}, {self.code}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}
#     , keywords : {self.news_keys}
#     , summary : {self.news_summary}
# """
#         else:
#             return f"""{self.name}, {upjong_name}, {company_price}, {detail.company_price_up_per}, {trade_price}
#     , keywords : {self.news_keys}
#     , summary : {self.news_summary}
# """


class StockDetail:
    def __init__(self, type, name, code):
        self.type = type
        self.name = name
        self.code = code
        self.url = getCodeUrl(code)

        self.loading()


    def to_file(self):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        file_name = f"{uc.base_data_path}/stock_info/d{dd}/{self.code}_{self.name}_{dd}.txt"
        dir = os.path.dirname(file_name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(str(self))
            self.save_chart_day_candle()

    def to_file_memo(self):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        file_name = f"{uc.base_data_path}/stock_data/stock-{dd}/{self.code}_{self.name}_{dd}.txt"
        dir = os.path.dirname(file_name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(str(self.memo_format()))

    def to_md_file(self):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        file_name = f"{uc.base_data_path}/stock_info/d{dd}/{self.code}_{self.name}_{dd}.md"
        dir = os.path.dirname(file_name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(str(self.md_format()))
            self.save_chart_day_candle()

    def to_md_file2(self):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        file_name = f"{uc.base_data_path}/stock_info/s{dd}/{self.code}_{self.name}_{dd}.md"
        dir = os.path.dirname(file_name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(str(self.md_format()))
            self.save_chart_day_candle()

    def save_file_common(self, url, type):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        ddhh = datetime.datetime.now().strftime('%Y%m%d%H')

        file_name_dh = f"{uc.base_data_path}/stock_info/d{dd}/{self.code}_{self.name}_{ddhh}_{type}.png"
        file_name = f"{uc.base_data_path}/stock_info/d{dd}/{self.code}_{self.name}_{dd}_{type}.png"
        
        if os.path.exists(file_name_dh):
            uc.logger.debug("img down pass")
            pass
        else:
            uc.logger.debug("img down ing")
            response = requests.get(url)
            if response.status_code == 200:
                dir = os.path.dirname(file_name)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                with open(file_name_dh, 'w', encoding='utf-8') as file:
                    file.write('') # 빈파일 생성 캐쉬용.
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                print(f"이미지 다운로드가 완료되었습니다.({type})")
            else:
                print(f"이미지를 다운로드할 수 없습니다.({type})")
            

    def save_chart_day_candle(self):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        url = f"https://ssl.pstatic.net/imgfinance/chart/item/area/week/{self.code}.png"
        self.save_file_common(url, 'wd')
        url = f"https://ssl.pstatic.net/imgfinance/chart/item/candle/day/{self.code}.png"
        self.save_file_common(url, 'd')
        url = f"https://ssl.pstatic.net/imgfinance/chart/item/candle/week/{self.code}.png"
        self.save_file_common(url, 'w')
        url = f"https://ssl.pstatic.net/imgfinance/chart/item/candle/month/{self.code}.png"
        self.save_file_common(url, 'm')



    def loading(self):
        nn = datetime.datetime.now() # 현재 시간.
        dd = nn.strftime('%Y%m%d') # 현재 작업일자.
        mm = nn.strftime('%Y%m') # 현재 작업일자.
        ddhh = nn.strftime('%Y%m%d%H') # 일단 시간단위로...

        def get_stock_html():
            url = getCodeUrl(self.code)
            response = requests.get(url)
            return response.text
        
        def get_stock_jong_html():
            url = getCodeJongUrl(self.code)
            response = requests.get(url)
            return response.text
        
        self.naver_html = uc.file_cache_write(f"/naver_page/d-{dd}/stock_{self.name}_{self.code}-{ddhh}-source.txt", get_stock_html )
        self.naver_html_jong = uc.file_cache_write(f"/naver_page/m-{mm}/stock_{self.name}_{self.code}-source2.html", get_stock_html )
        
        soup = BeautifulSoup(self.naver_html, "html.parser")

        self.bean = StockDetailSoupObject(self.name, self.code, self.naver_html)
        b = self.bean

        self.upjong_name = b.upjong_name
        self.upjong_code = b.upjong_code


        self.market_sum = b.market_sum

        self.news_list = code_news.getNaverCodeNewsList(self.code)
        self.date = datetime.datetime.now()
        self.news_list_naver = code_news.getNaverNewsList(self.name)

        self.company_info = b.company_info
        self.company_price = b.company_price
        self.company_price_up = b.company_price_up
        self.company_price_up_per = b.company_price_up_per

        self.trade_price = b.trade_price
        self.today_price = b.today_price


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
    
    def memo_format(self):
        dd = datetime.datetime.now().strftime('%Y%m%d')
        typeName = getTypeName(self.type)
        news_str = '\n'.join(str(news.md_format()) for news in self.news_list)
        naver_new_str = '\n'.join(str(news.md_format()) for news in self.news_list_naver)

        stock_trade_rate = 10
        frighner_rate = 10
        main_name = "대주주"
        main_holding_rate = f"{main_name} = 10"

        if ( self.upjong_name ):
            upjong_str = f"업종 : {self.upjong_name}({self.upjong_code})"
        else:
            upjong_str = ""

        return f"""테마: {self.upjong_name}

[{dd}] 특징주,
거래대금({dd}) : {self.trade_price}

시총 : {self.market_sum}
유동 비율 : {stock_trade_rate}
외국인 지분율 : {frighner_rate}
대주주 지분율 : {main_holding_rate}

회사소개 : {self.company_info}
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

        sample = f"""

차트 이미지: https://ssl.pstatic.net/imgfinance/chart/item/candle/day/033790.png
차트 이미지 wd: 

![{self.code}_{self.name}_{dd}.png](./{self.code}_{self.name}_{dd}_wd.png)

차트 이미지 d: 

![{self.code}_{self.name}_{dd}.png](./{self.code}_{self.name}_{dd}_d.png)

차트 이미지 w: 

![{self.code}_{self.name}_{dd}.png](./{self.code}_{self.name}_{dd}_w.png)

차트 이미지 m: 

![{self.code}_{self.name}_{dd}.png](./{self.code}_{self.name}_{dd}_m.png)

"""
        

        return f"""
## {typeName} : [{self.name}({self.code})]({self.url})

    {upjong_str}
    시가총액 : {self.market_sum}
    거래대금 : {self.trade_price}
    금일 가격 : {self.company_price}, 전일대비 {self.company_price_up}, 상승율 {self.company_price_up_per}
    기업개요 : {self.company_info}

*****

![{self.code}_{self.name}_{dd}.png](./d{dd}/{self.code}_{self.name}_{dd}_wd.png)

![{self.code}_{self.name}_{dd}.png](./d{dd}/{self.code}_{self.name}_{dd}_d.png)

![{self.code}_{self.name}_{dd}.png](./d{dd}/{self.code}_{self.name}_{dd}_w.png)

![{self.code}_{self.name}_{dd}.png](./d{dd}/{self.code}_{self.name}_{dd}_m.png)

*****

* 종목 뉴스

*****

{news_str}

*****

* 네이버 뉴스 : {self.date}

*****

{naver_new_str}

*****

"""



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
    sd = StockDetail(1, name, code)

    # print("종가:", sd.today_price)

    # sd.to_md_file()
    # print(sd.to_file())
    # print(sd.to_md_file2())
