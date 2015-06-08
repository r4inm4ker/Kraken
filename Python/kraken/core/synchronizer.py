

class Synchronizer(object):
    """The Synchronizer is a singleton object used to synchronize data between
    Kraken objects and the DCC objects."""

    def __init__(self, target=None):
        """Initializes Synchronizer.

        The target object's hierarchy will be traversed and synchronized.

        Arguments:
        target -- Object, top Kraken object to synchronize.

        """

        super(Synchronizer, self).__init__()
        self._hrcMap = {}
        self._target = None

        if target is not None:
            self.setTarget(target)


    # ===============
    # Target Methods
    # ===============
    def getTarget(self):
        """Gets the target object of the synchronizer.

        Return:
        Object, the object that is the target of synchronization.

        """

        return self._target


    def setTarget(self, target):
        """Sets the target for synchronization.

        Arguments:
        target -- Object, top Kraken object to synchronize.

        Return:
        True if successful.

        """

        self.clearHierarchyMap()

        self._target = target

        self.createHierarchyMap(self.getTarget())

        return True


    # ======================
    # Hierarchy Map Methods
    # ======================
    def getHierarchyMap(self):
        """Gets the hierarchy map from the Inspector.

        Return:
        Dict, the hierarhcy map. None if it hasn't been created.

        """

        return self._hrcMap


    def createHierarchyMap(self, kObject):

        # ==============
        # Map Hierarchy
        # ==============
        if kObject.isTypeOf('Object3D'):

            # Sync Xfo if it's not a Component
            if kObject.isTypeOf('Component') is False:
                dccItem = self.getDCCItem(kObject)

                self._hrcMap[kObject] = {
                               "dccItem": dccItem
                              }

        elif kObject.isTypeOf('Attribute'):
            fullBuildName = kObject.getBuildName()
            dccItem = self.getDCCItem(kObject)

            self._hrcMap[kObject] = {
                           "dccItem": dccItem
                          }

        else:
            pass

        # =======================
        # Iterate over hierarchy
        # =======================
        if kObject.isTypeOf('Object3D'):
            # Iterate over attribute groups
            for i in xrange(kObject.getNumAttributeGroups()):
                attrGrp = kObject.getAttributeGroupByIndex(i)
                self.createHierarchyMap(attrGrp)

        # Iterate over attributes
        if kObject.isTypeOf('AttributeGroup'):
            for i in xrange(kObject.getNumAttributes()):
                attr = kObject.getAttributeByIndex(i)
                self.createHierarchyMap(attr)

        if kObject.isTypeOf('Object3D'):

            # Iterate over children
            for i in xrange(kObject.getNumChildren()):
                child = kObject.getChildByIndex(i)
                self.createHierarchyMap(child)

        return


    def clearHierarchyMap(self):
        """Clears the hierarhcy map data.

        Return:
        True if successful.

        """

        self._hrcMap = {}

        return True


    # ========================
    # Synchronization Methods
    # ========================
    def sync(self):
        """Synchronizes the target hierarchy with the matching objects in the DCC.

        Return:
        True if successful.

        """

        self.synchronize(self.getTarget())

        return True


    def synchronize(self, kObject):
        """Iteration method that traverses the hierarchy and syncs the different
        object types.

        Arguments:
        kObject -- Object, object to synchronize.

        Return:
        True if successful.

        """

        # =================
        # Synchronize Data
        # =================
        if kObject.isTypeOf('Object3D'):

            # Sync Xfo if it's not a Component
            if kObject.isTypeOf('Component') is False:
                self.syncXfo(kObject)

        elif kObject.isTypeOf('Attribute'):
            self.syncAttribute(kObject)

        else:
            pass

        # =======================
        # Iterate over hierarchy
        # =======================
        if kObject.isTypeOf('Object3D'):
            # Iterate over attribute groups
            for i in xrange(kObject.getNumAttributeGroups()):
                attrGrp = kObject.getAttributeGroupByIndex(i)
                self.synchronize(attrGrp)

        # Iterate over attributes
        if kObject.isTypeOf('AttributeGroup'):
            for i in xrange(kObject.getNumAttributes()):
                attr = kObject.getAttributeByIndex(i)
                self.synchronize(attr)

        if kObject.isTypeOf('Object3D'):

            # Iterate over children
            for i in xrange(kObject.getNumChildren()):
                child = kObject.getChildByIndex(i)
                self.synchronize(child)

        return True


    # ============
    # DCC Methods
    # ============
    def getDCCItem(self, kObject):
        """Gets the DCC Item from the full decorated path.

        * This should be re-implemented in the sub-classed synchronizer for each
        plugin.

        Arguments:
        kObject -- object, the Kraken Python object that we must find the corresponding DCC item.

        Return:
        DCC Object, None if it isn't found.

        """

        dccItem = None

        return dccItem


    def syncXfo(self, kObject):
        """Syncs the xfo from the DCC objec to the Kraken object.

        * This should be re-implemented in the sub-classed synchronizer for each
        plugin.

        Arguments:
        kObject -- Object, object to sync the xfo for.

        Return:
        True if successful.

        """

        return True


    def syncAttribute(self, kObject):
        """Syncs the attribute value from the DCC objec to the Kraken object.

        * This should be re-implemented in the sub-classed synchronizer for each
        plugin.

        Arguments:
        kObject -- Object, object to sync the attribute value for.

        Return:
        True if successful.

        """

        return True