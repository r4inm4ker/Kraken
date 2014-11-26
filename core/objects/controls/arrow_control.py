"""Kraken - objects.Controls.ArrowControl module.

Classes:
ArrowControl - Arrow Control.

"""

from kraken.core.maths import Vec3
from kraken.core.objects.controls.base_control import BaseControl


class ArrowControl(BaseControl):
    """Arrow Control object."""

    def __init__(self, name, parent=None):
        """Initializes base control object.

        Arguments:
        name -- String, Name of the constraint.
        parent -- Object, parent object of this object.

        """

        super(ArrowControl, self).__init__(name, parent=parent)
        self.addCurveSection([Vec3(-0.05, 0.0, -0.25), Vec3(-0.15, 0.0, -0.25), Vec3(0.0, -0.0, -0.5), Vec3(0.15, 0.0, -0.25), Vec3(0.05, 0.0, -0.25), Vec3(0.05, 0.0, 0.5), Vec3(-0.05, 0.0, 0.5)], True)