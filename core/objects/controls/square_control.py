"""Kraken - objects.Controls.SquareControl module.

Classes:
BaseControl - Base Control.

"""

from kraken.core.objects.controls.base_control import BaseControl


class SquareControl(BaseControl):
    """Square Control object."""

    def __init__(self, name, parent=None):
        """Initializes base control object.

        Arguments:
        name -- String, Name of the constraint.
        parent -- Object, parent object of this object.

        """

        super(SquareControl, self).__init__(name, parent=parent)
        self.setControlPoints = [[1, 0, -1], [1, 0, 1], [-1, 0, 1], [-1, 0, -1]]
        self.setClosed(True)