"""Kraken - objects.Constraints.PoseConstraint module.

Classes:
PoseConstraint - Pose Constraint.

"""

from base_constraint import BaseConstraint


class PoseConstraint(BaseConstraint):
    """Pose Constraint."""

    __kType__ = "PoseConstraint"

    def __init__(self, name):
        super(PoseConstraint, self).__init__(name)