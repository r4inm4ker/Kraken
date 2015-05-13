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
