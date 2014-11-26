"""Kraken - maths.vec module.

Classes:
Vec3 -- Vector 3 object.
"""

import math
from math_object import MathObject
from kraken.core.objects.kraken_core import KrakenCore as KC
from vec import Vec

class Vec3(Vec):
    """Vector 2 object."""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Initializes x, y values for Vec3 object."""

        super(Vec3, self).__init__()
        client = KC.getInstance().getCoreClient()
        self.rtval = client.RT.types.Vec3()
        self.set(x=x, y=y, z=z)

    def __str__(self):
        """String representation of the Vec3 object."""
        return "Vec3(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

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

    @property
    def z(self):
        """I'm the 'z' property."""
        return self.rtval.z

    @y.setter
    def z(self, value):
        self.rtval.z = KC.inst().rtVal('Scalar', value)


    # Setter from scalar components
    def set(self, x, y, z):
        self.rtval.set('', KC.inst().rtVal('Scalar', x), KC.inst().rtVal('Scalar', y), KC.inst().rtVal('Scalar', z))
