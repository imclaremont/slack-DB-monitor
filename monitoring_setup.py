# monitoring_setup.py
# .env 파일에서 DB 설정을 로드하고 pymysql을 사용하여 MariaDB 데이터베이스에 연결합니다

import os
import pymysql
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
    "charset": "utf8mb4"
}

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
        print("query_monitor 테이블 생성 완료!")
    finally:
        conn.close()

if __name__ == "__main__":
    create_monitoring_table()
