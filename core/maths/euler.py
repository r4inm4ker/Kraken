"""Kraken - maths.euler module.

Classes:
Euler -- Euler rotation.
"""

import math
from kraken.core.objects.kraken_system import KrakenSystem as KS
from math_object import MathObject


class Euler(MathObject):
    """Euler rotation object."""

    def __init__(self, x=None, y=None, z=None, ro=None):
        """Initialize values for x,y,z, and rotation order values."""

        super(Euler, self).__init__()

        if x is not None and not isinstance(x, (int, float)):
            raise TypeError("Euler: Invalid type for 'x' argument. Must be a int or float.")

        if y is not None and not isinstance(y, (int, float)):
            raise TypeError("Euler: Invalid type for 'y' argument. Must be a int or float.")

        if z is not None and not isinstance(z, (int, float)):
            raise TypeError("Euler: Invalid type for 'z' argument. Must be a int or float.")

        # if ro is not None and not isinstance(ro, (int, float)):
        #     raise TypeError("Euler: Invalid type for 'ro' argument. Must be a int or float.")

        client = KS.getInstance().getCoreClient()
        self.rtval = client.RT.types.Euler()

        # self.set(x, y, z, ro)


    def __str__(self):
        """String representation of Euler object."""

        return "Euler(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + "," + " ro: " + str(self.ro) + ")"


    @property
    def x(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.x


    @x.setter
    def x(self, value):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.x = KS.inst().rtVal('Scalar', value)


    @property
    def y(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.y


    @y.setter
    def y(self, value):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.y = KS.inst().rtVal('Scalar', value)


    @property
    def z(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.z


    @z.setter
    def z(self, value):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.z = KS.inst().rtVal('Scalar', value)


    @property
    def ro(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.ro


    @ro.setter
    def ro(self, value):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.ro = KS.inst().rtVal('RotationOrder', value)


    # Setter from scalar components
    def set(self, x, y, z):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.set(KS.inst().rtVal('Scalar', x), KS.inst().rtVal('Scalar', y), KS.inst().rtVal('Scalar', z))