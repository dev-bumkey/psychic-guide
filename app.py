import sys
import os
import time
from random import randint
from flask import Flask, request, redirect
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 콘솔 핸들러
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
app.logger.addHandler(console_handler)


# # 로그 핸들러 설정
# file_handler = RotatingFileHandler('/var/log/app.log', maxBytes=1024 * 1024 * 100, backupCount=20)
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# app.logger.addHandler(file_handler)


# 예제 라우트
@app.route('/')
def index():
    app.logger.warning('--- PYTHON APPLICATION START ---')
    app.logger.debug('This logging App for Log Service')

    randomSec = randint(1, 5)
    logging_interval_minutes = int(os.getenv('LOGGING_INTERVAL_SECOND', randomSec))

    while randomSec < 30:
        # 환경 변수에서 로깅 간격(초)을 읽기

        app.logger.info('Logging interval set to %d seconds', logging_interval_minutes)

        # 주어진 간격(초)마다 로깅을 수행
        app.logger.info('Waiting for %d second(s) before logging again...', logging_interval_minutes)

        time.sleep(logging_interval_minutes)

        randomSec = randint(1, 10)
        logging_interval_minutes = int(os.getenv('LOGGING_INTERVAL_SECOND', randomSec))
        app.logger.info('---- Time is TicTok ----')


@app.route("/rolldice")
def roll_dice():
    player = request.args.get('player', default=None, type=str)
    result = str(roll())
    app.logger.info('시작')
    if player:
        app.logger.warning("%s is rolling the dice: %s", player, result)
    else:
        app.logger.warning("Anonymous player is rolling the dice: %s", result)
    return result


def roll():
    return randint(1, 6)


if __name__ == '__main__':
    app.run()
