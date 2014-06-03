from kraken.core.objects import elements
from kraken.plugins.si_plugin.utils import *


def _build(self):
    """Builds element definition.

    Implement in sub-classes.

    Return:
    definition of the element.

    """

    if self.__kType__ == "Null":
        scnRoot = si.ActiveProject3.ActiveScene.Root
        scnRoot.AddNull(self.name)

    return True


def patch():
    nullElement = elements.Null
    nullElement._build = _build