"""Kraken - objects.operators.splice_operator module.

Classes:
SpliceOperator - Splice operator object.

"""

from kraken.core.objects.operators.base_operator import BaseOperator


class SpliceOperator(BaseOperator):
    """Base Operator representation."""

    __kType__ = "SpliceOperator"

    def __init__(self, name, solverTypeName, extension):
        super(SpliceOperator, self).__init__(name)

        self.solverTypeName = solverTypeName
        self.extension = extension

    def getSolverTypeName(self):
        return self.solverTypeName