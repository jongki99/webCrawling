import requests
from bs4 import BeautifulSoup

def main():
    # 크롤링할 웹페이지의 URL
    url = 'https://www.naver.com'  # 크롤링하려는 웹페이지의 URL을 여기에 입력하세요.

    # 웹페이지에 GET 요청 보내기
    response = requests.get(url)

    print(response.status_code)

    # 응답의 상태 코드를 확인하여 정상적으로 응답을 받았는지 확인
    if response.status_code == 200:
        # 응답의 HTML을 BeautifulSoup을 사용하여 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 웹페이지에서 원하는 내용 추출하기
        # 예를 들어, 여기서는 제목과 해당 링크를 추출합니다.
        # 웹페이지의 구조에 따라 적절히 수정하세요.
        titles = soup.find_all('title') # , class_='post-title')  # 예시: 웹페이지에서 제목이 <h2 class="post-title"> 태그에 있는 경우
        for title in titles:
            # 제목 출력
            print("제목:", title.text.strip())
            # 링크 출력
            # print("링크:", title.a['href'])  # 예시: 제목이 <a> 태그 안에 들어 있는 경우

    else:
        print("오류:", response.status_code)


if __name__ == "__main__":
    main()
