from kraken.core.Synchronizer import Synchronizer
from kraken.plugins.maya_plugin.utils import *


class Synchronizer(Synchronizer):
    """The Synchronizer is a singleton object used to synchronize data between
    Kraken objects and the DCC objects."""

    def __init__(self):
        super(Synchronizer, self).__init__()


    # ============
    # DCC Methods
    # ============
    def getDCCItem(self, name):
        """Gets the DCC Item from the full build name.

        This should be re-implemented in each DCC plugin.

        Arguments:
        name -- String, full build name for the object.

        Return:
        DCC Object, None if it isn't found.

        """

        try:
            if ':' in name:
                nameSplit = name.split(':')
                objName = nameSplit[0].replace('.', '|')

                if len(nameSplit[1].split('.')) > 0:
                    objName += '.' + nameSplit[1].split('.')[-1]
                else:
                    objName += '.' + nameSplit[1]
            else:
                objName = "|" + name.replace('.', '|')

            print "finding: " + objName

            findItem = pm.PyNode(objName)
        except:
            return None

        return findItem


    def syncXfo(self, obj):
        """Syncs the xfo from the DCC objec to the Kraken object.

        * This should be re-implemented in the sub-classed synchronizer for each
        plugin.

        Arguments:
        obj -- Object, object to sync the xfo for.

        Return:
        True if successful.

        """

        return True


    def syncAttribute(self, obj):
        """Syncs the attribute value from the DCC objec to the Kraken object.

        * This should be re-implemented in the sub-classed synchronizer for each
        plugin.

        Arguments:
        obj -- Object, object to sync the attribute value for.

        Return:
        True if successful.

        """

        return True