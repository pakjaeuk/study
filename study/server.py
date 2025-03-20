from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS 활성화

# PostgreSQL 데이터베이스 연결 정보
DB_CONFIG = {
    "dbname": "test_db",
    "user": "study",
    "password": "1q2w3e4r",
    "host": "localhost",
    "port": "5432"
}

# 테이블 생성 함수
def create_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS TB_eat_lunch (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            menu TEXT NOT NULL,
            price INT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# create_table()  # 서버 실행 시 테이블 생성 확인

# 점심 기록 추가 API
@app.route('/add_lunch', methods=['POST'])
def add_lunch():
    data = request.json
    date = data.get("date")
    menu = data.get("menu")
    price = data.get("price")

    if not date or not menu or price is None:
        return jsonify({"error": "Invalid input"}), 400

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO TB_eat_lunch (date, menu, price) VALUES (%s, %s, %s)", (date, menu, price))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "등록 완료"}), 201

# 점심 기록 조회 API
@app.route('/get_lunch', methods=['GET'])
def get_lunch():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT date, menu, price FROM TB_eat_lunch ORDER BY date ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = [{"date": str(row[0]), "menu": row[1], "price": row[2]} for row in rows]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
