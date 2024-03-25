from random import randint
from flask import Flask, request
from logging.handlers import RotatingFileHandler
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 로그 핸들러 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = RotatingFileHandler('/var/log/app.log', maxBytes=1024 * 1024 * 100, backupCount=20)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
app.logger.addHandler(console_handler)

# 예제 라우트
@app.route('/')
def index():
    app.logger.debug('This is a DEBUG message')
    app.logger.info('This is an INFO message')
    app.logger.warning('This is a WARNING message')
    app.logger.error('This is an ERROR message')
    return 'Check the logs!'



@app.route("/rolldice")
def roll_dice():
    player = request.args.get('player', default=None, type=str)
    result = str(roll())
    print('시작')
    app.logger.info('시자악합니다')
    if player:
        print('성공!!!!')
        app.logger.warning("%s is rolling the dice: %s", player, result)
    else:
        print('실패!!!!')
        app.logger.warning("Anonymous player is rolling the dice: %s", result)
    return result


def roll():
    return randint(1, 6)


if __name__ == '__main__':
    app.logger.info('min')
    app.run()
