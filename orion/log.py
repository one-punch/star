import logging
import logging.config


def logger():
    if "LOGGER" in globals():
        return LOGGER
    else:
        global LOGGER
        logging.config.fileConfig("logging.conf")
        LOGGER = logging.getLogger("orion")
        return LOGGER
