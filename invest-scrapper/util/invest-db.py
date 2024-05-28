import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('example.db')

# 커서 생성
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# 데이터 삽입
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 30))
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 25))

# 커밋
conn.commit()

# 데이터 조회
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 데이터 수정
cursor.execute("UPDATE users SET age = ? WHERE name = ?", (31, 'Alice'))
conn.commit()

# 데이터 삭제
cursor.execute("DELETE FROM users WHERE name = ?", ('Bob',))
conn.commit()

# 연결 닫기
conn.close()



if __name__ == "__main__2": # 회사정보를 parsing 테스트 할때 사용하는 코드.
    pass
