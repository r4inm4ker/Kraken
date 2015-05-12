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


def getInspector():
    """Gets the inspector that belongs to the DCC calling this method.

    Return:
    Inspect, instance of the inspector for the DCC.

    """

    dccInspector = None

    for eachPlugin in __all__:
        mod = __import__("kraken.plugins." + eachPlugin, fromlist=['dccTest'])
        reload(mod)

        if mod.dccTest() is True:
            loaded_mod = __import__("kraken.plugins." + eachPlugin + ".inspector", fromlist=['inspector'])
            reload(loaded_mod)
            loaded_class = getattr(loaded_mod, 'Inspector')

            dccInspector = loaded_class()

    if dccInspector is None:
        print "Failed to find DCC inspector. Falling back to Python inspector."

        from kraken.core import inspector
        dccInspector = inspector.Inspector()

    return dccInspector