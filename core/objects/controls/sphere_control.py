"""Kraken - objects.Controls.SphereControl module.

Classes:
SphereControl - Sphere Control.

"""

from kraken.core.maths.vec import Vec3
from kraken.core.objects.controls.base_control import BaseControl


class SphereControl(BaseControl):
    """Sphere Control object."""

    def __init__(self, name, parent=None):
        """Initializes base control object.

        Arguments:
        name -- String, Name of the constraint.
        parent -- Object, parent object of this object.

        """

        super(SphereControl, self).__init__(name, parent=parent)
        self.addCurveSection([Vec3(0.0, 0.5, 0.0), Vec3(0.0, 0.35, -0.35), Vec3(0.0, 0.0, -0.5), Vec3(0.0, -0.35, -0.35), Vec3(0.0, -0.5, 0.0), Vec3(0.0, -0.35, 0.35), Vec3(0.0, 0.0, 0.5), Vec3(0.0, 0.35, 0.35)], True)
        self.addCurveSection([Vec3(0.0, 0.0, -0.5), Vec3(0.35, 0.0, -0.35), Vec3(0.5, 0.0, 0.0), Vec3(0.35, 0.0, 0.35), Vec3(0.0, 0.0, 0.5), Vec3(-0.35, 0.0, 0.35), Vec3(-0.5, 0.0, 0.0), Vec3(-0.35, 0.0, -0.35)], True)
        self.addCurveSection([Vec3(0.0, 0.5, 0.0), Vec3(0.35, 0.35, 0.0), Vec3(0.5, 0.0, 0.0), Vec3(0.35, -0.35, 0.0), Vec3(0.0, -0.5, 0.0), Vec3(-0.35, -0.35, 0.0), Vec3(-0.5, 0.0, 0.0), Vec3(-0.35, 0.35, 0.0)], True)