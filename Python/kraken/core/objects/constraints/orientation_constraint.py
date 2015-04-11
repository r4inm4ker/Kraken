"""Kraken - objects.Constraints.OrientationConstraint module.

Classes:
OrientationConstraint - Orientation Constraint.

"""

from constraint import Constraint


class OrientationConstraint(Constraint):
    """Orientation Constraint."""

    def __init__(self, name):
        super(OrientationConstraint, self).__init__(name)