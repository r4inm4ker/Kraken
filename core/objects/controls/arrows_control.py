"""Kraken - objects.Controls.ArrowsControl module.

Classes:
ArrowsControl - Arrows Control.

"""

from kraken.core.maths.vec import Vec3
from kraken.core.objects.controls.base_control import BaseControl


class ArrowsControl(BaseControl):
    """Arrows Control object."""

    def __init__(self, name, parent=None):
        """Initializes base control object.

        Arguments:
        name -- String, Name of the constraint.
        parent -- Object, parent object of this object.

        """

        super(ArrowsControl, self).__init__(name, parent=parent)
        self.addCurveSection([Vec3(-0.05, 0.0, 0.05), Vec3(-0.05, 0.0, 0.25), Vec3(-0.15, 0.0, 0.25), Vec3(0.0, -0.0, 0.4), Vec3(0.15, 0.0, 0.25), Vec3(0.05, 0.0, 0.25), Vec3(0.05, 0.0, 0.05), Vec3(0.25, 0.0, 0.05), Vec3(0.25, 0.0, 0.15), Vec3(0.4, -0.0, 0.0), Vec3(0.25, 0.0, -0.15), Vec3(0.25, 0.0, -0.05), Vec3(0.05, 0.0, -0.05), Vec3(0.05, 0.0, -0.25), Vec3(0.15, 0.0, -0.25), Vec3(0.0, -0.0, -0.4), Vec3(-0.15, 0.0, -0.25), Vec3(-0.05, 0.0, -0.25), Vec3(-0.05, 0.0, -0.05), Vec3(-0.25, 0.0, -0.05), Vec3(-0.25, 0.0, -0.15), Vec3(-0.4, -0.0, -0.0), Vec3(-0.25, 0.0, 0.15), Vec3(-0.25, 0.0, 0.05)], True)