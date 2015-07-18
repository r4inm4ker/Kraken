"""Kraken - maths.vec2 module.

Classes:
Vec2 -- Vector 2 object.
"""

import math
from kraken.core.kraken_system import ks
from math_object import MathObject


class Vec2(MathObject):
    """Vector 2 object."""

    def __init__(self, x=0.0, y=0.0):
        """Initializes x, y values for Vec2 object."""

        super(Vec2, self).__init__()
        if ks.getRTValTypeName(x) == 'Vec2':
            self._rtval = x
        else:
            self._rtval = ks.rtVal('Vec2')
            if isinstance(x, Vec2):
                self.set(x=x.x, y=x.y)
            else:
                self.set(x=x, y=y)


    def __str__(self):
        """String representation of the Vec2 object.

        Returns:
            str: String representation of the Vec2 object."""

        return "Vec2(" + str(self.x) + "," + str(self.y) + ")"


    @property
    def x(self):
        """Gets x value of this vector.

        Returns:
            float: X value of this vector.

        """

        return self._rtval.x


    @x.setter
    def x(self, value):
        """Sets x value from the input value.

        Args:
            value (float): Value to set the x property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.x = ks.rtVal('Scalar', value)

        return True


    @property
    def y(self):
        """Gets y value of this vector.

        Returns:
            float: Y value of this vector.

        """

        return self._rtval.y


    @y.setter
    def y(self, value):
        """Sets y value from the input value.

        Args:
            value (float): Value to set the y property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.y = ks.rtVal('Scalar', value)

        return True


    def clone(self):
        """Returns a clone of the Vec2.

        Returns:
            Vec2: The cloned Vec2

        """

        vec2 = Vec2()
        vec2.x = self.x
        vec2.y = self.y

        return vec2


    def set(self, x, y):
        """Sets the x and y value from the input values.

        Args:
            x (float): Value to set the x property as.
            y (float): Value to set the x property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.set('', ks.rtVal('Scalar', x), ks.rtVal('Scalar', y))

        return True

    def add(self, other):
        """Overload method for the add operator.

        Args:
            other (Vec2): Other vector to add to this one.

        Returns:
            Vec2: New Vec2 of the sum of the two Vec2's.

        """

        return Vec2(self._rtval.add('Vec2', other._rtval))