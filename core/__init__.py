"""Kraken Framework."""

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 1
VERSION_SUFFIX = "beta"


def getVersion():
    versionString = str(VERSION_MAJOR) + "." + str(VERSION_MINOR) + "." + str(VERSION_BUILD)
    if VERSION_SUFFIX:
        versionString = versionString + "-" + VERSION_SUFFIX

    return versionString