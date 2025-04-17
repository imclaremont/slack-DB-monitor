# test_run.py
# 이 코드는 performance_monitor.py의 기능을 테스트하는 스크립트입니다

from performance_monitor import DBAnalyzer, create_monitoring_table

# 테이블 생성
create_monitoring_table()

# 모니터링 인스턴스 생성
analyzer = DBAnalyzer()

# threshold 임시로 낮춰서 알림 무조건 뜨게 하기
analyzer.thresholds['slow_query'] = 1.0

# 테스트용 쿼리 날리기 (SELECT, INSERT, UPDATE)
analyzer.monitor_read_performance()
analyzer.monitor_write_performance()
analyzer.monitor_update_performance()
