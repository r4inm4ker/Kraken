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
