"""Kraken - objects.Constraints.PoseConstraint module.

Classes:
PoseConstraint - Pose Constraint.

"""

from constraint import Constraint


class PoseConstraint(Constraint):
    """Pose Constraint."""

    def __init__(self, name):
        super(PoseConstraint, self).__init__(name)