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
    def getDCCItem(self, kObject):
        """Gets the DCC Item from the full decorated path.

        Arguments:
        kObject -- object, the Kraken Python object that we must find the corresponding DCC item.

        Return:
        DCC Object, None if it isn't found.

        """
        fullBuildName = kObject.getBuildName()

        # Softimage matches the Kraken build name

        findItem = si.Dictionary.GetObject(fullBuildName, False)
        if findItem is None:
            return None

        return findItem


    def syncXfo(self, kObject):
        """Syncs the xfo from the DCC objec to the Kraken object.

        Arguments:
        kObject -- Object, object to sync the xfo for.

        Return:
        True if successful.

        """

        hrcMap = self.getHierarchyMap()

        if kObject not in hrcMap.keys():
            print "Warning! 3D Object '" + kObject.getName() + "' was not found in the mapping!"
            return False

        dccItem = hrcMap[kObject]['dccItem']

        dccXfo = dccItem.Kinematics.Global.GetTransform2(None)
        dccPos = dccXfo.Translation.Get2()
        dccQuat = dccXfo.Rotation.Quaternion.Get2()
        dccScl = dccXfo.Scaling.Get2()

        pos = Vec3(x=dccPos[0], y=dccPos[1], z=dccPos[2])
        quat = Quat(v=Vec3(dccQuat[1], dccQuat[2], dccQuat[3]), w=dccQuat[0])
        scl = Vec3(x=dccScl[0], y=dccScl[1], z=dccScl[2])

        newXfo = Xfo(tr=pos, ori=quat, sc=scl)

        kObject.xfo = newXfo

        return True


    def syncAttribute(self, kObject):
        """Syncs the attribute value from the DCC objec to the Kraken object.

        Arguments:
        kObject -- Object, object to sync the attribute value for.

        Return:
        True if successful.

        """

        hrcMap = self.getHierarchyMap()

        if kObject not in hrcMap.keys():
            print "Warning! Attribute '" + kObject.getName() + "' was not found in the mapping!"
            return False

        dccItem = hrcMap[kObject]['dccItem']

        kObject.setValue(dccItem.Value)

        return True