"""Kraken - objects.Attributes.BoolAttribute module.

Classes:
BoolAttribute - Base Attribute.

"""

from kraken.objects.attributes.attribute import Attribute
from kraken.core.kraken_system import ks


class BoolAttribute(Attribute):
    """Boolean Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value=False):
        super(BoolAttribute, self).__init__(name, value)
        assert type(value) is bool, "Value is not of type 'bool'."


    def setValue(self, value):
        """Sets the value of the attribute.

        Arguments:
        value -- Value to set the attribute to.

        Return:
        True if successful.

        """

        if type(value) is not bool:
            raise TypeError("Value is not of type 'bool'.")

        super(BoolAttribute, self).setValue(value)

        return True


    def getRTVal(self):
        """Returns and RTVal object for this attribute.

        Return:
        RTVal

        """

        return ks.rtVal('Boolean', self.value)
