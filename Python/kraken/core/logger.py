import logging
import os
import sys
import types

LOGGER_PREFIX = 'kraken.pyLogger'


class PyLogger(logging.Logger):
    """Custom Python logger."""

    def fatal(self, msg, *args, **kwargs):
        self.log(45, msg, *args, **kwargs)

    def comment(self, msg, *args, **kwargs):
        self.log(5, msg, *args, **kwargs)


class PyHandler(logging.Handler):
    """Logger handler to map messages to correct commands."""

    def emit(self, record):
        """Emit messages using correct commands.

        Arguments:
        record -- Record, record to emit.

        Return:
        True if successful.

        """

        if isinstance(record.msg, types.StringTypes):
            msg = self.format(record)
        else:
            record.msg = str(record.msg)
            msg = self.format(record)

        print msg

        return True


def getLogger(name=None):
    """Returns the custom logger or creates it if it doesn't exist.

    Arguments:
    name -- String, name of the custom logger to get or create.

    Return:
    Custom logger.

    """

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
    logger.addHandler(pyHandler)
    logger.setLevel(0)
    sys.PY_LOGGING_CONFIGURED = True
    logger = getLogger()