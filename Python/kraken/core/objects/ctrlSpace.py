"""Kraken - objects.ctrlSpace module.

Classes:
CtrlSpace -- CtrlSpace representation.

"""

from kraken.core.objects.scene_item import SceneItem


class CtrlSpace(SceneItem):
    """CtrlSpace object."""

    def __init__(self, name, parent=None):
        super(CtrlSpace, self).__init__(name, parent=parent)
        self.setShapeVisibility(False)

