from kraken.plugins.si_plugin.utils import *


class Handler(logging.Handler):
    """Logging Handler for Softimage."""

    def emit(self, record):

        msg = self.format(record)

        siLevel = constants.siComment
        if record.levelno == logging.CRITICAL:
            siLevel = constants.siFatal

        elif record.levelno == logging.ERROR:
            siLevel = constants.siError

        elif record.levelno == logging.WARNING:
            siLevel = constants.siWarning

        elif record.levelno == logging.INFO:
            siLevel = constants.siInfo

        elif record.levelno == logging.DEBUG:
            siLevel = constants.siVerbose

        else:
            siLevel = constants.siComment

        si.LogMessage(msg, siLevel)
