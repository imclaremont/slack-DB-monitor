# 준비 사항
- [Slack Webhook URL](https://api.slack.com/messaging/webhooks) 생성 후 `.env` 파일에 저장
- `.env` 파일에 **MySQL 접속 정보** (`user`, `password`, `host`, `port`, `db`) 추가

(예시)
```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=test_db

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
```

<br>

# 실행 절차
### 1. 테스트용 데이터베이스 생성
CREATE DATABASE test_db;

### 2. 더미 테이블 생성 + 샘플 데이터 삽입
mysql -u root -p test_db < test_db_init.sql

### 3. 패키지 설치
pip install -r requirements.txt

### 4. 모니터링 테이블 생성
python monitoring_setup.py

### 5. 성능 모니터링 실행
python performance_monitor.py

(느린 쿼리 감지 시 Slack으로 실시간 알림 전송, 하루 1회 리포트 시각화 생성)

<br>

## + 슬랙 수동 테스트
python slack_test.py

(.env에 등록된 SLACK_WEBHOOK_URL로 테스트 메시지가 전송)

## ++ 쿼리 성능 테스트 수동 실행
python test_run.py

(슬로우 쿼리를 수동으로 실행해 Slack 알림이 정상 동작하는지 확인)
