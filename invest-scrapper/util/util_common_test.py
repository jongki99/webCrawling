""" 패키지 주석은 여기에... 함수 목록을 나열해야 하나???

주저리 주저리...
이렇게 하면 개행 안됨.

이렇게 한줄 더 띄워써야 함.
"""
import util_common as util

def func1():
    """여기에는 함수 주석. title

    이렇게 주저리 주저리.
    """
    print('test 1')
    test = 1234
    util.logger.info(f"logger test={test}")
    return 'test 2'

util.check_and_create_folder(util.base_data_path + '/util_common_test1/test.txt')

text = util.file_cache_write(
    base_path=util.base_data_path,
    file_path1="/util_common_test/test1.txt",
    func_text_return=func1
)

""" 파이선 주석 처리 방법. 2024-05-28


**** 환경변수 설정 및 가져오기.
window : https://m.blog.naver.com/kamzzang1/221872888840
mac : https://stackoverflow.com/questions/4808809/how-to-fetch-environment-variables-in-mac-os-x-using-python
    zsh = > ~/.zshrc >> export VAR1 = "value1"


**** lambda, inline함수, 클로져. callback.
기본 : https://nowonbun.tistory.com/652
https://soma0sd.tistory.com/category/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D/%ED%8C%8C%EC%9D%B4%EC%8D%AC

**** lambda 도 있네... 조금 느낌이 나르지만... 이건 아직...
    간단한 수식을 쉽게 작성하기 위한 anonymous 함수 같은 느낌. 나중에 더 자세히...
    간단한 예러 map(함수, list) 함수에서 list 를 파라미터로 연산을 처리를 간단히 처리하기 위해 제공. 하는듯...
    lambda 매개변수 : 표현식


**** logger, console out coloring 설정까지.
기본 : https://wisdomcoder.oopy.io/806105a4-d0e0-4dad-b8bc-12529c123049
console coloring : https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

**** 파이선 주석.
에디터가 지원하는 포멧과 이를 보는 방법을 알았다.


**** 파이썬에도 enum 이 있다.

언어기본이 아니라서...
참조 : https://velog.io/@swhan9404/python-Enum

from enum import Enum 을 하고, 클래스를 만들면서 Enum 을 상속하는 형태로 한다. 실제 클래스는 아니라고 한다.
name, value 쌍을 가지며, value 는 숫자로 하는것 같다.

확장은 ... 아래와 같이 ( 속성을 여러개 넣는다. )
    FIEDL = ("field 1", "field 2", "field 3")

class Test(Enum):
    ENUM_1 = ("1", "2", "3")
    def __inif__(self, f1, f2, f3):
        self.field1 = f1
        self.field2 = f2
        self.field3 = f3
    ... good 좋은데...

    @classmothod
    def get_static_method(cls) # cls 가 self 느낌인데???? static 함수의 자기자신 참조. 이거 없으면??? 나중에....
        return cls.NUM_1
    def func1(self)
        return self.field1

value # ("1", "2", "3")
field1 # 1
Test.get_static_method() # 이런것도 가능하네... 좀 어렵네.
Test.NUM_1.func1() # enum 함수
"""