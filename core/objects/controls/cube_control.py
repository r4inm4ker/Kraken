"""Kraken - objects.Controls.CubeControl module.

Classes:
BaseControl - Base Control.

"""

from kraken.core.maths import Vec3
from kraken.core.objects.controls.base_control import BaseControl


class CubeControl(BaseControl):
    """Cube Control object."""

    def __init__(self, name, parent=None):
        """Initializes base control object.

        Arguments:
        name -- String, Name of the constraint.
        parent -- Object, parent object of this object.

        """

        super(CubeControl, self).__init__(name, parent=parent)
        self.addCurveSection([Vec3(1, 0, -1), Vec3(1, 0, 1), Vec3(-1, 0, 1), Vec3(-1, 0, -1)], True)
