"""Kraken - objects.Constraints.ScaleConstraint module.

Classes:
ScaleConstraint - Scale Constraint.

"""

from constraint import Constraint


class ScaleConstraint(Constraint):
    """Scale Constraint."""

    def __init__(self, name):
        super(ScaleConstraint, self).__init__(name)