"""Kraken - objects.Attributes.StringAttribute module.

Classes:
StringAttribute - Base Attribute.

"""

from BaseAttribute import BaseAttribute


class StringAttribute(BaseAttribute):
    """String Attribute. Implemented value type checking."""

    def __init__(self, name, value):
        super(StringAttribute, self).__init__(name, value)
        assert type(value) is str, "Value is not of type 'string'."

    def setValue(self, value):
        """Ensures 'value' attribute is correct type and within min and max range."""

        if type(value) not in (str):
            raise TypeError("Value is not of type 'str'.")

        super(StringAttribute, self).setValue(value)

        return True