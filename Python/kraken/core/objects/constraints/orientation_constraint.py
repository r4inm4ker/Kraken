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
