"""Kraken - objects.Constraints.OrientationConstraint module.

Classes:
OrientationConstraint - Orientation Constraint.

"""

from constraint import Constraint
from kraken.core.maths.vec3 import Vec3
from kraken.core.maths.quat import Quat


class OrientationConstraint(Constraint):
    """Orientation Constraint."""

    def __init__(self, name):
        super(OrientationConstraint, self).__init__(name)


    def evaluate(self):
        """invokes the constraint causing the output value to be computed.

        Return:
        Boolean, True if successful.

        """

        if self.getMaintainOffset() is False:
            newOri = Quat();
            newOri.set(Vec3(), 0.0)
            for constrainer in self.getConstrainers():
                newOri = newOri.add(constrainer.xfo.ori)

            newOri.setUnit()
            self.getConstrainee().xfo.ori = newOri

        return True
