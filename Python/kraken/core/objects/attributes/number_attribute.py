"""Kraken - objects.Attributes.NumberAttribute module.

Classes:
NumberAttribute - Base Attribute.

"""

from attribute import Attribute


class NumberAttribute(Attribute):
    """Number Attributee. Base class for number attribute types"""

    def __init__(self, name, value=0, minValue=None, maxValue=None):
        super(NumberAttribute, self).__init__(name, value)
        self._min = None
        self._max = None
        self._uiMin = None
        self._uiMax = None

        if minValue is not None:
            self.setMin(minValue)

        if maxValue is not None:
            self.setMax(maxValue)

        self.setUIMin(minValue)
        self.setUIMax(maxValue)


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


    def getUIMin(self):
        """Gets the default minimum ui slider value for this attribute.

        Return:
        Float / Integer - default minimum ui slider value.

        """

        return self._uiMin


    def setUIMin(self, minimum):
        """Sets the default minimum ui slider value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        minimum -- float / integer, default minimum ui slider value.

        Return:
        True if successful.

        """

        attrType = self.__class__.__name__
        if attrType is 'IntegerAttribute':
            if type(minimum) is not int:
                raise TypeError("UiMin value is not of type 'int'.")

        if attrType is 'FloatAttribute':
            if type(minimum) not in (int, float):
                raise TypeError("UiMin value is not of type 'int' or 'float'.")

        if self._uiMax is not None:
            if minimum > self._uiMax:
                raise ValueError('UiMin value is greater than attribute uiMax')

        if minimum > self._max:
            raise ValueError('UiMin value is greater than attribute maximum')

        if minimum < self._min:
            raise ValueError('UiMin value is less than attribute minimum')

        self._uiMin = minimum

        return True


    def getUIMax(self):
        """Gets the default maximum ui slider value for this attribute.

        Return:
        Float / Integer - default maximum ui slider value.

        """

        return self._uiMax


    def setUIMax(self, maximum):
        """Sets the default maximum ui slider value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        maximum -- float / integer, default maximum ui slider value.

        Return:
        True if successful.

        """

        attrType = self.__class__.__name__
        if attrType is 'IntegerAttribute':
            if type(maximum) is not int:
                raise TypeError("UiMax value is not of type 'int'.")

        if attrType is 'FloatAttribute':
            if type(maximum) not in (int, float):
                raise TypeError("UiMax value is not of type 'int' or 'float'.")

        if self._uiMin is not None:
            if maximum < self._uiMin:
                raise ValueError('UiMax value is less than attribute uiMin')

        if maximum < self._min:
            raise ValueError('UiMax value is less than attribute minimum')

        if maximum > self._max:
            raise ValueError('UiMax value is greater than attribute maximum')

        self._uiMax = maximum

        return True
