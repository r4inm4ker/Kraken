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

    __kType__ = "Attribute"

    def __init__(self, name, value):
        super(Attribute, self).__init__()
        self.name = name
        self.value = value
        self.definition = {}


    def buildDef(self):
        """Builds the object's definition and stores to definition attribute.

        Return:
        Dictionary of object data.
        """

        self.definition["name"] = self.name
        self.definition["value"] = self.value
        self.definition["type"] = self.__kType__

        if hasattr(self, "min"):
            self.definition["min"] = self.min

        if hasattr(self, "max"):
            self.definition["max"] = self.min

        return self.definition


class BoolAttribute(Attribute):
    """Boolean Attribute. Implemented value type checking and limiting."""

    __kType__ = "BooleanAttribute"

    def __init__(self, name, value):
        super(BoolAttribute, self).__init__(name, value)
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

    __kType__ = "FloatAttribute"

    def __init__(self, name, value, minValue, maxValue):
        super(FloatAttribute, self).__init__(name, value)
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

    __kType__ = "IntegerAttribute"

    def __init__(self, name, value, minValue, maxValue):
        super(IntegerAttribute, self).__init__(name, value)
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

    __kType__ = "StringAttribute"

    def __init__(self, name, value):
        super(StringAttribute, self).__init__(name, value)
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