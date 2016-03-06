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

