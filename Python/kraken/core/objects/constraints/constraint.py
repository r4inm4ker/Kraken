"""Kraken - objects.Constraints.Constraint module.

Classes:
Constraint - Base Constraint.

"""

from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.object_3d import Object3D


class Constraint(SceneItem):
    """Constraint object."""

    def __init__(self, name, parent=None):
        super(Constraint, self).__init__(name, parent)

        self._constrainee = None
        self._constrainers = []
        self._maintainOffset = False


    # ===================
    # Constraint Methods
    # ===================
    def getMaintainOffset(self):
        """Returns the whether the constraint should maintain offset when it's
        built or not.

        Return:
        Boolean, whether the constraint should maintain offset or not.

        """

        return self._maintainOffset


    def setMaintainOffset(self, value):
        """Sets the constraint to maintain offset when creating the constraint.

        Arguments:
        value -- Boolean, whether the constraint should maintain offset or not.

        Return:
        True if successful.

        """

        self._maintainOffset = value


    def setConstrainee(self, constrainee):
        """Sets the constrainee object for this constraint.

        Arguments:
        constrainee -- Object, kSceneItem that will be constrained.

        Return:
        True if successful.

        """

        self._constrainee = constrainee

        return True


    def getConstrainee(self):
        """Returns the constrainee object for this constraint.

        Return:
        True if successful.

        """

        return self._constrainee


    def addConstrainer(self, kObject3D):
        """Adds a constrainer object to this constraint.

        Arguments:
        kObject3D -- Object, kObject3D that will constrain the constrainee.

        Return:
        True if successful.

        """

        self._constrainers.append(None)
        self.setConstrainer(kObject3D, len(self._constrainers) - 1)

        return True


    def setConstrainer(self, kObject3D, index=0):
        """Sets the constrainer at the specified index.

        Arguments:
        kObject3D -- kObject3D, Kraken 3D object.
        index -- Integer, index of the constraint to set.

        Return:
        True if successful.

        """

        if not isinstance(kObject3D, Object3D):
            raise Exception("'kObject3D' argument is not a valid instance type. '"
                             + kObject3D.getName() + "': " + type(kObject3D) +
                             ". Must be an instance of 'Object3D'.")

        if kObject3D in self._constrainers:
            raise Exception("'kObject3D' argument is already a constrainer: '" + kObject3D.getName() + "'.")

        self._constrainers[index] = kObject3D

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

        return self._constrainers


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
            'constrainee': self._constrainee.getName(),
            'constrainers': []
        }
        for cnstrnr in self._constrainers:
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
