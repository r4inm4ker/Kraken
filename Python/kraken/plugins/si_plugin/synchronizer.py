from kraken.core.maths import Xfo, Vec3, Quat

from kraken.core.synchronizer import Synchronizer
from kraken.plugins.si_plugin.utils import *
from kraken.plugins.si_plugin.utils.curves import curveToKraken


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

        Args:
            kObject (object): The Kraken Python object that we must find the corresponding DCC item.

        Returns:
            object: DCC Object.

        """

        pathObj = kObject
        softPath = ''

        traverse = True
        while traverse is True:

            if pathObj is None:
                raise Exception("Parent not specified for object, so a full path cannot be resolved to a Softimage object: " + kObject.getPath())

            if pathObj.isTypeOf('AttributeGroup'):
                softPath = '.' + pathObj.getName() + softPath

            elif pathObj.isTypeOf('Attribute'):
                softPath = '.' + pathObj.getName()

            else:
                if pathObj.isTypeOf('Layer') or pathObj.isTypeOf('Container'):
                    softPath = pathObj.getBuildName() + softPath
                    traverse = False
                else:
                    softPath = '.' + pathObj.getBuildName() + softPath

            pathObj = pathObj.getParent()

        findItem = si.Dictionary.GetObject(softPath, False)
        if findItem is None:
            return None

        return findItem


    def syncXfo(self, kObject):
        """Syncs the xfo from the DCC object to the Kraken object.

        Args:
            kObject (object): object to sync the xfo for.

        Returns:
            object: True if successful.

        """

        hrcMap = self.getHierarchyMap()

        if kObject not in hrcMap.keys():
            log("Warning! 3D Object '" + kObject.getName() + "' was not found in the mapping!", 8)
            return False

        dccItem = hrcMap[kObject]['dccItem']

        if dccItem is None:
            log("Warning Syncing. No DCC Item for :" + kObject.getPath(), 8)
            return

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
        """Syncs the attribute value from the DCC object to the Kraken object.

        Args:
            kObject (object): object to sync the attribute value for.

        Returns:
            bool: True if successful.

        """

        hrcMap = self.getHierarchyMap()

        if kObject not in hrcMap.keys():
            log("Warning! Attribute '" + kObject.getName() + "' was not found in the mapping!", 8)
            return False

        dccItem = hrcMap[kObject]['dccItem']

        if dccItem is None:
            log("Warning Syncing. No DCC Item for :" + kObject.getPath(), 8)
            return

        kObject.setValue(dccItem.Value)

        return True


    def syncCurveData(self, kObject):
        """Syncs the curve data from the DCC object to the Kraken object.

        Args:
            kObject (object): object to sync the curve data for.

        Returns:
            bool: True if successful.

        """

        hrcMap = self.getHierarchyMap()

        if kObject not in hrcMap.keys():
            log("Warning! 3D Object '" + kObject.getName() + "' was not found in the mapping!", 8)
            return False

        dccItem = hrcMap[kObject]['dccItem']

        if dccItem is None:
            log("Warning Syncing. No DCC Item for :" + kObject.getPath(), 8)
            return

        # Get Curve Data from Softimage Curve
        data = curveToKraken(dccItem)
        kObject.setCurveData(data)

        return True
