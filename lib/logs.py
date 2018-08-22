import logging
import os
from MyloggingHandler import MyloggingHandler
# from logging.handlers import TimedRotatingFileHandler

path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib'
init = False


def set_logger(name, filename='debug.log'):
    global init
    path = os.getcwd().split('cassia_automation')[0]
    file_name = path + "cassia_automation/logs/" + filename
    if os.path.exists(file_name):
        if not init:
            os.remove(file_name)
            init = True
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.DEBUG)
    if not logger.handlers:
        header = MyloggingHandler(
            file_name, when='H', interval=8, backupCount=3)
        format = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        header.setFormatter(format)
        header.suffix = "%Y-%m-%d_%H"
        header.setLevel(logging.DEBUG)
        logger.addHandler(header)
    return logger
