"""Kraken - maths.color module.

Classes:
Color -- Color object.
"""


import random
import math
from kraken.core.kraken_system import ks
from math_object import MathObject


class Color(MathObject):
    """Vector 4 object."""

    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        """Initializes r, g b and a values for Color object."""

        super(Color, self).__init__()
        if ks.getRTValTypeName(r) == 'Color':
            self._rtval = r
        else:
            self._rtval = ks.rtVal('Color')
            if isinstance(r, Color):
                self.set(r=r.r, g=r.g, b=r.b, a=r.b)
            else:

                self.set(r=r, g=g, b=b, a=a)


    def __str__(self):
        """String representation of the Color object.

        Returns:
            str: String representation of the Color object."""

        stringRep = "Color("
        stringRep += str(self.r) + ","
        stringRep += str(self.g) + ","
        stringRep += str(self.b) + ","
        stringRep += str(self.a) + ")"

        return stringRep


    @property
    def r(self):
        """Gets red channel of this color.

        Returns:
            float: red channel of this color.

        """

        return self._rtval.r.getSimpleType()


    @r.setter
    def r(self, value):
        """Sets red channel from the input channel.

        Args:
            channel (float): Value to set the red channel to.

        Returns:
            bool: True if successful.

        """

        self._rtval.r = ks.rtVal('Scalar', value)

        return True


    @property
    def g(self):
        """Gets green channel of this color.

        Returns:
            float: green channel of this color.

        """

        return self._rtval.g.getSimpleType()


    @g.setter
    def g(self, value):
        """Sets green channel from the input channel.

        Args:
            channel (float): Value to set the green property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.g = ks.rtVal('Scalar', value)

        return True


    @property
    def b(self):
        """Gets blue channel of this color.

        Returns:
            float: blue channel of this color.

        """

        return self._rtval.b.getSimpleType()


    @g.setter
    def b(self, value):
        """Sets blue channel from the input channel.

        Args:
            channel (float): Value to set the blue property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.b = ks.rtVal('Scalar', value)

        return True


    @property
    def a(self):
        """Gets alpha channel of this color.

        Returns:
            float: alpha channel of this color.

        """

        return self._rtval.a.getSimpleType()


    def __eq__(self, other):
        return self.equal(other)

    def __ne__(self, other):
        return not self.equal(other)


    @g.setter
    def a(self, value):
        """Sets a channel from the input channel.

        Args:
            channel (float): Value to set the a property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.a = ks.rtVal('Scalar', value)


    def clone(self):
        """Returns a clone of the Color.

        Returns:
            Color: The cloned Color

        """

        color = Color()
        color.r = self.r
        color.g = self.g
        color.b = self.b
        return color


    def set(self, r, g, b, a):
        """Sets the r, g, b, and a value from the input values.

        Args:
            r (float): Value to set the r channel to.
            g (float): Value to set the g channel to.
            b (float): Value to set the b channel to.
            a (float): Value to set the a channel to.

        Returns:
            bool: True if successful.

        """

        self._rtval.set('', ks.rtVal('Scalar', r), ks.rtVal('Scalar', g),
                        ks.rtVal('Scalar', b), ks.rtVal('Scalar', a))

        return True


    def equal(self, other):
        """Checks equality of this color with another.

        Args:
            other (Color): other color to check equality with.

        Returns:
            bool: True if equal.

        """

        return self._rtval.equal('Boolean', other._rtval).getSimpleType()


    def almostEqual(self, other, precision):
        """Checks almost equality of this Color with another.

        Args:
            other (Color): other value to check equality with.
            precision (float): Precision value.

        Returns:
            bool: True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', other._rtval,
                                       ks.rtVal('Scalar', precision)).getSimpleType()


    def component(self, i ):
        """Gets the component of this Color by index.

        Args:
            i (int): index of the component to return.

        Returns:
            float: component of this Color.

        """

        return self._rtval.component('Scalar', ks.rtVal('Size', i)).getSimpleType()


    def setComponent(self, i, v ):
        """Sets the component of this Color by index.

        Args:
            i (int): index of the component to set.
            v (float): Value to set component as.

        Returns:
            bool: True if successful.

        """

        return self._rtval.setComponent('', ks.rtVal('Size', i),
                                        ks.rtVal('Scalar', v))



    def add(self, other):
        """Overload method for the add operator.

        Args:
            other (Color): other color to add to this one.

        Returns:
            Color: New Color of the sum of the two Color's.

        """

        return Color(self._rtval.add('Color', other._rtval))


    def subtract(self, other):
        """Overload method for the subtract operator.

        Args:
            other (Color): other color to subtract from this one.

        Returns:
            Color: New Color of the difference of the two Color's.

        """

        return Color(self._rtval.subtract('Color', other._rtval))


    def multiply(self, other):
        """Overload method for the multiply operator.

        Args:
            other (Color): other color to multiply from this one.

        Returns:
            Color: New Color of the product of the two Color's.

        """

        return Color(self._rtval.multiply('Color', other._rtval))


    def divide(self, other):
        """Divides this color and an other.

        Args:
            other (Color): other color to divide by.

        Returns:
            Color: Quotient of the division of this color by the other.

        """

        return Color(self._rtval.divide('Color', other._rtval))


    def multiplyScalar(self, other):
        """Product of this color and a scalar.

        Args:
            other (float): Scalar value to multiply this color by.

        Returns:
            Color: Product of the multiplication of the scalar and this color.

        """

        return Color(self._rtval.multiplyScalar('Color', ks.rtVal('Scalar', other)))


    def divideScalar(self, other):
        """Divides this color and a scalar.

        Args:
            other (float): Value to divide this color by.

        Returns:
            Color: Quotient of the division of the color by the scalar.

        """

        return Color(self._rtval.divideScalar('Color', ks.rtVal('Scalar', other)))


    def linearInterpolate(self, other, t):
        """Linearly interpolates this color with another one based on a scalar
        blend value (0.0 to 1.0).

        Args:
            other (Color): color to blend to.
            t (float): Blend value.

        Returns:
            Color: New color blended between this and the input color.

        """

        return Color(self._rtval.linearInterpolate('Color', ks.rtVal('Color', other), ks.rtVal('Scalar', t)))


    @classmethod
    def randomColor(cls, gammaAdjustment):
        """ Generates a random color based on a seed and offset with gamma adjustment.
            Example:

                # Generate a regular random color
                color = randomColor(seed)

                # Generate a light random color
                color = randomColor(seed, 0.5)

                # Generate a dark random color
                color = randomColor(seed, -0.5)

        Args:
            gammaAdjustment (float): A gamma adjustment to offset the range of the generated color.

        Returns:
            Color: New random color.

        """
        def lerp( val1, val2, t):
            return val1 + ((val2 - val1) * t)

        if(gammaAdjustment > 0.0001):
            # Generate a light color with values between gammaAdjustment and 1.0
            return Color(
                lerp(gammaAdjustment, 1.0, random.random()),
                lerp(gammaAdjustment, 1.0, random.random()),
                lerp(gammaAdjustment, 1.0, random.random())
                )
        elif(gammaAdjustment < -0.0001):
            # Generate a dark color with values between 0.0 and 1.0-gammaAdjustment
            return Color(
                lerp(0.0, 1.0+gammaAdjustment, random.random()),
                lerp(0.0, 1.0+gammaAdjustment, random.random()),
                lerp(0.0, 1.0+gammaAdjustment, random.random())
                )
        else:
            # We add an arbitrary offset to the provided offset so that each color
            # generated based on the seed and offset is unique.
            return Color(
                random.random(),
                random.random(),
                random.random()
                )

