"""Kraken - builders module.

Classes:
BaseBuilder -- Base builder object to build objects in DCC.

"""


class BaseBuilder(object):
    """BaseBuilder object for building objects in DCC's. Sub-class per DCC in
    plugin.

    """

    def __init__(self):
        super(BaseBuilder, self).__init__()


    def buildAttributes(self, sceneItem, node):
        """Builds attributes on the DCC object.

        Arguments:
        sceneItem -- SceneItem, kraken object to build attributes for.
        node -- DCC Object, DCC object to build attributes on.

        Return:
        True if successful.

        """

        return True


    def buildHierarchy(self, sceneItem, parentNode, component=None):
        """Builds the hierarchy for the supplied sceneItem.

        Arguments:
        sceneItem -- SceneItem, kraken object to build.
        parentNode -- DCC Object, object that is the parent of the created object.
        component -- Component, component that this object belongs to.

        Return:
        DCC object that was created.

        """

        node = None

        return node


    def buildName(self, sceneItem, component=None):
        """Builds the name for the sceneItem that is passed.

        Arguments:
        sceneItem -- SceneItem, kraken object to build the name for.
        component -- Component, component that this object belongs to.

        Return:
        Built name as a string.
        None if it fails.

        """

        return None


    def build(self, container):
        """Builds the supplied container into a DCC representation.

        Arguments:
        container -- Container, kraken container object to build.

        Return:
        True if successful.

        """

        return True