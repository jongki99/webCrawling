"""
네이버 증권 홈.
https://finance.naver.com/sise/sise_rise.naver

추세 파악용. 회사 분석.
https://finance.naver.com/sise/sise_rise.naver?sosok=1 --> 코스닥
https://finance.naver.com/sise/sise_rise.naver?sosok=0 --> 코스피

위 정보중에서 링크 찾아서 들어오면 됨.
필요한 정보 요약하도록...

https://finance.naver.com/item/main.naver?code=090460 --> 주식상세.
기업개요 버튼이 있어야 회사로??? 회사 요약 참고.

하락도 검토. 일단은 제외.


대상조건
    코스피
        10% 이상 10번째 이상인 경우.
    코스닥
        25% 이상 30번째 이상인 경우.
"""


import ranking_list as st

stocks = st.getTop40()

for index, stock in enumerate(stocks):
    stock.print()
    stock.save_md()

st.merge_txt_order_md(stocks)

