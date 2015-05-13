from kraken.core.maths import Xfo, Vec3, Quat

from kraken.core.synchronizer import Synchronizer
from kraken.plugins.si_plugin.utils import *


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

        name = name.replace(':', '.')

        findItem = si.Dictionary.GetObject(name, False)
        if findItem is None:
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

        hrcMap = self.getHierarchyMap()

        if obj not in hrcMap.keys():
            print "Warning! " + obj.getName() + " was not found in the mapping!"
            return False

        dccItem = hrcMap[obj]['dccItem']

        dccXfo = dccItem.Kinematics.Global.GetTransform2()
        dccPos = dccXfo.Translation.Get2()
        dccQuat = dccXfo.Rotation.Quaternion.Get2()

        pos = Vec3(x=dccPos[0], y=dccPos[1], z=dccPos[2])
        quat = Quat(v=Vec3(dccQuat[1], dccQuat[2], dccQuat[3]), w=dccQuat[0])

        obj.xfo = dccItem

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