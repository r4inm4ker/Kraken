

class Synchronizer(object):
    """The Synchronizer is a singleton object used to synchronize data between
    Kraken objects and the DCC objects."""

    def __init__(self, target=None):
        """Initializes Synchronizer.

        The target object's hierarchy will be traversed and synchronized.

        Args:
            target (object): top Kraken object to synchronize.

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

        Returns:
            object: The object that is the target of synchronization.

        """

        return self._target


    def setTarget(self, target):
        """Sets the target for synchronization.

        Args:
            target (object): top Kraken object to synchronize.

        Returns:
            bool: True if successful.

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

        Returns:
            dict: The hierarhcy map. None if it hasn't been created.

        """

        return self._hrcMap


    def createHierarchyMap(self, kObject):

        # ==============
        # Map Hierarchy
        # ==============

        # Skip components in the mapping as they are not built into the DCC
        if kObject.isTypeOf('Component') is False:
            dccItem = self.getDCCItem(kObject)

            self._hrcMap[kObject] = {
                           "dccItem": dccItem
                          }

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

        Returns:
            bool: True if successful.

        """

        self._hrcMap = {}

        return True


    # ========================
    # Synchronization Methods
    # ========================
    def sync(self):
        """Synchronizes the target hierarchy with the matching objects in the DCC.

        Returns:
            bool: True if successful.

        """

        self.synchronize(self.getTarget())

        return True


    def synchronize(self, kObject):
        """Iteration method that traverses the hierarchy and syncs the different
        object types.

        Args:
            kObject (object): object to synchronize.

        Returns:
            bool: True if successful.

        """

        # =================
        # Synchronize Data
        # =================
        if kObject.isTypeOf('Object3D'):

            # Sync Xfo if it's not a Component
            if kObject.isTypeOf('Component') is False:

                # If the top-level rig DCC node does not exist, don't proceed
                # through the hierarchy.
                if kObject.isTypeOf('Rig') and self.getDCCItem(kObject) is None:
                    return False

                self.syncXfo(kObject)

            # Sync Curves / Controls
            if kObject.isTypeOf('Curve') is True:
                self.syncCurveData(kObject)

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

            if kObject.getName() != 'implicitAttrGrp':
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

        **This should be re-implemented in the sub-classed synchronizer for each
        plugin.**

        Args:
            kObject (object): The Kraken Python object that we must find the corresponding DCC item.

        Returns:
            object: None if it isn't found.

        """

        dccItem = None

        return dccItem


    def syncXfo(self, kObject):
        """Syncs the xfo from the DCC object to the Kraken object.

        **This should be re-implemented in the sub-classed synchronizer for each
        plugin.**

        Args:
            kObject (object): object to sync the xfo for.

        Returns:
            bool: True if successful.

        """

        return True


    def syncAttribute(self, kObject):
        """Syncs the attribute value from the DCC object to the Kraken object.

        **This should be re-implemented in the sub-classed synchronizer for each
        plugin.**

        Args:
            kObject (object): object to sync the attribute value for.

        Returns:
            bool: True if successful.

        """

        return True


    def syncCurveData(self, kObject):
        """Syncs the curve data from the DCC object to the Kraken object.

        **This should be re-implemented in the sub-classed synchronizer for each
        plugin.**

        Args:
            kObject (object): object to sync the curve data for.

        Returns:
            bool: True if successful.

        """

        return True