from kraken.core.inspector import Inspector
from kraken.plugins.maya_plugin.utils import *


class Inspector(Inspector):
    """The Inspector is a singleton object used to create mapping between Kraken
    objects and the DCC objects."""

    def __init__(self):
        super(Inspector, self).__init__()


    # ======================
    # Hierarchy Map Methods
    # ======================
    def getDCCItem(self, name):
        """Gets the DCC Item from the full build name.

        This should be re-implemented in each DCC plugin.

        Arguments:
        name -- String, full build name for the object.

        Return:
        DCC Object, None if it isn't found.

        """

        findItem = pm.PyNode("|" + "|".join(name.split('.')))
        if findItem is None:
            return None

        return findItem
