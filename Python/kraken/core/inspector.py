

class Inspector(object):
    """The Inspector is a singleton object used to create mapping between Kraken
    objects and the DCC objects."""

    def __init__(self):
        super(Inspector, self).__init__()
        self._hrcMap = {}


    # ======================
    # Hierarchy Map Methods
    # ======================
    def getHierarchyMap(self):
        """Gets the hierarchy map from the Inspector.

        Return:
        Dict, the hierarhcy map. None if it hasn't been created.

        """

        return self._hrcMap


    def createHierarchyMap(self, obj):

        if obj.isTypeOf('Component') is False:

            fullBuildName = obj.getFullBuildName()
            dccItem = self.getDCCItem(fullBuildName)

            self._hrcMap[obj] = {
                           "buildName": fullBuildName,
                           "dccItem": dccItem
                          }

        if obj.isTypeOf('Object3D'):
            for i in xrange(obj.getNumAttributeGroups()):
                attrGrp = obj.getAttributeGroupByIndex(i)
                self.createHierarchyMap(attrGrp)

        if obj.isTypeOf('AttributeGroup'):
            print "getting attributes!"
            print obj.name

            for i in xrange(obj.getNumAttributes()):
                attr = obj.getAttributeByIndex(i)
                self.createHierarchyMap(attr)

        if obj.isTypeOf('Object3D'):
            for i in xrange(obj.getNumChildren()):
                child = obj.getChildByIndex(i)
                self.createHierarchyMap(child)

        return


    def clearHierarchyMap(self):
        """Clears the hierarhcy map data.

        Return:
        True if successful.

        """

        self._hrcMap = {}

        return True


    def getDCCItem(self, name):
        """Gets the DCC Item from the full build name.

        This should be re-implemented in each DCC plugin.

        Arguments:
        name -- String, full build name for the object.

        Return:
        DCC Object, None if it isn't found.

        """

        dccItem = None

        return dccItem