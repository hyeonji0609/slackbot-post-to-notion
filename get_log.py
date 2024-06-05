import logging
from datetime import datetime

class Logger:
    def __init__(self, name='db_logger', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 콘솔 출력 핸들러 설정
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # 포맷터 설정
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # 핸들러를 로거에 추가
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger