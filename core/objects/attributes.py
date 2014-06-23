"""Kraken - objects.attributes module.

Classes:
Attribute - Base Attribute.
BoolAttribute - Boolean Attribute.
FloatAttribute - Float Attribute.
IntegerAttribute - Integer Attribute.
StringAttribute - String Attribute.

"""


class Attribute(object):
    """Base Attribute object."""

    def __init__(self, name, value):
        super(Attribute, self).__init__()
        self.name = name
        self.value = value


    def getName(self):
        return self.name


    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

        return True


class BoolAttribute(Attribute):
    """Boolean Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value):
        super(BoolAttribute, self).__init__(name, value)
        assert type(value) is bool, "Value is not of type 'bool'."


    def setValue(self, value):
        """Ensures 'value' attribute is correct type and within min and max range."""

        if type(value) is not bool:
            raise TypeError("Value is not of type 'bool'.")

        super(BoolAttribute, self).setValue(value)


        return True


class FloatAttribute(Attribute):
    """Float Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value, minValue, maxValue):
        super(FloatAttribute, self).__init__(name, value)
        self.min = minValue
        self.max = maxValue

        assert type(self.value) in (int, float), "Value is not of type 'int' or 'float'."
        assert self.value >= self.min, "Value is less than attribute minimum."
        assert self.value <= self.max, "Value is greater than attribute maximum."


    def setValue(self, value):
        """Ensures 'value' attribute is correct type and within min and max range."""

        if type(value) not in (int, float):
            raise TypeError("Value is not of type 'int' or 'float'.")

        if value < self.min:
            raise ValueError("Value is less than attribute minimum.")
        elif value > self.max:
            raise ValueError("Value is greater than attribute maximum.")

        super(FloatAttribute, self).setValue(value)

        return True


class IntegerAttribute(Attribute):
    """Float Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value, minValue, maxValue):
        super(IntegerAttribute, self).__init__(name, value)
        self.min = minValue
        self.max = maxValue

        assert type(self.value) is int, "Value is not of type 'int'."
        assert self.value >= self.min, "Value is less than attribute minimum."
        assert self.value <= self.max, "Value is greater than attribute maximum."


    def setValue(self, value):
        """Ensures 'value' attribute is correct type and within min and max range."""

        if type(value) not in (int):
            raise TypeError("Value is not of type 'int'.")

        if value < self.min:
            raise ValueError("Value is less than attribute minimum.")
        elif value > self.max:
            raise ValueError("Value is greater than attribute maximum.")

        super(IntegerAttribute, self).setValue(value)

        return True


class StringAttribute(Attribute):
    """String Attribute. Implemented value type checking."""

    def __init__(self, name, value):
        super(StringAttribute, self).__init__(name, value)
        assert type(value) is str, "Value is not of type 'string'."

    def setValue(self, value):
        """Ensures 'value' attribute is correct type and within min and max range."""

        if type(value) not in (str):
            raise TypeError("Value is not of type 'str'.")

        super(IntegerAttribute, self).setValue(value)

        return True