# slack_test.py
# 이 스크립트는 Slack Webhook URL을 사용하여 Slack에 메시지를 전송하는 테스트를 수행합니다

# [사용법]
# 1. .env 파일에 SLACK_WEBHOOK_URL을 설정합니다.
# 2. 이 스크립트를 실행하여 Slack에 메시지를 전송합니다.

import os
import requests
from dotenv import load_dotenv

load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

payload = {
    "text": "✅ Slack Webhook 테스트 메시지입니다! (개별 테스트)"
}

try:
    res = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    print(f"[테스트] 응답 코드: {res.status_code}")
    print(f"[테스트] 응답 본문: {res.text}")
except Exception as e:
    print(f"[테스트] Slack 예외 발생: {type(e).__name__} - {e}")
