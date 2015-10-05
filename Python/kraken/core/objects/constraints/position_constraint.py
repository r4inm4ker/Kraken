"""Kraken - objects.Constraints.PositionConstraint module.

Classes:
PositionConstraint - Position Constraint.

"""

from constraint import Constraint
from kraken.core.maths.vec3 import Vec3


class PositionConstraint(Constraint):
    """Position Constraint."""

    def __init__(self, name):
        super(PositionConstraint, self).__init__(name)


    def evaluate(self):
        """invokes the constraint causing the output value to be computed.

        Returns:
            bool: True if successful.

        """

        if self.getMaintainOffset() is False:
            newTr = Vec3();
            for constrainer in self.getConstrainers():
                newTr = newTr.add(constrainer.xfo.tr)

            self.getConstrainee().xfo.tr = newTr

        return True
