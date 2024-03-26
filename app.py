import sys
import os
import threading
import time
from random import randint
from flask import Flask, request, redirect
from logging.handlers import RotatingFileHandler
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
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
    app.logger.info('--- PYTHON APPLICATION START ---')
    app.logger.info('This logging App for Log Service')

    randomSec = randint(5, 30)
    logging_interval_minutes = int(os.getenv('LOGGING_INTERVAL_SECOND', randomSec))

    app.logger.info('Logging interval set to %d seconds', logging_interval_minutes)

    # 주어진 간격(초)마다 로깅을 수행
    app.logger.info('Waiting for %d second(s) before logging again...', logging_interval_minutes)
    time.sleep(logging_interval_minutes)

    randomSec = randint(1, 30)
    logging_interval_minutes = int(os.getenv('LOGGING_INTERVAL_SECOND', randomSec))
    app.logger.info('---- Time is TicTok ----')
    return 'Check the logs!'


@app.teardown_request
def teardown_request(exception=None):
    if exception:
        logger.error('An error occurred during request processing: %s', exception)
    else:
        logger.info('Request processed successfully')


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
    app.run(debug=False)
