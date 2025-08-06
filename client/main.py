import time
from client import logger

def run_worker():
    logger.info("Client running..")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    run_worker()
    logger.info("Exit...")