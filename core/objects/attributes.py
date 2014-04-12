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

    def __init__(self, name, attrType, value):
        super(Attribute, self).__init__()
        self.name = name
        self.attrType = attrType
        self.value = value


class BoolAttribute(Attribute):
    """Boolean Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value):
        super(BoolAttribute, self).__init__(name, "bool", value)
        assert type(value) is bool, "Value is not of type 'bool'."


    def __setattr__(self, key, value):
        """Ensures 'value' attribute is correct type and within min and max range."""

        if not self.__dict__.has_key(key):
            super(BoolAttribute, self).__setattr__(key, value)
        elif self.__dict__.has_key(key):
            if key == "value":
                if type(value) is not bool:
                    raise TypeError("Value is not of type 'bool'.")
            else:
                super(BoolAttribute, self).__setattr__(key, value)
        else:
            self.__setitem__(key, value)


class FloatAttribute(Attribute):
    """Float Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value, minValue, maxValue):
        super(FloatAttribute, self).__init__(name, "float", value)
        self.min = minValue
        self.max = maxValue

        assert type(self.value) in (int, float), "Value is not of type 'int' or 'float'."
        assert self.value >= self.min, "Value is less than attribute minimum."
        assert self.value <= self.max, "Value is greater than attribute maximum."


    def __setattr__(self, key, value):
        """Ensures 'value' attribute is correct type and within min and max range."""

        if not self.__dict__.has_key(key):
            super(FloatAttribute, self).__setattr__(key, value)
        elif self.__dict__.has_key(key):
            if key == "value":
                if type(value) not in (int, float):
                    raise TypeError("Value is not of type 'int' or 'float'.")

                if value < self.min:
                    raise ValueError("Value is less than attribute minimum.")
                elif value > self.max:
                    raise ValueError("Value is greater than attribute maximum.")
            else:
                super(FloatAttribute, self).__setattr__(key, value)
        else:
            self.__setitem__(key, value)


class IntegerAttribute(Attribute):
    """Float Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value, minValue, maxValue):
        super(IntegerAttribute, self).__init__(name, "int", value)
        self.min = minValue
        self.max = maxValue

        assert type(self.value) is int, "Value is not of type 'int'."
        assert self.value >= self.min, "Value is less than attribute minimum."
        assert self.value <= self.max, "Value is greater than attribute maximum."


    def __setattr__(self, key, value):
        """Ensures 'value' attribute is correct type and within min and max range."""

        if not self.__dict__.has_key(key):
            super(IntegerAttribute, self).__setattr__(key, value)
        elif self.__dict__.has_key(key):
            if key == "value":
                if type(value) is not int:
                    raise TypeError("Value is not of type 'int'.")

                if value < self.min:
                    raise ValueError("Value is less than attribute minimum.")
                elif value > self.max:
                    raise ValueError("Value is greater than attribute maximum.")
            else:
                super(IntegerAttribute, self).__setattr__(key, value)
        else:
            self.__setitem__(key, value)


class StringAttribute(Attribute):
    """String Attribute. Implemented value type checking."""

    def __init__(self, name, value):
        super(StringAttribute, self).__init__(name, "string", value)
        assert type(value) is str, "Value is not of type 'string'."


    def __setattr__(self, key, value):
        """Ensures 'value' attribute is of the correct type."""

        if not self.__dict__.has_key(key):
            super(StringAttribute, self).__setattr__(key, value)
        elif self.__dict__.has_key(key):
            if key == "value":
                if type(value) is not str:
                    raise TypeError("Value is not of type 'string'.")
            else:
                super(StringAttribute, self).__setattr__(key, value)
        else:
            self.__setitem__(key, value)