"""Kraken - objects.Constraints.PositionConstraint module.

Classes:
PositionConstraint - Position Constraint.

"""

from constraint import Constraint


class PositionConstraint(Constraint):
    """Position Constraint."""

    def __init__(self, name):
        super(PositionConstraint, self).__init__(name)