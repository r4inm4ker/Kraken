"""Kraken - objects.container module.

Classes:
Container -- Component container representation.

"""

from kraken.core.objects.scene_item import SceneItem


class Container(SceneItem):
    """Container object."""

    __kType__ = "Container"

    def __init__(self, name):
        super(Container, self).__init__(name, None)

        self.setShapeVisibility(False)


    # =============
    # Name methods
    # =============

    def getBuildName(self):
        """Returns the name used when building the node in the target application.

        Return:
        String, build name of the object.

        """
        
        # The container is generally the root node in the rig. 
        return self.getName() + '_rig'