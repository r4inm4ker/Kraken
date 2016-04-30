import logging

from kraken.plugins.maya_plugin.utils import *


class Handler(logging.Handler):
    """Logging Handler for Maya."""

    def emit(self, record):

        msg = self.format(record)
        if record.levelno > logging.WARNING:
            om.MGlobal.displayError(msg)

        elif record.levelno > logging.INFO:
            om.MGlobal.displayWarning(msg)

        else:
            om.MGlobal.displayInfo(msg)
