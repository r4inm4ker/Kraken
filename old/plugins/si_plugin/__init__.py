from kraken.kraken_si.utils import *


class Scene(object):
    """Softimage Scene Root."""

    def __init__(self, app="si"):
        super(Scene, self).__init__()
        self.app = app
        self.object3D = si.ActiveProject3.ActiveScene.Root


    def __str__(self):
        return str("Kraken Scene: " + self.object3D.Name)


class Dispatcher(object):
    """Softimage Dispatcher"""

    def __init__(self, cls):
        super(Dispatcher, self).__init__()
        self.cls = cls


    def _checkParent(self):
        """Check if parent is set, if not set to scene root."""

        if self.cls.parent is None:
            self.cls.parent = Scene()

        return

    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations.

        Return:
        True if successful.

        """

        self._checkParent()

        return


    def _build(self, kObject):
        """Builds element definition.

        Implement in sub-classes.

        Return:
        definition of the element.

        """

        if self.cls.__kType__ == "Null":
            kObject.object3D = kObject.parent.object3D.AddNull(kObject.name)

        return True


    def build(self):
        """Method sequence to build the element's desription.

        Return:
        self.definition

        """

        self._preBuild()
        self._build(self.cls)
        self._postBuild()

        return self.cls.object3D


    def _postBuild(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        # self._initTransform()
        # self._setObjName()
        # self._setVisibility()
        # self._setDisplay()
        # self._buildAttributes()
        # self._buildConstraints()

        for eachChild in self.cls.children:
            self._build(self.cls.children[eachChild])
            # self.cls.children[eachChild].build()

        return