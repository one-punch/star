import logging
import logging.config


def logger():
    logging.config.fileConfig("logging.conf")
    return logging.getLogger("orion")
