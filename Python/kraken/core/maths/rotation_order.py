"""Kraken - maths.rotation_order module.

Classes:
RotationOrder -- Rotation Order.
"""

import math

from kraken.core.kraken_system import ks
from kraken.core.maths.math_object import MathObject


class RotationOrder(MathObject):
    """RotationOrder rotation object."""

    def __init__(self, order=0):
        """Initialize rotation order."""

        super(RotationOrder, self).__init__()

        if ks.getRTValTypeName(order) == 'RotationOrder':
            self._rtval = order
        else:
            self._rtval = ks.rtVal('RotationOrder')
            if isinstance(order, RotationOrder):
                self.set(order=order.order)
            else:
                self.set(order=order)


    def __str__(self):
        """String representation of RotationOrder object.

        Returns:
            str: String representation of the RotationOrder.

        """

        return "RotationOrder(order='" + str(self.order) + "')"


    @property
    def order(self):
        """Gets order value of this Rotation Order.

        Returns:
            float: Order value of this Rotation Order.

        """

        return self._rtval.order.getSimpleType()


    @order.setter
    def order(self, value):
        """Sets order value from the input value.

        Args:
            value (int, str): Value to set the order property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.order = ks.rtVal('Integer', value)

        return True


    def __eq__(self, other):
        return self.order == other.order

    def __ne__(self, other):
        return not self.order == other.order


    def clone(self):
        """Returns a clone of the RotationOrder.

        Returns:
            RotationOrder: The cloned RotationOrder.

        """

        rotOrder = RotationOrder()
        rotOrder.order = self.order

        return rotOrder


    def set(self, order):
        """Sets the order value from the input values.

        Args:
            order (int, str): Value to set the order property as.

        Returns:
            bool: True if successful.

        """

        if type(order) == str:
            lowerOrder = order.lower()
            if lowerOrder == 'xyz':
                newOrder = 0
            elif lowerOrder == 'yzx':
                newOrder = 1
            elif lowerOrder == 'zxy':
                newOrder = 2
            elif lowerOrder == 'xzy':
                newOrder = 3
            elif lowerOrder == 'zyx':
                newOrder = 4
            elif lowerOrder == 'yxz':
                newOrder = 5
            else:
                print "Invalid rotation order '" + order + "', using default 0 (XYZ)."
                newOrder = 0

        elif type(order) == int:
            if order < 0 or order > 5:
                print "Invalid rotation order: '" + str(order) + "', using default 0 (XYZ)."
                newOrder = 0
            else:
                newOrder = order

        if newOrder == 0:
            self._rtval.setXYZ('')
        elif newOrder == 1:
            self._rtval.setYZX('')
        elif newOrder == 2:
            self._rtval.setZXY('')
        elif newOrder == 3:
            self._rtval.setXZY('')
        elif newOrder == 4:
            self._rtval.setZYX('')
        elif newOrder == 5:
            self._rtval.setYXZ('')
        else:
            raise ValueError("Invalid rotation order: '" + str(order) + "'")

        return True


    def isXYZ(self):
        """Checks if this Rotation Order is equal to XYZ.

        Returns:
            bool: True if this rotationorder is XYZ.

        """

        return self.order == 0


    def isYZX(self):
        """Checks if this Rotation Order is equal to YZX.

        Returns:
            bool: True if this rotationorder is YZX.

        """

        return self.order == 1


    def isZXY(self):
        """Checks if this Rotation Order is equal to ZXY.

        Returns:
            bool: True if this rotationorder is ZXY.

        """

        return self.order == 2


    def isXZY(self):
        """Checks if this Rotation Order is equal to XZY.

        Returns:
            bool: True if this rotationorder is XZY.

        """

        return self.order == 3


    def isZYX(self):
        """Checks if this Rotation Order is equal to ZYX.

        Returns:
            bool: True if this rotationorder is ZYX.

        """

        return self.order == 4


    def isYXZ(self):
        """Checks if this Rotation Order is equal to YXZ.

        Returns:
            bool: True if this rotationorder is YXZ.

        """

        return self.order == 5


    def isReversed(self):
        """Checks if this Rotation Order is a reversed one.

        Returns:
            bool: True if this rotation order is one of the reversed ones (XZY, ZYX or YXZ).

        """

        return self.isXZY() or self.isZYX() or self.isYXZ()


    def setXYZ(self):
        """Sets this rotation order to be XYZ.

        Returns:
            bool: True if successful.

        """

        self.order = 0

        return True


    def setYZX(self):
        """Sets this rotation order to be YZX.

        Returns:
            bool: True if successful.

        """

        self.order = 1

        return True


    def setZXY(self):
        """Sets this rotation order to be ZXY.

        Returns:
            bool: True if successful.

        """

        self.order = 2

        return True


    def setXZY(self):
        """Sets this rotation order to be XZY.

        Returns:
            bool: True if successful.

        """

        self.order = 3

        return True


    def setZYX(self):
        """Sets this rotation order to be ZYX.

        Returns:
            bool: True if successful.

        """

        self.order = 4

        return True


    def setYXZ(self):
        """Sets this rotation order to be YXZ.

        Returns:
            bool: True if successful.

        """

        self.order = 5

        return True
