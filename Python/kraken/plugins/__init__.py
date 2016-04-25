import os
import glob

__all__ = [os.path.splitext(os.path.basename(plugin))[0]
           for path in __path__
           for plugin in glob.glob(os.path.join(path, '*_plugin'))]


def getBuilder():
    """Returns the appropriate builder module for the DCC.

    Return:
    Builder, instance of the builder for the DCC.

    """

    dccBuilder = None

    for eachPlugin in __all__:
        mod = __import__("kraken.plugins." + eachPlugin, fromlist=['dccTest'])
        reload(mod)

        if mod.dccTest() is True:
            loaded_mod = __import__("kraken.plugins." + eachPlugin + ".builder", fromlist=['builder'])
            reload(loaded_mod)
            loaded_class = getattr(loaded_mod, 'Builder')

            dccBuilder = loaded_class()

    if dccBuilder is None:
        print "Failed to find DCC builder. Falling back to Python builder."

        from kraken.core import builder
        dccBuilder = builder.Builder(debugMode=True)

    return dccBuilder


def getSynchronizer():
    """Gets the Synchronizer that belongs to the DCC calling this method.

    Return:
    Inspect, instance of the Synchronizer for the DCC.

    """

    dccSynchronizer = None

    for eachPlugin in __all__:
        mod = __import__("kraken.plugins." + eachPlugin, fromlist=['dccTest'])
        reload(mod)

        if mod.dccTest() is True:
            loaded_mod = __import__("kraken.plugins." + eachPlugin + ".synchronizer", fromlist=['synchronizer'])
            reload(loaded_mod)
            loaded_class = getattr(loaded_mod, 'Synchronizer')

            dccSynchronizer = loaded_class()

    if dccSynchronizer is None:
        print "Failed to find DCC Synchronizer. Falling back to Python Synchronizer."

        from kraken.core import synchronizer
        dccSynchronizer = synchronizer.Synchronizer()

    return dccSynchronizer


def getLogger():
    """Returns the appropriate logging module for the DCC.

    Return:
    Function, function pointer for the DCC

    """

    logger = None

    for eachPlugin in __all__:
        mod = __import__("kraken.plugins." + eachPlugin, fromlist=['dccTest'])
        reload(mod)

        if mod.dccTest() is True:
            loaded_mod = __import__("kraken.plugins." + eachPlugin + ".logger", fromlist=['logger'])
            reload(loaded_mod)
            loaded_class = getattr(loaded_mod, 'OutputLog')

            logger = loaded_class()

    if logger is None:
        print "Failed to find DCC logger. Falling back to Python logger."

        from logger import OutputLog
        logger = OutputLog()

    return logger


def getFabricClient():
    """Returns the appropriate Fabric client for the DCC.

    Args:
        Arguments (Type): information.

    Returns:
        Type: True if successful.

    """

    client = None

    for eachPlugin in __all__:
        mod = __import__("kraken.plugins." + eachPlugin, fromlist=['dccTest'])
        reload(mod)

        if mod.dccTest() is True:
            loaded_mod = __import__("kraken.plugins." + eachPlugin + ".fabric_client", fromlist=['getClient'])
            reload(loaded_mod)

            client = loaded_mod.getClient()

    if client is None:
        print "Failed to find DCC client. Falling back to Python client."

    return client