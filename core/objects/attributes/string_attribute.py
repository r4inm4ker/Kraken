"""Kraken - objects.Attributes.StringAttribute module.

Classes:
StringAttribute - Base Attribute.

"""

from base_attribute import BaseAttribute


class StringAttribute(BaseAttribute):
    """String Attribute. Implemented value type checking."""

    __kType__ = "StringAttribute"

    def __init__(self, name, value):
        super(StringAttribute, self).__init__(name, value)
        assert type(value) is str, "Value is not of type 'string'."

    def setValue(self, value):
        """Sets the value of the attribute.

        Arguments:
        value -- Value to set the attribute to.

        Return:
        True if successful.

        """

        if type(value) not in (str):
            raise TypeError("Value is not of type 'str'.")

        super(StringAttribute, self).setValue(value)

        return True