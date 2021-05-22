"""Logging adaptor"""
import logging


logging.basicConfig(filename='./sparrow_player.log',
                    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
                    datefmt='%b-%d %H:%M:%S',
                    level=logging.DEBUG)


def get_logger(name=None):
    """get_logger"""
    return logging.getLogger(name)
