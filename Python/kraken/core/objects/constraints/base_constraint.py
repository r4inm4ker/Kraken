"""Kraken - objects.Constraints.BaseConstraint module.

Classes:
BaseConstraint - Base Constraint.

"""

from kraken.core.objects.scene_item import SceneItem


class BaseConstraint(object):
    """Base Constraint object."""

    def __init__(self, name):
        super(BaseConstraint, self).__init__()

        self.name = name
        self.constrainee = None
        self.constrainers = []
        self.maintainOffset = False

    # ==============
    # Type Methods
    # ==============
    def getTypeName(self):
        """Returns the class name of this object.

        Return:
        True if successful.

        """

        return self.__class__.__name___

    def getTypeHierarchyNames(self):
        """Returns the class name of this object.

        Return:
        True if successful.

        """
        khierarchy = []
        for cls in type.mro(type(self)):
            if cls == object:
                break;
            khierarchy.append(cls.__class__.__name___)
        return khierarchy

    # =============
    # Name Methods
    # =============
    def getName(self):
        """Returns the name of the attribute.

        Return:
        String of the name of the attribute.

        """

        return self.name


    def getFullName(self):
        """Returns the full hierarchical path to this object.

        Return:
        String, full name of the object.

        """

        return self.getName()

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


    # ================
    # Persistence Methods
    # ================
    def jsonEncode(self, saver):
        """Returns the data for this object encoded as a JSON hierarchy.

        Arguments:

        Return:
        A JSON structure containing the data for this SceneItem.

        """

        classHierarchy = []
        for cls in type.mro(type(self)):
            if cls == object:
                break;
            classHierarchy.append(cls.__name__)

        jsonData = {
            '__typeHierarchy__': classHierarchy,
            'name': self.name,
            'constrainee': self.constrainee.getName(),
            'constrainers': []
        }
        for cnstrnr in self.constrainers:
            jsonData['constrainers'].append(cnstrnr.getName())

        return jsonData


    def jsonDecode(self, loader, jsonData):
        """Returns the color of the object.

        Return:
        True if decoding was successful

        """

        loader.registerConstructionCallback(jsonData['constrainee'], self.setConstrainee)

        for cnstrnr in jsonData['constrainers']:
            loader.registerConstructionCallback(cnstrnr, self.addConstrainer)

        return True
