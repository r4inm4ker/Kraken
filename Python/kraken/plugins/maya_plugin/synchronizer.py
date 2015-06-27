from kraken.core.maths import Xfo, Vec3, Quat

from kraken.core.synchronizer import Synchronizer
from kraken.plugins.maya_plugin.utils import *
from kraken.core.objects.attributes.attribute_group import AttributeGroup

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

        if dccItem is None:
            print "Warning Syncing. No DCC Item for :" + kObject.getPath()
            return

        dccPos = dccItem.getTranslation()
        dccQuat = dccItem.getRotation(quaternion=True).get()
        dccScl = dccItem.getScale()

        pos = Vec3(x=dccPos[0], y=dccPos[1], z=dccPos[2])
        quat = Quat(v=Vec3(dccQuat[0], dccQuat[1], dccQuat[2]), w=dccQuat[3])
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

        if dccItem is None:
            print "Warning Syncing. No DCC Item for :" + kObject.getPath()
            return

        kObject.setValue(dccItem.get())

        return True