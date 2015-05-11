"""Kraken - objects.Attributes.NumberAttribute module.

Classes:
NumberAttribute - Base Attribute.

"""

from kraken.core.objects.attributes.attribute import Attribute


class NumberAttribute(Attribute):
    """Number Attributee. Base class for number attribute types"""

    def __init__(self, name, value=0, minValue=None, maxValue=None):
        super(NumberAttribute, self).__init__(name, value)
        self.min = None
        self.max = None

        if minValue is None:
            if value < 0:
                self.setMin(value)
            else:
                self.setMin(0)

        if maxValue is None:
            if value == 0:
                self.setMax(10)
            else:
                self.setMax(value * 3)


    # ==============
    # Value Methods
    # ==============
    def setValue(self, value):
        """Sets the value of the attribute.

        Arguments:
        value -- Value to set the attribute to.

        Return:
        True if successful.

        """

        if self.validateValue(value) is False:
            raise TypeError("Value: '" + str(value) + "' has an invalid type!")

        super(NumberAttribute, self).setValue(value)

        return True


    # ==================
    # Min / Max Methods
    # ==================
    def getMin(self):
        """Gets the minimum value for this attribute.

        Return:
        Float / Integer - minimum value.

        """

        return self.min


    def setMin(self, minimum):
        """Sets the minimum value for the attributeself.

        Note: Only works on float or integer attributes.

        Arguments:
        min -- float / integer, minimum value the attribute can have.

        Return:
        True if successful.

        """

        assert type(minimum) in (int, float), "'minimum' is not of type 'int' \
                                              or 'float'."

        self.min = minimum

        return True


    def getMax(self):
        """Gets the maximum value for this attribute.

        Return:
        Float / Integer - maximum value.

        """

        return self.max


    def setMax(self, maximum):
        """Sets the maximum value for the attributeself.

        Note: Only works on float or integer attributes.

        Arguments:
        min -- float / integer, maximum value the attribute can have.

        Return:
        True if successful.

        """

        assert type(maximum) in (int, float), "'maximum' is not of type 'int' \
                                              or 'float'."

        self.max = maximum

        return True
