import sys
import os
import threading
import time
from logging.handlers import RotatingFileHandler
from random import randint
from flask import Flask, request, redirect
from flask import g
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 콘솔 핸들러
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)
# # 로그 핸들러 설정
# file_handler = RotatingFileHandler('/var/log/app.log', maxBytes=1024 * 1024 * 100, backupCount=20)
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)



# 백그라운드 스레드와 루프를 컨트롤할 플래그
keep_running = True
loop_thread = None
# 예제 라우트
@app.route('/')
def index():
    global loop_thread
    if loop_thread is None or not loop_thread.is_alive():
        # 루프 스레드가 없거나 종료되었을 때에만 새로운 스레드 시작
        loop_thread = threading.Thread(target=loop_function)
        loop_thread.start()
    logger.info('--- PYTHON APPLICATION START ---')
    logger.debug('This logging App for Log Service')
    return "Loop started"


def loop_function():
    global keep_running
    randomSec = randint(1, 10)
    logging_interval_minutes = int(os.getenv('LOGGING_INTERVAL_SECOND', randomSec))

    while keep_running:
        app.logger.error('Logging interval set to %d seconds', logging_interval_minutes)
        app.logger.warning('Waiting for %d second(s) before logging again...', logging_interval_minutes)
        time.sleep(logging_interval_minutes)
        randomSec = randint(1, 60)
        logging_interval_minutes = int(os.getenv('LOGGING_INTERVAL_SECOND', randomSec))
        app.logger.info('---- Time is TicTok ----')


@app.route("/rolldice")
def roll_dice():
    player = request.args.get('player', default=None, type=str)
    result = str(roll())
    logger.info('시작')
    if player:
        logger.warning("%s is rolling the dice: %s", player, result)
    else:
        logger.warning("Anonymous player is rolling the dice: %s", result)
    return result


def roll():
    return randint(1, 6)


if __name__ == '__main__':
    # log = logging.getLogger('werkzeug')
    # log.setLevel(logging.DEBUG)
    app.run(debug=False)
