"""Kraken - objects.Constraints.ScaleConstraint module.

Classes:
ScaleConstraint - Scale Constraint.

"""

from base_constraint import BaseConstraint


class ScaleConstraint(BaseConstraint):
    """Scale Constraint."""

    def __init__(self, name):
        super(ScaleConstraint, self).__init__(name)