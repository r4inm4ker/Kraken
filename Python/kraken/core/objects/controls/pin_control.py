"""Kraken - objects.Controls.PinControl module.

Classes:
PinControl - Pin Control.

"""

from kraken.core.maths import Vec3
from kraken.core.objects.controls.base_control import BaseControl


class PinControl(BaseControl):
    """Pin Control object."""

    def __init__(self, name, parent=None):
        """Initializes base control object.

        Arguments:
        name -- String, Name of the constraint.
        parent -- Object, parent object of this object.

        """

        super(PinControl, self).__init__(name, parent=parent)
        self.addCurveSection([Vec3(0.0, 0.0, -0.5), Vec3(-0.17, 0.0, -0.57), Vec3(-0.25, 0.0, -0.75), Vec3(-0.17, 0.0, -0.93), Vec3(0.0, 0.0, -1.0), Vec3(0.17, 0.0, -0.93), Vec3(0.25, 0.0, -0.75), Vec3(0.17, 0.0, -0.57), Vec3(0.0, 0.0, -0.5), Vec3(0.0, 0.0, 0.0)], False)