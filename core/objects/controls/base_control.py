"""Kraken - objects.Controls.BaseControl module.

Classes:
BaseControl - Base Control.

"""

from kraken.core.objects.curve import Curve


class BaseControl(Curve):
    """Base Control object."""

    def __init__(self, name, parent=None, controlPoints=None):
        """Initializes base control object.

        Arguments:
        name -- String, Name of the constraint.
        parent -- Object, parent object of this object.

        """

        super(BaseControl, self).__init__(name, parent=parent, controlPoints=controlPoints)