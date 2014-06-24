"""Kraken - objects.Constraints.OrientationConstraint module.

Classes:
OrientationConstraint - Orientation Constraint.

"""

import BaseConstraint


class OrientationConstraint(BaseConstraint):
    """Orientation Constraint."""

    def __init__(self, name, constrainers, maintainOffset=False):
        super(OrientationConstraint, self).__init__(name, constrainers, maintainOffset=maintainOffset)