"""Kraken - objects.Constraints.OrientationConstraint module.

Classes:
OrientationConstraint - Orientation Constraint.

"""

from base_constraint import BaseConstraint


class OrientationConstraint(BaseConstraint):
    """Orientation Constraint."""

    def __init__(self, name):
        super(OrientationConstraint, self).__init__(name)