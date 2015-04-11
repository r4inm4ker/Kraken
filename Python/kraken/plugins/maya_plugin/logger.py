import logging
import sys
import types

import maya.OpenMaya as OpenMaya

LOGGER_PREFIX = 'kraken.mayaLogger'

thing = "blah"


class MayaLogger(logging.Logger):

    def fatal(self, msg, *args, **kwargs):
        self.log(45, msg, *args, **kwargs)

    def comment(self, msg, *args, **kwargs):
        self.log(5, msg, *args, **kwargs)


class MayaHandler(logging.Handler):

    def emit(self, record):

        if isinstance(record.msg, types.StringTypes):
            msg = self.format(record)
        else:
            record.msg = str(record.msg)
            msg = self.format(record)

        if record.levelno > logging.CRITICAL:
            OpenMaya.MGlobal.displayError(msg)
        elif record.levelno in [logging.ERROR, 45]:
            OpenMaya.MGlobal.displayError(msg)
        elif record.levelno > logging.WARNING:
            OpenMaya.MGlobal.displayWarning(msg)
        elif record.levelno > logging.INFO:
            OpenMaya.MGlobal.displayInfo(msg)
        elif record.levelno <= logging.DEBUG:
            OpenMaya.MGlobal.displayInfo(msg)
        else:
            OpenMaya.MGlobal.displayInfo(msg)


def getLogger(name=None):

    if name is None:
        return logging.getLogger(LOGGER_PREFIX)
    else:
        return logging.getLogger(LOGGER_PREFIX + '.' + name)


if not hasattr(sys, 'MAYA_LOGGING_CONFIGURED'):
    logging.setLoggerClass(MayaLogger)
    logging.addLevelName(45, 'FATAL')
    logging.addLevelName(5, 'COMMENT')
    logger = logging.getLogger()
    mayaHandler = MayaHandler()
    mayaHandler.setLevel(0)
    #fileHandler = logging.FileHandler(os.path.join(os.environ['XSI_USERHOME'], 'xsiScriptLog.txt'))
    #fileHandler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    #fileHandler.setLevel(45)
    logger.addHandler(mayaHandler)
    #log.addHandler(fileHandler)
    logger.setLevel(0)
    sys.MAYA_LOGGING_CONFIGURED = True
    logger = getLogger()