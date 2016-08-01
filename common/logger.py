#!/usr/bin/python
"""
the logger module (logging encapsulated)
"""

import logging
import logging.handlers
import os

# global variables
log_formatter = None
log_handler = None


def init(log_home, log_file):
    global log_formatter, log_handler

    if os.path.exists(log_home) == False:
        print "create the log dir home"
        os.mkdir(log_home)

    log_file_name = log_home + log_file

    log_formatter = logging.Formatter('%(asctime)-15s %(levelname)s %(name)s -- %(message)s')
    log_handler = logging.handlers.RotatingFileHandler(log_file_name, maxBytes=50*1024*1024, backupCount=6)
    log_handler.setFormatter(log_formatter)


def get_logger(name, log_level=logging.DEBUG):
    if log_formatter == None:
        print "the log has not been initialized"
        return None
    
    logger = None
    if len(name) == 0:
        logger = logging.getLogger()
    else:
        logger = logging.getLogger(name)

    logger.setLevel(log_level)
    logger.addHandler(log_handler)
    return logger


if __name__ == "__main__":
    init("../logs/", "logger.log")

    mock_logger = get_logger("test.demo")
    mock_logger.debug("this is a debug log")
    mock_logger.info("this is a info log")
    mock_logger.warning("this is a warning log")
    mock_logger.error("this is a error log")

    toy_logger = get_logger("test.toy")
    toy_logger.info("i am a toy")
