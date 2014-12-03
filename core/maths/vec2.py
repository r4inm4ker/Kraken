"""Kraken - maths.vec module.

Classes:
Vec2 -- Vector 2 object.
Vec3 -- Vector 3 object.
Vec4 -- Vector 4 object.
"""

import math
from math_object import MathObject
from kraken.core.objects.kraken_core import KrakenCore as KC

class Vec2(MathObject):
    """Vector 2 object."""

    def __init__(self, x=0.0, y=0.0):
        """Initializes x, y values for Vec2 object."""

        super(Vec2, self).__init__()
        client = KC.getInstance().getCoreClient()
        self.rtval = client.RT.types.Vec2()
        self.set(x=x, y=y)

    def __str__(self):
        """String representation of the Vec2 object."""
        return "Vec2(" + str(self.x) + "," + str(self.y) + ")"

    @property
    def x(self):
        """I'm the 'x' property."""
        return self.rtval.x

    @x.setter
    def x(self, value):
        self.rtval.x = KC.inst().rtVal('Scalar', value)

    @property
    def y(self):
        """I'm the 'y' property."""
        return self.rtval.y

    @y.setter
    def y(self, value):
        self.rtval.y = KC.inst().rtVal('Scalar', value)


    # Setter from scalar components
    def set(self, x, y):
        self.rtval.set(KC.inst().rtVal('Scalar', x), KC.inst().rtVal('Scalar', y))
