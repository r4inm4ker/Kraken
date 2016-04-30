
import logging

from kraken.plugins import getLogHandler


def getLogger(name):
    """Get's a logger and attaches the correct DCC compatible Handler.

    Args:
        name (str): Name of the logger to get / create.

    Returns:
        Logger: Logger.

    """

    dccHandler = getLogHandler()
    logger = logging.getLogger(name)
    if dccHandler not in logger.handlers:
        logger.addHandler(dccHandler)

    return logger
