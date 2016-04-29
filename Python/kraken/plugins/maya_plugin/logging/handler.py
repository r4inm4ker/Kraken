import types

from kraken.plugins.maya_plugin import *


class Handler(logging.Handler):
    """Logging Handler for Maya."""

    def emit(self, record):
        pass
        # siLevel = constants.siComment

        # if record.levelno == logging.CRITICAL:
        #     siLevel = constants.siFatal
        # elif record.levelno == logging.ERROR:
        #     siLevel = constants.siError
        # elif record.levelno == logging.WARNING:
        #     siLevel = constants.siWarning
        # elif record.levelno == logging.INFO:
        #     siLevel = constants.siInfo
        # elif record.levelno == logging.DEBUG:
        #     siLevel = constants.siVerbose
        # else:
        #     siLevel = constants.siComment

        # if isinstance(record.msg, types.StringTypes):
        #     msg = self.format(record)

        # else:
        #     record.msg = str(record.msg)
        #     msg = self.format(record)

        # xsi.LogMessage(msg, siLevel)