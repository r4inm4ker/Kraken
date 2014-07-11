"""Kraken - objects.Controls.CircleControl module.

Classes:
BaseControl - Base Control.

"""

from kraken.core.maths import Vec3
from kraken.core.objects.controls.base_control import BaseControl


class CircleControl(BaseControl):
    """Circle Control object."""

    def __init__(self, name, parent=None):
        """Initializes base control object.

        Arguments:
        name -- String, Name of the constraint.
        parent -- Object, parent object of this object.

        """

        super(CircleControl, self).__init__(name, parent=parent)
        self.addCurveSection([Vec3(0.7071067811865475, 0.0, -0.7071067811865478), Vec3(1.0, 0.0, 0.0), Vec3(0.7071067811865476, 0.0, 0.7071067811865475), Vec3(0.0, 0.0, 1.0), Vec3(-0.7071067811865475, 0.0, 0.7071067811865476), Vec3(-1.0, 0.0, 0.0), Vec3(-0.7071067811865477, 0.0, -0.7071067811865475), Vec3(0.0, 0.0, -1.0)], True)