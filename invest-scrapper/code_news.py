from playwright.sync_api import sync_playwright
import requests, re, time
from bs4 import BeautifulSoup


class NewsInfo:
    def __init__(self, title, where, date):
        self.title = title.strip()
        self.where = where.strip()
        self.date = date.strip()
    
    # def __str__(self):
    #     return f"{self.title}, {self.from}"

    def __str__(self):
        return f"{self.title}, {self.where}, {self.date}"
    
    def md_format(self):
        return f"   * **{self.title}**, ({self.where}, {self.date})"


class NaverNewsInfo(NewsInfo):
    def __init__(self, title, where, date, url):
        super().__init__(title, where, date)
        self.url = url

    def __str__(self):
        return super().__str__() + f", {self.url}"
    
    def md_format(self):
        return f"   * **[{self.title}]({self.url})**, ({self.where}, {self.date})"


# 일단 이건 안 씀... iframe 이 었나??? 맞네..
def getHtmlComplete(url):
    p = sync_playwright().start()
    # browser = p.chromium.launch(headless=False)
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    return page.content()



def getNaverCodeNewsList(code):
    url = f"https://finance.naver.com/item/news_news.naver?code={code}&page=1"

    # html = getHtmlComplete(url)
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    news_list = soup.select("td.title a")

    # print(news_list)

    newsInfo_list = []
    for anews in news_list:
        where = anews.parent.next_sibling.next_sibling
        date = where.next_sibling.next_sibling

        # print(1, anews, 2, where, 3, date)

        newsInfo = NewsInfo( title=anews.text, where=where.text, date=date.text)
        # print(newsInfo)
        newsInfo_list.append(newsInfo)

    return newsInfo_list


def getNaverNewsList(query):
    # url = f"https://search.naver.com/search.naver?where=news&query={query}" # 이건 요약본인데... 상관없음.
    url = f"https://search.naver.com/search.naver?where=news&sm=tab_tnw&query={query}&sort=0&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&nso=so:r,p:all,a:all"

    # html = getHtmlComplete(url)

    print("source", url)

    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    news_list = soup.select("div.news_area")
    #print(news_list)

    newsInfo_list = []
    for news in news_list:
        atitle = news.select_one("a.news_tit")
        title = atitle.text
        link = atitle.attrs["href"]

        where = news.select_one("a.press").text
        date = news.select_one("div.info_group span.info").text

        #print(1, title, 2, where, 3, date, 4, link)

        newsInfo = NaverNewsInfo( title=atitle.text, where=where, date=date, url=link)
        # print(newsInfo)
        newsInfo_list.append(newsInfo)

    return newsInfo_list



if __name__ == "__main__":
#    html = getHtmlComplete("https://finance.naver.com/item/news.naver?code=033790")
#    print(html)
#    news_list = getNaverCodeNewsList("033790")
#    news_list = getNaverNewsList("스카이문스테크놀로지")
    news_list = getNaverNewsList("민테크")

    for news in news_list:
        print(news)

