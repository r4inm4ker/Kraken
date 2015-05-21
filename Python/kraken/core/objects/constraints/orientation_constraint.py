"""Kraken - objects.Constraints.OrientationConstraint module.

Classes:
OrientationConstraint - Orientation Constraint.

"""

from constraint import Constraint


class OrientationConstraint(Constraint):
    """Orientation Constraint."""

    def __init__(self, name):
        super(OrientationConstraint, self).__init__(name)


    def evaluate(self):
        """invokes the constraint causing the output value to be computed.

        Return:
        Boolean, True if successful.

        """

        if not self.maintainOffset:
            newOri = Quat();
            newOri.set(Vec3(), 0.0)
            for constrainer in self.constrainers:
                newOri = newOri.add(constrainer.xfo.ori)
            newOri.setUnit()
            self.constrainee.xfo.ori = newOri
        return True
