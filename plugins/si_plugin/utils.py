"""Kraken SI - Utils module."""

from win32com.client import constants
from win32com.client.dynamic import Dispatch

from kraken.plugins.si_plugin import logger as siLogger


si = Dispatch("XSI.Application").Application
sel = si.Selection
log = si.LogMessage
logger = siLogger.getLogger("siLogger")

XSIMath = Dispatch("XSI.Math")
XSIUtils = Dispatch("XSI.Utils")
XSIUIToolkit = Dispatch("XSI.UIToolkit")
XSIFactory = Dispatch("XSI.Factory")


def getCollection():
    """Returns an XSICollection object."""

    return Dispatch("XSI.Collection")