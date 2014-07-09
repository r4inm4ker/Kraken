"""Kraken - objects.Constraints.BaseConstraint module.

Classes:
BaseConstraint - Base Constraint.

"""


class BaseConstraint(object):
    """Base Constraint object."""

    __kType__ = "Constraint"

    def __init__(self, name, constrainers, maintainOffset=False):
        """Initializes base constraint object.

        Arguments:
        name -- String, Name of the constraint.
        constrainers -- List, objects to act as constrainers.
        maintainOffset -- Boolean, to keep the offset from the constrainers or not.

        """

        super(BaseConstraint, self).__init__()
        assert type(constrainers) is list, "'constrainers' argument must be a list!"

        self.name = name
        self.constrainers = constrainers
        self.maintainOffset = maintainOffset
        self.definition = {
                           "name": self.name,
                           "constrainers": [],
                           "maintainOffset": self.maintainOffset
                          }