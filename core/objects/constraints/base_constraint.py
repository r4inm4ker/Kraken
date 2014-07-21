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


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        """Returns the paret of this attribute.

        Return:
        Parent object of this attribute.

        """

        return self.parent


    def setParent(self, parent):
        """Sets the paret of this attribute.

        Arguments:
        parent -- Object, parent object of this attribute.

        Return:
        True if successful.

        """

        self.parent = parent

        return True


    # ===================
    # Constraint Methods
    # ===================
    def getMaintainOffset(self):
        """Returns the whether the constraint should maintain offset when it's
        built or not.

        Return:
        Boolean, whether the constraint should maintain offset or not.

        """

        return self.maintainOffset


    def setMaintainOffset(self, value):
        """Sets the constraint to maintain offset when creating the constraint.

        Arguments:
        value -- Boolean, whether the constraint should maintain offset or not.

        Return:
        True if successful.

        """

        self.maintainOffset = value


    def setConstrainee(self, constrainee):
        """Sets the constrainee object for this constraint.
        
        Arguments:
        constrainee -- Object, kSceneItem that will be constrained.
        
        Return:
        True if successful.
        
        """

        self.constrainee = constrainee

        return True


    def getConstrainee(self):
        """Returns the constrainee object for this constraint.
        
        Return:
        True if successful.
        
        """

        return self.constrainee


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


    def getConstrainers(self):
        """Returns the constrainers of this constraint.

        Return:
        List, constrainer objects.

        """

        return self.constrainers


    # ==============
    # kType Methods
    # ==============
    def getKType(self):
        """Returns the kType of this object.

        Return:
        True if successful.

        """

        return self.__kType__