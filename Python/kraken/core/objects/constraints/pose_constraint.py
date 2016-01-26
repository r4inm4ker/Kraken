"""Kraken - objects.Constraints.PoseConstraint module.

Classes:
PoseConstraint - Pose Constraint.

"""

from constraint import Constraint
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.vec3 import Vec3
from kraken.core.maths.quat import Quat


class PoseConstraint(Constraint):
    """Pose Constraint."""

    def __init__(self, name):
        super(PoseConstraint, self).__init__(name)


    def evaluate(self):
        """invokes the constraint causing the output value to be computed.

        Returns:
            bool: True if successful.

        """

        if self.getMaintainOffset() is False:
            newXfo = Xfo()
            newXfo.ori.set(Vec3(), 0.0)
            for constrainer in self.getConstrainers():
                newXfo.tr = newXfo.tr.add(constrainer.xfo.tr)
                newXfo.ori = newXfo.ori.add(constrainer.xfo.ori)

            newXfo.ori.setUnit()
            self.getConstrainee().xfo = newXfo

        return True

