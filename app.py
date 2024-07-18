import sys
import os
import threading
import time
import logging
from logging.handlers import RotatingFileHandler
from random import randint
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()
# logger = logging.getLogger(__name__)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# formatter1 = logging.Formatter('Stream :  "%(asctime)s - %(levelname)s - %(message)s')
#
# # 콘솔 핸들러
# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.setLevel(logging.DEBUG)
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)
# logger.setLevel(logging.DEBUG)

# 스트림 핸들러 (Uvicorn 액세스 로거용)
# stream_handler = logging.StreamHandler(sys.stdout)
# stream_handler.setLevel(logging.DEBUG)
# stream_handler.setFormatter(formatter1)

# uvicorn_access_logger = logging.getLogger("uvicorn.access")
# uvicorn_access_logger.addHandler(stream_handler)
# uvicorn_access_logger.setLevel(logging.DEBUG)

# 백그라운드 스레드와 루프를 컨트롤할 플래그
keep_running = True
loop_thread = None

def get_logging():
    # Create Logger
    logger = logging.getLogger()
    level = "INFO"

    # Check handler exists
    if len(logger.handlers) > 0:
        # Logger already exists
        return logger

    # Set Logger Level
    logger.setLevel(level)

    # Set Logger Format
    formatter = logging.Formatter("%(levelname)s %(asctime)s [%(filename)s > %(funcName)s function > %(lineno)d line] - %(message)s")

    # Create Handlers
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    # Set Handlers to Logger
    logger.addHandler(stream_handler)

    return logger

logger = get_logging()

@app.get("/")
async def index():
    global loop_thread
    if loop_thread is None or not loop_thread.is_alive():
        # 루프 스레드가 없거나 종료되었을 때에만 새로운 스레드 시작
        loop_thread = threading.Thread(target=loop_function)
        loop_thread.start()
    logger.info('--- PYTHON APPLICATION START ---')
    logger.debug('This logging App for Log Service')
    return PlainTextResponse("Loop started")

def loop_function():
    global keep_running
    randomSec = randint(1, 10)
    logging_interval_minutes = int(os.getenv('LOGGING_INTERVAL_SECOND', randomSec))

    while keep_running:
        logger.error('Logging interval set to %d seconds', logging_interval_minutes)
        logger.warning('Waiting for %d second(s) before logging again...', logging_interval_minutes)
        time.sleep(logging_interval_minutes)
        randomSec = randint(1, 60)
        logging_interval_minutes = int(os.getenv('LOGGING_INTERVAL_SECOND', randomSec))
        logger.info('---- Time is TicTok ----')

@app.get("/rolldice")
async def roll_dice(request: Request):
    player = request.query_params.get('player')
    result = str(roll())
    logger.info('시작')
    if player:
        logger.warning("%s is rolling the dice: %s", player, result)
    else:
        logger.warning("Anonymous player is rolling the dice: %s", result)
    return PlainTextResponse(result)

def roll():
    return randint(1, 6)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
