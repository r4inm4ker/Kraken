from kraken.core.maths import Xfo, Vec3, Quat

from kraken.core.synchronizer import Synchronizer
from kraken.plugins.maya_plugin.utils import *
from kraken.plugins.maya_plugin.utils.curves import curveToKraken


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
            object: The created DCC object.

        """

        path = kObject.getPath()
        pathSections = path.split('.')
        pathObj = kObject
        mayaPath = ''
        index = len(pathSections) - 1
        for pathSection in reversed(pathSections):

            if pathObj is None:
                raise Exception("parent not specified for object, so a full path cannot be resolved to a maya object:" + path)

            if pathObj.isTypeOf('AttributeGroup'):
                # We don't build an attribute group in Maya, so skip this object
                pass

            elif pathObj.isTypeOf('Attribute'):
                # The attribute object requires a '.' seperator in the Maya path.
                mayaPath = '.' + pathObj.getName()

            else:
                if index > 0:
                    mayaPath = '|' + pathObj.getBuildName() + mayaPath
                else:
                    mayaPath = pathObj.getBuildName() + mayaPath

            pathObj = pathObj.getParent()
            index -= 1

        try:
            foundItem = pm.PyNode(mayaPath)
        except:
            return None

        return foundItem


    def syncXfo(self, kObject):
        """Syncs the xfo from the DCC object to the Kraken object.

        Args:
            kObject (object): Object to sync the xfo for.

        Returns:
            Boolean: True if successful.

        """

        hrcMap = self.getHierarchyMap()

        if kObject not in hrcMap.keys():
            print "Warning! 3D Object '" + kObject.getName() + "' was not found in the mapping!"
            return False

        dccItem = hrcMap[kObject]['dccItem']

        if dccItem is None:
            print "Warning Syncing. No DCC Item for :" + kObject.getPath()
            return False

        dccPos = dccItem.getTranslation(space='world')
        dccQuat = dccItem.getRotation(space='world', quaternion=True).get()
        dccScl = dccItem.getScale()

        pos = Vec3(x=dccPos[0], y=dccPos[1], z=dccPos[2])
        quat = Quat(v=Vec3(dccQuat[0], dccQuat[1], dccQuat[2]), w=dccQuat[3])

        # If flag is set, pass the DCC Scale values.
        if kObject.testFlag('SYNC_SCALE') is True:
            scl = Vec3(x=dccScl[0], y=dccScl[1], z=dccScl[2])
        else:
            scl = Vec3(1.0, 1.0, 1.0)

        newXfo = Xfo(tr=pos, ori=quat, sc=scl)

        kObject.xfo = newXfo

        return True


    def syncAttribute(self, kObject):
        """Syncs the attribute value from the DCC objec to the Kraken object.

        Args:
            kObject (object): Object to sync the attribute value for.

        Returns:
            bool: True if successful.

        """

        if kObject.getParent() is not None and kObject.isTypeOf('AttributeGroup'):
            if kObject.getParent().getParent().isTypeOf('Component'):
                if kObject.getParent().getParent().getComponentType() == "Guide":
                    return False

        hrcMap = self.getHierarchyMap()

        if kObject not in hrcMap.keys():
            print "Warning! Attribute '" + kObject.getName() + "' was not found in the mapping!"
            return False

        dccItem = hrcMap[kObject]['dccItem']

        if dccItem is None:
            print "Warning Syncing. No DCC Item for :" + kObject.getPath()
            return

        kObject.setValue(dccItem.get())

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
            print "Warning! 3D Object '" + kObject.getName() + "' was not found in the mapping!"
            return False

        dccItem = hrcMap[kObject]['dccItem']

        if dccItem is None:
            print "Warning Syncing. No DCC Item for :" + kObject.getPath()
            return

        # Get Curve Data from Softimage Curve
        data = curveToKraken(dccItem)
        kObject.setCurveData(data)

        return True