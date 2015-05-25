"""Kraken - objects.Constraints.ScaleConstraint module.

Classes:
ScaleConstraint - Scale Constraint.

"""

from constraint import Constraint


class ScaleConstraint(Constraint):
    """Scale Constraint."""

    def __init__(self, name):
        super(ScaleConstraint, self).__init__(name)


    def evaluate(self):
        """invokes the constraint causing the output value to be computed.

        Return:
        Boolean, True if successful.

        """

        if self.getMaintainOffset() is False:
            newSc = Vec3();
            for constrainer in self.getConstrainers():
                newSc = newSc.add(constrainer.xfo.tr)

            newSc.multiplyScalar(1.0 / len(self.getConstrainers()))
            self.getConstrainee().xfo.sc = newSc

        return True
