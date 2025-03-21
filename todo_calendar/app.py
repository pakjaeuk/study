from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# PostgreSQL 연결 정보
DB_CONFIG = {
    "dbname": "test_db",
    "user": "study",
    "password": "1q2w3e4r",
    "host": "localhost",
    "port": "5432"
}

# PostgreSQL 테이블 생성 (초기 실행 시 필요)
def create_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            date TEXT NOT NULL,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# 할 일 저장
@app.route('/add_todo', methods=['POST'])
def add_todo():
    data = request.json
    date = data['date']  # YYYY-MM-DD 형식
    task = data['task']

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (date, task) VALUES (%s, %s)", (date, task))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "할 일이 저장되었습니다!"})

# 선택된 연/월에 해당하는 할 일 불러오기
@app.route('/get_todos', methods=['GET'])
def get_todos():
    year = request.args.get('year')
    month = request.args.get('month')

    if not year or not month:
        return jsonify({})

    date_prefix = f"{year}-{month.zfill(2)}"  # YYYY-MM 형식

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT date, task FROM todos WHERE date LIKE %s", (date_prefix + "%",))
    todos = cur.fetchall()
    cur.close()
    conn.close()

    todo_dict = {}
    for date, task in todos:
        if date not in todo_dict:
            todo_dict[date] = []
        todo_dict[date].append(task)

    return jsonify(todo_dict)

# 기본 페이지 렌더링
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    create_table()  # 서버 실행 전 테이블 생성
    app.run(host='0.0.0.0', port=5000, debug=True)