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

    __kType__ = "Constraint"

    def __init__(self, name, constrainers, maintainOffset=False):
        """Initializes base constraint object.

        Arguments:
        name -- String, Name of the constraint.
        constrainers -- List, objects to act as constrainers.
        maintainOffset -- Boolean, to keep the offset from the constrainers or not.

        """

        super(Constraint, self).__init__()
        self.name = name
        self.constrainers = constrainers
        self.maintainOffset = maintainOffset
        self.definition = {
                           "name":self.name,
                           "constrainers":[],
                           "maintainOffset":self.maintainOffset
                          }


    def buildDef(self):
        """Builds the object's definition and stores to definition attribute.

        Return:
        Dictionary of object data.
        """

        for eachConstrainer in self.constrainers:
            self.definition["constrainers"].append(eachConstrainer.name)

        return self.definition


class ScaleConstraint(Constraint):
    """Scale Constraint."""

    __kType__ = "ScaleConstraint"

    def __init__(self, name, constrainers, maintainOffset=False):
        super(ScaleConstraint, self).__init__(name, constrainers, maintainOffset=maintainOffset)
        assert type(constrainers) is list, "'constrainers' argument must be a list!"


class OrientationConstraint(Constraint):
    """Orientation Constraint."""

    __kType__ = "OrientationConstraint"

    def __init__(self, name, constrainers, maintainOffset=False):
        super(OrientationConstraint, self).__init__(name, constrainers, maintainOffset=maintainOffset)
        assert type(constrainers) is list, "'constrainers' argument must be a list!"


class PositionConstraint(Constraint):
    """Position Constraint."""

    __kType__ = "PositionConstraint"

    def __init__(self, name, constrainers, maintainOffset=False):
        super(PositionConstraint, self).__init__(name, constrainers, maintainOffset=maintainOffset)
        assert type(constrainers) is list, "'constrainers' argument must be a list!"


class PoseConstraint(Constraint):
    """Pose Constraint."""

    __kType__ = "PoseConstraint"

    def __init__(self, name, constrainers, maintainOffset=False):
        super(PoseConstraint, self).__init__(name, constrainers, maintainOffset=maintainOffset)
        assert type(constrainers) is list, "'constrainers' argument must be a list!"