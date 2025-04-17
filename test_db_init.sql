-- test_db_init.sql
-- 이 스크립트는 MySQL 데이터베이스를 초기화하고 샘플 데이터를 삽입합니다.

-- 데이터베이스 선택
USE test_db;

-- 1. 고객 테이블 생성
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
) ENGINE=InnoDB;

-- 2. 주문 테이블 생성
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    amount FLOAT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
) ENGINE=InnoDB;

-- 3. 모니터링 테이블 생성
CREATE TABLE IF NOT EXISTS query_monitor (
    log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    query_type VARCHAR(20),
    exec_time FLOAT,
    rows_examined INT,
    lock_time FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created (created_at)
) ENGINE=InnoDB;

-- 4. 샘플 고객 데이터 삽입
INSERT INTO customers (name, email)
VALUES 
('홍길동', 'hong@example.com'),
('이순신', 'lee@example.com'),
('강감찬', 'kang@example.com'),
('신사임당', 'shin@example.com'),
('김유신', 'kim@example.com'),
('윤봉길', 'yoon@example.com'),
('안중근', 'ahn@example.com'),
('유관순', 'ryu@example.com');

-- 5. 샘플 주문 데이터 삽입
INSERT INTO orders (customer_id, amount, order_date)
VALUES
(1, 500.0, '2024-01-02'),
(2, 300.0, '2024-02-03'),
(3, 900.0, '2024-03-10'),
(4, 1200.0, '2024-04-05'),
(5, 150.0, '2024-01-15'),
(6, 780.0, '2024-02-20'),
(7, 660.0, '2024-03-25'),
(8, 450.0, '2024-04-01'),
(1, 320.0, '2024-04-10'),
(2, 990.0, '2024-04-11');
