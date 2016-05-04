
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

    handlerNames = [type(x).__name__ for x in logger.handlers]

    if 'DCCHandler' not in handlerNames:
        dccHandler = getLogHandler()
        if dccHandler is not None:
            logger.addHandler(dccHandler)

    if 'WidgetHandler' not in handlerNames:
        widgetHandler = WidgetHandler()
        if widgetHandler is not None:
            logger.addHandler(widgetHandler)

    return logger
