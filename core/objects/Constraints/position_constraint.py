"""Kraken - objects.Constraints.PositionConstraint module.

Classes:
PositionConstraint - Position Constraint.

"""

from base_constraint import BaseConstraint


class PositionConstraint(BaseConstraint):
    """Position Constraint."""

    def __init__(self, name, constrainers, maintainOffset=False):
        super(PositionConstraint, self).__init__(name, constrainers, maintainOffset=maintainOffset)