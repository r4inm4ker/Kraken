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
        dccBuilder = builder.Builder()

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
        print "Failed to find DCC inspector. Falling back to Python inspector."

        from kraken.core import synchronizer
        dccSynchronizer = synchronizer.Synchronizer()

    return dccSynchronizer