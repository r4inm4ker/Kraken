"""Kraken - objects.Attributes.NumberAttribute module.

Classes:
NumberAttribute - Base Attribute.

"""

from attribute import Attribute


class NumberAttribute(Attribute):
    """Number Attributee. Base class for number attribute types"""

    def __init__(self, name, value=0, minValue=None, maxValue=None, keyable=None, lock=None, uiMin=None, uiMax=None):
        super(NumberAttribute, self).__init__(name, value, keyable=keyable, lock=lock)
        self._min = None
        self._max = None
        self._uiMin = None
        self._uiMax = None

        if minValue is not None:
            self.setMin(minValue)

        if maxValue is not None:
            self.setMax(maxValue)

        if uiMin is not None:
            self.setUiMin(uiMin)
        else:
            self.setUiMin(self._min)

        if uiMax is not None:
            self.setUiMax(uiMax)
        else:
            self.setUiMax(self._max)


    # ==================
    # Min / Max Methods
    # ==================
    def getMin(self):
        """Gets the minimum value for this attribute.

        Return:
        Float / Integer - minimum value.

        """

        return self._min


    def setMin(self, minimum):
        """Sets the minimum value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        minimum -- float / integer, minimum value the attribute can have.

        Return:
        True if successful.

        """

        assert type(minimum) in (int, float), "'minimum' is not of type 'int' or 'float'."

        self._min = minimum

        return True


    def getMax(self):
        """Gets the maximum value for this attribute.

        Return:
        Float / Integer - maximum value.

        """

        return self._max


    def setMax(self, maximum):
        """Sets the maximum value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        maximum -- float / integer, maximum value the attribute can have.

        Return:
        True if successful.

        """

        assert type(maximum) in (int, float), "'maximum' is not of type 'int' or 'float'."

        self._max = maximum

        return True


    def getUiMin(self):
        """Gets the default minimum ui slider value for this attribute.

        Return:
        Float / Integer - default minimum ui slider value.

        """

        return self._uiMin


    def setUiMin(self, minimum):
        """Sets the default minimum ui slider value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        minimum -- float / integer, default minimum ui slider value.

        Return:
        True if successful.

        """
        if self._uiMax is not None:
            if minimum > self._uiMax:
                raise ValueError('Value is greater than attribute uiMax')

        if minimum < self._min:
            raise ValueError('Value is less than attribute minimum')

        if minimum > self._min:
            raise ValueError('Value is greater than attribute maximum')

        self._uiMin = minimum

        return True


    def getUiMax(self):
        """Gets the default maximum ui slider value for this attribute.

        Return:
        Float / Integer - default maximum ui slider value.

        """

        return self._uiMax


    def setUiMax(self, maximum):
        """Sets the default maximum ui slider value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        maximum -- float / integer, default maximum ui slider value.

        Return:
        True if successful.

        """
        if self._uiMin is not None:
            if maximum < self._uiMin:
                raise ValueError('Value is less than attribute uiMin')

        if maximum < self._min:
            raise ValueError('Value is less than attribute minimum')

        if maximum < self._max:
            raise ValueError('Value is less than attribute maximum')

        self._uiMax = maximum

        return True
