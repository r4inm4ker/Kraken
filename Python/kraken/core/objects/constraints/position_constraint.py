"""Kraken - objects.Constraints.PositionConstraint module.

Classes:
PositionConstraint - Position Constraint.

"""

from constraint import Constraint


class PositionConstraint(Constraint):
    """Position Constraint."""

    def __init__(self, name):
        super(PositionConstraint, self).__init__(name)


    def evaluate(self):
        """invokes the constraint causing the output value to be computed.

        Return:
        Boolean, True if successful.

        """

        if not self.maintainOffset:
            newTr = Vec3();
            for constrainer in self.constrainers:
                newTr = newTr.add(constrainer.xfo.tr)
            self.constrainee.xfo.tr = newTr
        return True
