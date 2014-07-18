"""Kraken - Base Operator module.

Classes:
BaseOperator -- Base Operator representation.

"""

from kraken.core.objects.operators import operatorBinding


class BaseOperator(object):
    """Base Operator representation."""

    __kType__ = "Operator"

    def __init__(self, name):
        super(BaseOperator, self).__init__()
        self.name = name
        self.binding = None


    # ================
    # Binding Methods
    # ================
    def addBinding(self, binding):
        """Adds an operator binding to this operator.

        Arguments:
        binding -- Object, operator binding to add to this object.

        Return:
        True if successful.

        """

        return True


    def removeBinding(self):
        """Removes the bidning from the operator.

        Return:
        True if successful.

        """

        return True