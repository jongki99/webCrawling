"""프로그램 공통 유틸리티, 많은 것을 넣겠지?

logger : command color 를 사용하여 출력하도록 함.
base_data_path : 컴퓨터 환경정보에 데이터 폴더를 만들고, 설정해서 사용가능하게끔 만들어서 사용할수 있도록 했다.
    집에서는 다른 변수를 설정하고, 사용하도록 한다.
    원래는 s3 등에 넣을 수 있도록 해야 하는데... 일단은 ...
def check_and_create_folder : file_path 에서 디렉토리 부분만 만들어주는 함수.
def file_cache_write : 크롤링용으로 html 을 반복해서 불어오지 않도록 캐쉬하는 역활. 이거 캐쉬기능을 찾아보면 더 좋은게 있을거 같은데... 일단은...

이렇게 패키지 주석을 넣는 것이란다. 일단 배우는 거지.
일단 vscode 에서는 이렇게 하니까 잘 보여주네...

java 베이스로 알아보면 대부분 있네.. enum 도 그렇고, 하지만 enum 이 좀 제한도 많고, 학습 곡선이 필요하네.
"""
import requests, re, datetime, time, os
import logging


base_data_path = os.getenv("MY_INVEST_DATA_PATH")

# log_format = '%(asctime)s [%(filename)s:%(lineno)s|%(levelname)s] %(funcName)s(): %(message)s'
# logging.basicConfig(format=log_format, level=logging.DEBUG)

class CustomFormatter(logging.Formatter):

    white= "\x1b[45;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    # format = log_format
    format = '%(asctime)s [%(filename)s:%(lineno)s|%(levelname)s] %(funcName)s(): %(message)s' # 컬러와 기본 2개 찍힘. ㅜ.ㅜ
    # format = '%(asctime)s [%(filename)s:%(lineno)s|%(levelname)s] %(funcName)s(): %(message)s' # 컬러와 기본 2개 찍힘. ㅜ.ㅜ
    # format = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: white + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# create logger with 'spam_application'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)


def check_and_create_folder(file_path):
    """ 주석은 이렇게 해야 하는 걸로... 줄을 나눠야 개행처리가 되네... 이건 좀...
    이렇게 하면 개행처리가 안된다... ㅜ.ㅜ

    파일을 가지는 경로에서 맨뒤에 / 가 없어야 하겠지?

    파일을 제외하고, 경로를 생성하는 함수.

    file_path : 파일 경로를 가지는 string path.
    """
    # 을 넣어도 주석으로는 안된다.
    # 파일이 포함된 폴더의 경로 추출
    folder_path = os.path.dirname(file_path)
    
    # 폴더가 존재하는지 확인
    if not os.path.exists(folder_path):
        # 폴더가 존재하지 않으면 생성
        try:
            os.makedirs(folder_path)
            print(f"폴더가 생성되었습니다: {folder_path}")
        except OSError as e:
            print(f"폴더를 생성하는 동안 오류가 발생했습니다: {e}")
    else:
        print(f"폴더가 이미 존재합니다: {folder_path}")

def file_cache_write(file_path, func_text_return=None):
    """ 함수 주석은 이렇게 안에다가 넣어주면 된. 패키지는 파일안쪽이니까 이것도 나름 일관성은 있네...

    이 함수는 베이스 환경변수를 기준으로 캐쉬할수 있도록 하는 임시저장용 파일 저장 함수이다.
    file_path : 임시폴더의 하위 경로를 반환한다. ( 임시폴더는 환경변수로 지정한다. )
    func_text_return : 콜백함수, 캐쉬할 text 를 반환하는 함수로 캐쉬가 되어 있지 않다면 함수를 실행하고, 그외는 파일에서 읽어서 리턴하도록 한다.
    """
    base_path = base_data_path
    text = None

    if ( not func_text_return ):
        return ''

    file_path = base_path + file_path
    check_and_create_folder(file_path)

    if not os.path.exists(file_path):
        logger.info("none file_path=%s", file_path)
        text = func_text_return()
        # w 덮어쓰기, a 추가하기.
        with open(file_path, "w") as file: 
            file.write(text)
    else:
        logger.info("exists file_path=%s", file_path)
        with open(file_path, "r") as file:
            text = file.read()

    return text


if __name__ == "__main__": # 회사정보를 parsing 테스트 할때 사용하는 코드.

    # 경로 확인.
    print(base_data_path)
    # 로거 테스트.
    logger.debug(base_data_path)
    logger.info(base_data_path)
    logger.warning(base_data_path)
    logger.error(base_data_path)
    logger.fatal(base_data_path)

    # 기본 경로의 하위에 파일패스의 값으로 폴더 및 파일에서 폴더를 생성하고, 파일을 쓰기 모드로 설정하고, 파일 쓰기 작업을 처리.
    # base_data_path, file_path, text

    dd = datetime.datetime.now().strftime('%Y%m%d')

    def test1():
        return 'test1'

    text = file_cache_write(
        base_path=base_data_path,
        file_path1="/test/sample/test/good.txt",
        func_text_return=test1
    )

    print(text)
