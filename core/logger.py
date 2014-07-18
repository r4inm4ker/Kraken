import logging
import os
import sys
import types

LOGGER_PREFIX = 'kraken.pyLogger'


class PyLogger(logging.Logger):

    def fatal(self, msg, *args, **kwargs):
        self.log(45, msg, *args, **kwargs)

    def comment(self, msg, *args, **kwargs):
        self.log(5, msg, *args, **kwargs)


class PyHandler(logging.Handler):

    def emit(self, record):

        if isinstance(record.msg, types.StringTypes):
            msg = self.format(record)
        else:
            record.msg = str(record.msg)
            msg = self.format(record)

        print msg


def getLogger(name=None):

    if name is None:
        return logging.getLogger(LOGGER_PREFIX)
    else:
        return logging.getLogger(LOGGER_PREFIX + '.' + name)


if not hasattr(sys, 'PY_LOGGING_CONFIGURED'):
    logging.setLoggerClass(PyLogger)
    logging.addLevelName(45, 'FATAL')
    logging.addLevelName(5, 'COMMENT')
    logger = logging.getLogger()
    pyHandler = PyHandler()
    pyHandler.setLevel(0)
    #fileHandler = logging.FileHandler(os.path.join(os.environ['XSI_USERHOME'], 'xsiScriptLog.txt'))
    #fileHandler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    #fileHandler.setLevel(45)
    logger.addHandler(pyHandler)
    #log.addHandler(fileHandler)
    logger.setLevel(0)
    sys.PY_LOGGING_CONFIGURED = True
    logger = getLogger()