"""Kraken - objects.Attributes.ColorAttribute module.

Classes:
ColorAttribute - Base Attribute.

"""

from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.kraken_system import ks


class ColorAttribute(Attribute):
    """Color Attribute. Implemented value type checking."""

    def __init__(self, name, value=None, parent=None):
        super(ColorAttribute, self).__init__(name, value=value, parent=parent)

        if value is None:
            value = { 'r':0.5, 'g':0.5, 'b':0.5, 'a':1.0}
        self.setValue(value)


    def setValue(self, color):
        """Sets the value of the attribute..

        Args:
            value: Value to set the attribute to.

        Returns:
            bool: True if successful.

        """

        assert isinstance(r, Color), "r Value is not of type Color."

        super(ColorAttribute, self).setValue(value)

        return True


    def getRTVal(self):
        """Returns and RTVal object for this attribute.

        Returns:
            RTVal: RTVal object of the attribute.

        """

        return ks.rtVal('Color', self._value)



    def getDataType(self):
        """Returns the name of the data type for this attribute.

        Note:
            This is a localized method specific to the Color Attribute.

        Returns:
            str: Color name of the attribute type.

        """

        return 'Color'