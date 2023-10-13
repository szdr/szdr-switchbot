CREATE TABLE switchbot_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_datetime DATETIME,
    device_id VARCHAR(50),
    device_name VARCHAR(50),
    device_type VARCHAR(50),
    status JSON,
    INDEX log_datetime_index (log_datetime)
);