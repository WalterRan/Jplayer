import logging


logging.basicConfig(filename='./jplayer.log',
                    format='%(asctime)s %(levelname)s [%(name)s] %(message)s', datefmt='%b-%d %H:%M:%S',
                    level=logging.DEBUG)


def getLogger(name=None):
    return logging.getLogger(name)

