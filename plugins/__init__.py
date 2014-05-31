import os, glob

__all__ = [os.path.splitext(os.path.basename(handler))[0]
           for path in __path__
           for handler in glob.glob(os.path.join(path, '*_plugin'))]