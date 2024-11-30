from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import util_common as uc

# 데이터베이스 엔진 생성 (SQLite 파일 사용)
source_file = f"{uc.base_data_path}/stock_db/stock_code_name.db"
engine = create_engine(F'sqlite:///{source_file}', echo=True)

# ORM의 베이스 클래스 생성
Base = declarative_base()

# 데이터 모델 정의
class StockCode(Base):
    __tablename__ = 'stock_code'  # 테이블 이름 설정
    code = Column(String, primary_key=True)
    name = Column(String)
    marketType = Column(String)

    def __repr__(self):
        return f"<StockCode(code={self.code}, name={self.name}, marketType={self.marketType})>"

# 데이터베이스 테이블 생성
Base.metadata.create_all(engine)

# 세션 생성
Session = sessionmaker(bind=engine)
session = Session()

# 데이터 삽입, 샘플.
new_stockCode = StockCode(code='000500', name='가온전선', marketType='KOSPI')
session.add(new_stockCode)
session.commit()

# 데이터 조회, 샘플.
stockCodes = session.query(StockCode).all()
for stockCode in stockCodes:
    print(stockCode)

# 데이터 업데이트
stockCode_to_update = session.query(StockCode).filter_by(name='가온전선').first()
if stockCode_to_update:
    stockCode_to_update.marketType = 'KOSDAQ'
    session.commit()

# 데이터 삭제
# stockCode_to_delete = session.query(StockCode).filter_by(name='가온전선').first()
# if stockCode_to_delete:
#     session.delete(stockCode_to_delete)
#     session.commit()

