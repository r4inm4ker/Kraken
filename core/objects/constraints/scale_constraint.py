"""Kraken - objects.Constraints.ScaleConstraint module.

Classes:
ScaleConstraint - Scale Constraint.

"""

from base_constraint import BaseConstraint


class ScaleConstraint(BaseConstraint):
    """Scale Constraint."""

    def __init__(self, name, constrainers, maintainOffset=False):
        super(ScaleConstraint, self).__init__(name, constrainers, maintainOffset=maintainOffset)