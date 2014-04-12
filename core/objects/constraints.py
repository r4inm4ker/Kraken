"""Kraken - objects.attributes module.

Classes:
Attribute - Base Attribute.
BoolAttribute - Boolean Attribute.
FloatAttribute - Float Attribute.
IntegerAttribute - Integer Attribute.
StringAttribute - String Attribute.

"""


class Constraint(object):
    """Base Constraint object."""

    def __init__(self, name, constraintType, constrainers, maintainOffset=False):
        """Initializes base constraint object.

        Arguments:
        name -- String, Name of the constraint.
        constraintType -- String, Type of constraint; see constraint object for types.
        constrainers -- List, objects to act as constrainers.
        maintainOffset -- Boolean, to keep the offset from the constrainers or not.

        """

        super(Constraint, self).__init__()
        self.name = name
        self.constraintType = constraintType
        self.constrainers = constrainers
        self.maintainOffset = maintainOffset


class ScaleConstraint(Constraint):
    """Scale Constraint."""

    def __init__(self, name, constraintType, constrainers, maintainOffset=False):
        super(ScaleConstraint, self).__init__(name, "scale", constrainers, maintainOffset=maintainOffset)
        assert type(constrainers) is list, "'constrainers' argument must be a list!"


class OrientationConstraint(Constraint):
    """Orientation Constraint."""

    def __init__(self, name, constraintType, constrainers, maintainOffset=False):
        super(OrientationConstraint, self).__init__(name, "orientation", constrainers, maintainOffset=maintainOffset)
        assert type(constrainers) is list, "'constrainers' argument must be a list!"


class PositionConstraint(Constraint):
    """Position Constraint."""

    def __init__(self, name, constraintType, constrainers, maintainOffset=False):
        super(PositionConstraint, self).__init__(name, "position", constrainers, maintainOffset=maintainOffset)
        assert type(constrainers) is list, "'constrainers' argument must be a list!"


class PoseConstraint(Constraint):
    """Pose Constraint."""

    def __init__(self, name, constraintType, constrainers, maintainOffset=False):
        super(PoseConstraint, self).__init__(name, "pose", constrainers, maintainOffset=maintainOffset)
        assert type(constrainers) is list, "'constrainers' argument must be a list!"