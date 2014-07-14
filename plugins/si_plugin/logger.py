import logging
import os
import sys
import types

from win32com.client import constants
from win32com.client.dynamic import Dispatch

xsi = Dispatch("XSI.Application").Application
log = xsi.LogMessage

LOGGER_PREFIX = 'kraken.siLogger'


class XSILogger(logging.Logger):

    def fatal(self, msg, *args, **kwargs):
        self.log(45, msg, *args, **kwargs)

    def comment(self, msg, *args, **kwargs):
        self.log(5, msg, *args, **kwargs)


class XSIHandler(logging.Handler):

    def emit(self, record):
        if record.levelno == logging.CRITICAL:
            xsiLvl = constants.siFatal
        elif record.levelno in [logging.ERROR, 45]:
            xsiLvl = constants.siError
        elif record.levelno == logging.WARNING:
            xsiLvl = constants.siWarning
        elif record.levelno == logging.INFO:
            xsiLvl = constants.siInfo
        elif record.levelno == logging.DEBUG:
            xsiLvl = constants.siVerbose
        else:
            xsiLvl = constants.siComment

        if isinstance(record.msg, types.StringTypes):
            msg = self.format(record)
        else:
            record.msg = str(record.msg)
            msg = self.format(record)

        log(msg, xsiLvl)


def getLogger(name=None):

    if name is None:
        return logging.getLogger(LOGGER_PREFIX)
    else:
        return logging.getLogger(LOGGER_PREFIX + '.' + name)


if not hasattr(sys, 'SI_LOGGING_CONFIGURED'):
    logging.setLoggerClass(XSILogger)
    logging.addLevelName(45, 'FATAL')
    logging.addLevelName(5, 'COMMENT')
    logger = logging.getLogger()
    xsiHandler = XSIHandler()
    xsiHandler.setLevel(0)
    #fileHandler = logging.FileHandler(os.path.join(os.environ['XSI_USERHOME'], 'xsiScriptLog.txt'))
    #fileHandler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    #fileHandler.setLevel(45)
    logger.addHandler(xsiHandler)
    #log.addHandler(fileHandler)
    logger.setLevel(0)
    sys.XSI_LOGGING_CONFIGURED = True
    logger = getLogger()