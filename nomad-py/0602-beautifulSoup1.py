from email import header
import requests as rq
from bs4 import BeautifulSoup as bs

url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs#job-listings"

res = rq.get(url)

soup = bs(res.content, "html.parser")

jobs = soup.find("section", class_="jobs", id="category-2").find_all("li")

# print(jobs)

# 6.2 BeautilfulSoup

# 6.3 jobs
## [1:-1], 처음과 마직막을 걸러내기.
## a,b,c = [1,2,3] 리스트를 각 변수로 내보내기.

# 6.4 recap
## jobs_list(job_dict) 형태의 데이터로 만들기.
## company, position, region, url 4개의 속성을 갖는다.

# 6.5 Pagination.
## find pagination tag and get count.
## for x in range(page_count): loop pages.
## page scrape function, page count function create.

# 6.6 code challenge
## remoteok site. find keywords [flutter, python, golang] and url structures.
## site is blocking. no header info.(browser default string)

url2 = "https://remoteok.com/remote-flutter-jobs"
# res2 = rq.get(url2) # block 429??? too many requests
res2 = rq.get(url2, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"})

print(res2.content)
print(res2.status_code)


# 6.7 dynamic scraping : python.
## only python install.

# 6.8 playwright
## pip install playwright beautifulsoup4

# 6.9 keyword arguments.
## argument kind.
### positional  argument
### keyword argument.
## wanted.co.kr
### mission :: 로딩, 클릭, typing, entering, wait and find. scrolling 3 times.

# 6.10 interactiviti
## get_by_placeholder
## page.click("selector"), page.locator("selector").click();
## fill("flutter")
## selector.down("Enter") key event.
## selector.down("End") key event and scroll end.
## time.sleep

# 6.11 collecting jobs. bs4.
## bs4 ref: 6.3. easy.

# 6.12 exporting to excel.
## csv
## excel
## csv.writecsv
## dictionary to values(values) dict.values()
## dictionary to keys(title) dict.keys()
## file = open("filename.csv", mode="w")
## writer = csv.writer(file)
## writer.writerow(job.values())
## file.close()

# 6.13 code challenge.
## 일단 스킵. 주식 정보도 하기 바쁘다.
## gist.github.com
### Code Challenge
#### main.py
#### paste source
#### Create secret gist. ( gen url )

