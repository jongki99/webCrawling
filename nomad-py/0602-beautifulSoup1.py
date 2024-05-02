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
