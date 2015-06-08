from kraken.core.maths import Xfo, Vec3, Quat

from kraken.core.synchronizer import Synchronizer
from kraken.plugins.maya_plugin.utils import *


class Synchronizer(Synchronizer):
    """The Synchronizer is a singleton object used to synchronize data between
    Kraken objects and the DCC objects."""

    def __init__(self):
        super(Synchronizer, self).__init__()


    # ============
    # DCC Methods
    # ============
    def getDCCItem(self, obj):
        """Gets the DCC Item from the full decorated path.

        Arguments:
        decoratedPath -- String, full decorated path for the object.

        Return:
        DCC Object, None if it isn't found.

        """

        fullBuildName = obj.getBuildName()
        decoratedPath = obj.getDecoratedPath()
        try:
            path = ''
            pathSections = decoratedPath.split('.')
            for pathSection in pathSections:
                decorator = if ':' in pathSection: pathSection.split(':')[1] else: ''
                if decorator == '%':
                    # The '%' symbol represents an attribute group that we never
                    # build in Maya.
                    continue

                elif decorator == '#':
                    # The '#' symbol represents an attribute object which
                    # requires a '.' seperator in the Maya path.
                    path += '.' + pathSection

                else:
                    path += '|' + pathSection

            foundItem = pm.PyNode(path)
        except:
            return None

        return foundItem


    def syncXfo(self, obj):
        """Syncs the xfo from the DCC objec to the Kraken object.

        Arguments:
        obj -- Object, object to sync the xfo for.

        Return:
        True if successful.

        """

        hrcMap = self.getHierarchyMap()

        if obj not in hrcMap.keys():
            print "Warning! 3D Object '" + obj.getName() + "' was not found in the mapping!"
            return False

        dccItem = hrcMap[obj]['dccItem']

        if dccItem is None:
            print "Warning Syncing. No DCC Item for :" + obj.getPath()
            return;

        dccPos = dccItem.getTranslation()
        dccQuat = dccItem.getRotation(quaternion=True).get()
        dccScl = dccItem.getScale()

        pos = Vec3(x=dccPos[0], y=dccPos[1], z=dccPos[2])
        quat = Quat(v=Vec3(dccQuat[0], dccQuat[1], dccQuat[2]), w=dccQuat[3])
        scl = Vec3(x=dccScl[0], y=dccScl[1], z=dccScl[2])

        newXfo = Xfo(tr=pos, ori=quat, sc=scl)

        obj.xfo = newXfo

        return True


    def syncAttribute(self, obj):
        """Syncs the attribute value from the DCC objec to the Kraken object.

        Arguments:
        obj -- Object, object to sync the attribute value for.

        Return:
        True if successful.

        """

        hrcMap = self.getHierarchyMap()

        if obj not in hrcMap.keys():
            print "Warning! Attribute '" + obj.getName() + "' was not found in the mapping!"
            return False

        dccItem = hrcMap[obj]['dccItem']

        if dccItem is None:
            print "Warning Syncing. No DCC Item for :" + obj.getPath()
            return;

        obj.setValue(dccItem.get())

        return True