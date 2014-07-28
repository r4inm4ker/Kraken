"""Kraken - objects.operators.splice_operator module.

Classes:
SpliceOperator - Splice operator object.

"""

from kraken.core.objects.operators.base_operator import BaseOperator


class SpliceOperator(BaseOperator):
    """Base Operator representation."""

    __kType__ = "SpliceOperator"

    # TODO: Look in to expanding the Splice operator to be able to handle more
    # than one extension / operator. Need to change extension to extensions and
    # figure out how to differentiate the solver types per operator. Maybe have
    # an attirbute array called 'klOperators' that contains sets of what we
    # currently have setup.

    def __init__(self, name, solverTypeName, extension):
        super(SpliceOperator, self).__init__(name)

        self.solverTypeName = solverTypeName
        self.extension = extension


    def getSolverTypeName(self):
        """Returns the solver type name for this operator.

        Return:
        String, name of the solver type this operator uses.

        """

        return self.solverTypeName


    def getExtension(self):
        """Returns the extention this operator uses.

        Return:
        String, name of the extension this solver uses.

        """

        return self.extension