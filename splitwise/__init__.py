import logging


def configLogger():
    logging.basicConfig()
    logger = logging.getLogger("splitwise")
    logger.setLevel(logging.DEBUG)
