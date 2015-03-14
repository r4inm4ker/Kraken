"""Kraken - objects.Constraints.PositionConstraint module.

Classes:
PositionConstraint - Position Constraint.

"""

from base_constraint import BaseConstraint


class PositionConstraint(BaseConstraint):
    """Position Constraint."""

    __kType__ = "PositionConstraint"

    def __init__(self, name):
        super(PositionConstraint, self).__init__(name)