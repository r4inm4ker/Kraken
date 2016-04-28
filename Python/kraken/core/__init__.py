"""Kraken Core."""

VERSION_MAJOR = 1
VERSION_MINOR = 2
VERSION_BUILD = 0
VERSION_SUFFIX = ""


def getVersion():
    """Contatenates the version globals and returns the current version of
    Kraken.

    Returns:
        str: Current version of Kraken.

    """

    versionString = str(VERSION_MAJOR) + "." + str(VERSION_MINOR) + "." + str(VERSION_BUILD)
    if VERSION_SUFFIX:
        versionString = versionString + "-" + VERSION_SUFFIX

    return versionString
