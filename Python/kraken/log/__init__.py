
import logging

from kraken.log.widget_handler import WidgetHandler
from kraken.plugins import getLogHandler


def getLogger(name):
    """Get's a logger and attaches the correct DCC compatible Handler.

    Args:
        name (str): Name of the logger to get / create.

    Returns:
        Logger: Logger.

    """

    logger = logging.getLogger(name)

    dccHandler = getLogHandler()
    if dccHandler is not None:
        if dccHandler not in logger.handlers:
            logger.addHandler(dccHandler)

    handlerNames = [type(x).__name__ for x in logger.handlers]
    if 'WidgetHandler' not in handlerNames:
        widgetHandler = WidgetHandler()
        logger.addHandler(widgetHandler)

    return logger
