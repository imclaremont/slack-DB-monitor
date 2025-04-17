# performance_monitor.py
# DB 성능 모니터링 및 Slack 알림 시스템
# DB에 쿼리 성능을 기록하고, 주기적으로 성능 리포트를 생성합니다

import os
import time
import json
import pymysql
import requests
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# DB 및 Slack 설정 불러오기
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
    "charset": "utf8mb4"
}
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def create_monitoring_table():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS query_monitor (
                log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
                query_type VARCHAR(20),
                exec_time FLOAT,
                rows_examined INT,
                lock_time FLOAT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_created (created_at)
            ) ENGINE=InnoDB;
            """)
        conn.commit()
    finally:
        conn.close()

class DBAnalyzer:
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.thresholds = {
            'slow_query': 1000.0,
            'lock_warning': 0.1,
            'rows_warning': 1000
        }

    def _log_metrics(self, query_type: str, explain_result: dict):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO query_monitor
                (query_type, exec_time, rows_examined, lock_time)
                VALUES (%s, %s, %s, %s)
            """, (
                query_type,
                explain_result.get('exec_time', 0),
                explain_result.get('rows_examined', 0),
                explain_result.get('lock_time', 0)
            ))
        self.conn.commit()

    def _execute_with_monitoring(self, query: str, query_type: str):
        start = time.time()
        with self.conn.cursor() as cur:
            cur.execute(f"EXPLAIN FORMAT=JSON {query}")
            result = cur.fetchone()
            explain_json = json.loads(result[0])
            query_block = explain_json.get("query_block", {})
            cost_info = query_block.get("cost_info", {})
            query_cost = float(cost_info.get("query_cost", 0))
            rows_examined = query_block.get("table", {}).get("rows_examined_per_scan", 0)
            exec_time = time.time() - start
            if query_cost > self.thresholds['slow_query']:
                self._trigger_alert(f"Slow Query 발생!\n쿼리 비용: {query_cost}\n쿼리: {query}")
            explain_result = {
                'exec_time': exec_time,
                'rows_examined': rows_examined,
                'lock_time': 0
            }
            self._log_metrics(query_type, explain_result)
        return exec_time

    def _trigger_alert(self, message: str):
        print(f"[ALERT] {datetime.now()} - {message}")

        print(f"[DEBUG] SLACK_WEBHOOK_URL = {SLACK_WEBHOOK_URL}")

        payload = {
            "text": f"🚨 DB 성능 모니터링 알림\n시간: {datetime.now()}\n내용: {message}"
        }

        print(f"[DEBUG] PAYLOAD = {json.dumps(payload, indent=2)}")

        try:
            res = requests.post(SLACK_WEBHOOK_URL, json=payload)
            print(f"[Slack 응답] status={res.status_code}, text={res.text}")
        except requests.exceptions.RequestException as e:
            print(f"[Slack 예외 발생] {type(e).__name__}: {e}")

    def monitor_read_performance(self):
        query = """
        SELECT c.name, SUM(o.amount)
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        WHERE o.order_date > '2024-01-01'
        GROUP BY c.name
        """
        return self._execute_with_monitoring(query, 'SELECT')

    def monitor_write_performance(self):
        query = """
        INSERT INTO orders (customer_id, amount, order_date)
        VALUES (FLOOR(RAND()*10000), RAND()*1000, CURDATE())
        """
        return self._execute_with_monitoring(query, 'INSERT')

    def monitor_update_performance(self):
        query = """
        UPDATE customers SET email = CONCAT(name, '@new_domain.com')
        WHERE id IN (SELECT customer_id FROM orders WHERE amount > 500)
        """
        return self._execute_with_monitoring(query, 'UPDATE')

    def visualize_performance(self, hours: int = 24):
        with self.conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("""
            SELECT
                HOUR(created_at) AS hour,
                AVG(exec_time) AS avg_time,
                MAX(rows_examined) AS max_rows
            FROM query_monitor
            WHERE created_at > NOW() - INTERVAL %s HOUR
            GROUP BY hour
            """, (hours,))
            data = cur.fetchall()
        hours = [x['hour'] for x in data]
        plt.figure(figsize=(12, 6))
        plt.plot(hours, [x['avg_time'] for x in data], label='평균 실행시간')
        plt.bar(hours, [x['max_rows']/100 for x in data], alpha=0.3, label='최대 검색행(x100)')
        plt.xticks(range(24))
        plt.legend()
        plt.title('쿼리 성능 모니터링 리포트')
        plt.xlabel('시간대')
        plt.ylabel('지표')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    create_monitoring_table()
    analyzer = DBAnalyzer()
    last_report_date = datetime.now().date()
    
    try:
        while True:
            print(f"모니터링 시작: {datetime.now()}")
            analyzer.monitor_read_performance()
            analyzer.monitor_write_performance()
            analyzer.monitor_update_performance()
            time.sleep(5)  # 5초마다 실행
            now = datetime.now()
            if now.date() != last_report_date:
                analyzer.visualize_performance()
                last_report_date = now.date()
    except KeyboardInterrupt:
        print("모니터링 중지")
        analyzer.conn.close()
        print("DB 연결 종료")