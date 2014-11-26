"""Kraken - maths.euler module.

Classes:
Euler -- Euler rotation.
"""

import math
from kraken.core.objects.kraken_core import KrakenCore as KC
from math_object import MathObject


class Euler(MathObject):
    """Euler rotation object."""


    def __init__(self, x=None, y=None, z=None, ro=None):
        """Initialize values for x,y,z, and rotation order values."""

        super(Euler, self).__init__()

        if v is not None and not isinstance(v, Vec3):
            raise TypeError("Euler: Invalid type for 'v' argument. Must be a Vec3.")

        if w is not None and not isinstance(w, (int, float)):
            raise TypeError("Euler: Invalid type for 'w' argument. Must be a int or float.")

        client = KC.getInstance().getCoreClient()
        self.rtval = client.RT.types.Euler()
        self.set(v=v, q=q)

        self.set(mathUtils.degToRad(x), mathUtils.degToRad(y), mathUtils.degToRad(z), ro)


    def __str__(self):
        """String representation of Euler object."""

        return "Euler(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " Order: " + self.roMap[self.ro]


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

    @z.setter
    def z(self, value):
        self.rtval.z = KC.inst().rtVal('Scalar', value)

