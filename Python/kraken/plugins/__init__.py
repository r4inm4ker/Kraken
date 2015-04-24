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

    builder = None

    for eachPlugin in __all__:
        mod = __import__("kraken.plugins." + eachPlugin, fromlist=['dccTest'])
        reload(mod)

        if mod.dccTest() is True:
            loaded_mod = __import__("kraken.plugins." + eachPlugin + ".builder", fromlist=['builder'])
            reload(loaded_mod)
            loaded_class = getattr(loaded_mod, 'Builder')

            builder = loaded_class()

    if builder is None:
        print "Failed to find DCC builder. Falling back to Python builder."

        from kraken.core.builders import builder
        builder = builder.Builder()

    return builder