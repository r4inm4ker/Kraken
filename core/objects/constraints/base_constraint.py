"""Kraken - objects.Constraints.BaseConstraint module.

Classes:
BaseConstraint - Base Constraint.

"""

from kraken.core.objects.scene_item import SceneItem


class BaseConstraint(object):
    """Base Constraint object."""

    __kType__ = "BaseConstraint"

    def __init__(self, name):
        super(BaseConstraint, self).__init__()
        assert type(constrainers) is list, "'constrainers' argument must be a list!"

        self.name = name
        self.constrainee = None
        self.constrainers = []
        self.maintainOffset = False


    # =============
    # Name Methods
    # =============
    def getName(self):
        """Returns the name of the attribute.

        Return:
        String of the name of the attribute.

        """

        return self.name


    # ===================
    # Constraint Methods
    # ===================
    def addConstrainer(self, kSceneItem):
        """Adds a constrainer object to this constraint.

        Arguments:
        kSceneItem -- Object, kSceneItem that will constrain the constrainee.

        Return:
        True if successful.

        """

        if not isinstance(kSceneItem, SceneItem):
            raise Exception("'kSceneItem' argument is not a valid instance type. '"
                             + kSceneItem.getName() + "': " + type(kSceneItem) +
                             ". Must be an instance of 'SceneItem'.")

        if kSceneItem in self.constrainers:
            raise Exception("'kSceneItem' argument is already a constrainer: '" + kSceneItem.getName() + "'.")

        self.constrainers.append(kSceneItem)

        return True


    def removeConstrainerByIndex(self, index):
        """Removes a constrainer object by its index.

        Arguments:
        index -- Integer, index of the constrainer you want to remove.

        Return:
        True if successful.

        """

        return True


    # ==============
    # kType Methods
    # ==============
    def getKType(self):
        """Returns the kType of this object.

        Return:
        True if successful.

        """

        return self.__kType__