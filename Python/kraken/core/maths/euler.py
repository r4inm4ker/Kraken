"""Kraken - maths.euler module.

Classes:
Euler -- Euler rotation.
"""

import math

from kraken.core.kraken_system import ks
from kraken.core.maths.math_object import MathObject
from kraken.core.maths.mat33 import Mat33
from kraken.core.maths.rotation_order import RotationOrder


rotationOrderStrToIntMapping = {
    'xyz': 0,
    'XYZ': 0,
    'yzx': 1,
    'YZX': 1,
    'zxy': 2,
    'ZXY': 2,
    'xzy': 3,
    'XZY': 3,
    'zyx': 4,
    'ZYX': 4,
    'yxz': 5,
    'YXZ': 5
}

rotationOrderIntToStrMapping = [
    'XYZ',
    'YZX',
    'ZXY',
    'XZY',
    'ZYX',
    'YXZ'
]


class Euler(MathObject):
    """Euler rotation object."""

    def __init__(self, x=None, y=None, z=None, ro=None):
        """Initialize values for x,y,z, and rotation order values."""

        super(Euler, self).__init__()

        if ks.getRTValTypeName(x) == 'Euler':
            self._rtval = x
        else:

            if x is not None and not isinstance(x, (int, float)) and not isinstance(x, Euler):
                raise TypeError("Euler: Invalid type for 'x' argument. \
                                Must be an int or float.")

            if y is not None and not isinstance(y, (int, float)):
                raise TypeError("Euler: Invalid type for 'y' argument. Must be \
                                an int or float.")

            if z is not None and not isinstance(z, (int, float)):
                raise TypeError("Euler: Invalid type for 'z' argument. Must be \
                                an int or float.")

            if ro is not None:
                if isinstance(ro, basestring) or isinstance(ro, (int)):
                    ro = RotationOrder(order=ro)

            self._rtval = ks.rtVal('Euler')
            if isinstance(x, Euler):
                self.set(x=x.x, y=x.y, z=x.z, ro=x.ro)
            elif x is not None and y is not None and z is not None:
                if ro is not None:
                    self.set(x=x, y=y, z=z, ro=ro)
                else:
                    self.set(x=x, y=y, z=z)


    def __str__(self):
        """String representation of Euler object."""

        return "Euler(x=" + str(self.x) + ", y=" + str(self.y) + ", z=" + str(self.z) + ", ro= '" + str(self.ro) + "')"


    @property
    def x(self):
        """Doc String.

        Return:
        True if successful.

        """

        return self._rtval.x


    @x.setter
    def x(self, value):
        """Doc String.

        Arguments:
        value -- number, x value of the Euler Angles.

        Return:
        True if successful.

        """

        self._rtval.x = ks.rtVal('Scalar', value)


    @property
    def y(self):
        """Doc String.

        Return:
        True if successful.

        """

        return self._rtval.y


    @y.setter
    def y(self, value):
        """Doc String.

        Arguments:
        value -- number, y value of the Euler Angles.

        Return:
        True if successful.

        """

        self._rtval.y = ks.rtVal('Scalar', value)


    @property
    def z(self):
        """Doc String.

        Return:
        True if successful.

        """

        return self._rtval.z


    @z.setter
    def z(self, value):
        """Doc String.

        Arguments:
        value -- number, z value of the Euler Angles.

        Return:
        True if successful.

        """

        self._rtval.z = ks.rtVal('Scalar', value)


    @property
    def ro(self):
        """Doc String.

        Return:
        True if successful.

        """

        return RotationOrder(self._rtval.ro)


    @ro.setter
    def ro(self, value):
        """Doc String.

        Arguments:
        value -- number, rotation order(ro) value of the Euler Angles.

        Return:
        True if successful.

        """

        self._rtval.ro = ks.rtVal('RotationOrder', value)


    def clone(self):
        """Returns a clone of the Euler.

        Return:
        The cloned Euler

        """

        euler = Euler();
        euler.x = self.x;
        euler.y = self.y;
        euler.z = self.z;
        euler.ro = self.ro;

        return euler


    # Setter from scalar components
    def set(self, x, y, z, ro=None):
        """Doc String.

        Arguments:
        x -- Scalar, x angle in radians.
        y -- Scalar, y angle in radians.
        z -- Scalar, z angle in radians.
        ro -- Integer, the rotation order to use in the euler angles.

        Return:
        True if successful.

        """

        if ro is not None:
            self._rtval.set('', ks.rtVal('Scalar', x), ks.rtVal('Scalar', y), ks.rtVal('Scalar', z))
        else:
            self._rtval.set('', ks.rtVal('Scalar', x), ks.rtVal('Scalar', y), ks.rtVal('Scalar', z), ks.rtval('RotationOrder', ro))

        return True


    def equal(self, other):
        """Checks equality of this Euler with another.

        Arguments:
        other -- Euler, other value to check equality with.

        Return:
        True if equal.

        """

        return self._rtval.equal('Boolean', ks.rtVal('Euler', other))


    def almostEqual(self, other, precision):
        """Checks almost equality of this Euler with another.

        Arguments:
        other -- Euler, other value to check equality with.
        precision -- Scalar, precision value.

        Return:
        True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', ks.rtVal('Euler', other), ks.rtVal('Scalar', precision))


    def toMat33(self):
        """Converts the Euler angles value to a Mat33.

        Return:
        The Mat33 value

        """

        return Mat33(self._rtval.toMat33('Mat33'))
