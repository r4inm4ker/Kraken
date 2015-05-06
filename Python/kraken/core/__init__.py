"""Kraken Core."""

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 1
VERSION_SUFFIX = "alpha"


def getVersion():
    """Contatenates the version globals and returns the current version of
    Kraken.

    Return:
    String, current version of Kraken.

    """

    versionString = str(VERSION_MAJOR) + "." + str(VERSION_MINOR) + "." + str(VERSION_BUILD)
    if VERSION_SUFFIX:
        versionString = versionString + "-" + VERSION_SUFFIX

    return versionString
