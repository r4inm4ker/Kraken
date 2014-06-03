"""Kraken - objects.elements module.

Classes:
SceneObject -- Scene root representation.
Group -- Object used to group objects together.
Null -- Basic 3d transform with basic graphical representation.
Control -- Controller objects for transforming objects.
Joint -- Joint objects which are used for skinning / deformation.
Chain -- Bone chain object consists of Joint objects.

"""

from kraken.core.objects import interfaces
from kraken.core.objects import attributes
from kraken.core.objects import constraints


class SceneObject(interfaces.AttributeInterface,
                  interfaces.ChildInterface,
                  interfaces.ConstraintInterface,
                  interfaces.DisplayInterface,
                  interfaces.JSONInterface,
                  interfaces.NameInterface,
                  interfaces.TransformInterface,
                  interfaces.BuildInterface):
    """Scene object representation. All elements sub-class off this."""

    __kType__ = "SceneObject"

    def __init__(self, name, parent=None):
        """Initializes base scene object.

        Arguments:
        name -- String, Name of model object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(SceneObject, self).__init__()
        self.name = name
        self.parent = parent
        self.layer = None


    def __repr__(self):
        return 'Kraken %s: %s' % (self.__kType__, self.name)


class Group(SceneObject):
    """Group / locator object."""

    __kType__ = "Group"

    def __init__(self, name, parent=None):
        """Initializes Group object.

        Arguments:
        name -- String, Name of model object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(Group, self).__init__(name, parent=parent)


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Group, self)._preBuild()

        return True


    def build(self):
        """Build element's definition."""

        self._preBuild()
        self._build()
        self._postBuild()

        return self.definition


    def _postBuild(self):
        """Post-build operations."""

        super(Group, self)._postBuild()

        return True


class Null(SceneObject):
    """Null / locator object."""

    __kType__ = "Null"

    def __init__(self, name, parent=None):
        """Initializes Null object.

        Arguments:
        name -- String, Name of model object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(Null, self).__init__(name, parent=parent)


class Control(SceneObject):
    """Control object."""

    __kType__ = "Control"

    shapes = {
                "arrows":
                            [
                                [-0.1, -0.3, 0.0],
                                [-0.1, -0.1, 0.0],
                                [-0.3, -0.1, 0.0],
                                [-0.3, -0.2, 0.0],
                                [-0.5, 0.0, 0.0],
                                [-0.3, 0.2, 0.0],
                                [-0.3, 0.1, 0.0],
                                [-0.1, 0.1, 0.0],
                                [-0.1, 0.3, 0.0],
                                [-0.2, 0.3, 0.0],
                                [0.0, 0.5, 0.0],
                                [0.2, 0.3, 0.0],
                                [0.1, 0.3, 0.0],
                                [0.1, 0.1, 0.0],
                                [0.3, 0.1, 0.0],
                                [0.3, 0.2, 0.0],
                                [0.5, 0.0, 0.0],
                                [0.3, -0.2, 0.0],
                                [0.3, -0.1, 0.0],
                                [0.1, -0.1, 0.0],
                                [0.1, -0.3, 0.0],
                                [0.2, -0.3, 0.0],
                                [0.0, -0.5, 0.0],
                                [-0.2, -0.3, 0.0],
                                [-0.1, -0.3, 0.0]
                            ],
                "circle":
                            [
                                [-0.3512, -0.3512, 0.0],
                                [-0.4966, 0.0, 0.0],
                                [-0.3512, 0.3512, 0.0],
                                [0.0, 0.4966, -17.4068],
                                [0.3512, 0.3512, 0.0],
                                [0.4966, 0.0, 0.0],
                                [0.3512, -0.3512, 0.0],
                                [0.0, -0.4966, 0.0],
                                [-0.3512, -0.3512, 0.0]
                            ],
                "circleDouble":
                            [
                                [0.3512, -0.3512, 0.0],
                                [0.4966, 0.0, 0.0],
                                [0.3512, 0.3512, 0.0],
                                [0.0, 0.4966, 0.0],
                                [-0.3512, 0.3512, 0.0],
                                [-0.4966, 0.0, 0.0],
                                [-0.3512, -0.3512, 0.0],
                                [0.0, -0.4966, 0.0],
                                [0.3512, -0.3512, 0.0],
                                [0.3233, -0.3233, 0.0],
                                [0.4571, 0.0, 0.0],
                                [0.3233, 0.3233, 0.0],
                                [0.0, 0.4571, 0.0],
                                [-0.3233, 0.3233, 0.0],
                                [-0.4571, 0.0, 0.0],
                                [-0.3233, -0.3233, 0.0],
                                [0.0, -0.4571, 0.0],
                                [0.3233, -0.3233, 0.0]
                            ],
                "circleHalf":
                            [
                                [0.0, 0.4965, 0.0],
                                [0.3511, 0.3511, 0.0],
                                [0.4965, 0.0, 0.0],
                                [0.3511, -0.3511, 0.0],
                                [0.0, -0.4965, 0.0]
                            ],
                "cube":
                            [
                                [-0.5, 0.5, -0.5],
                                [-0.5, 0.5, 0.5],
                                [0.5, 0.5, 0.5],
                                [0.5, 0.5, -0.5],
                                [-0.5, 0.5, -0.5],
                                [-0.5, -0.5, -0.5],
                                [-0.5, -0.5, 0.5],
                                [0.5, -0.5, 0.5],
                                [0.5, -0.5, -0.5],
                                [-0.5, -0.5, -0.5],
                                [-0.5, -0.5, 0.5],
                                [-0.5, 0.5, 0.5],
                                [0.5, 0.5, 0.5],
                                [0.5, -0.5, 0.5],
                                [0.5, -0.5, -0.5],
                                [0.5, 0.5, -0.5]
                            ],
                "cubeXAligned":
                            [
                                [0.0, 0.5, -0.5],
                                [0.0, 0.5, 0.5],
                                [1.0, 0.5, 0.5],
                                [1.0, 0.5, -0.5],
                                [0.0, 0.5, -0.5],
                                [0.0, -0.5, -0.5],
                                [0.0, -0.5, 0.5],
                                [1.0, -0.5, 0.5],
                                [1.0, -0.5, -0.5],
                                [0.0, -0.5, -0.5],
                                [0.0, -0.5, 0.5],
                                [0.0, 0.5, 0.5],
                                [1.0, 0.5, 0.5],
                                [1.0, -0.5, 0.5],
                                [1.0, -0.5, -0.5],
                                [1.0, 0.5, -0.5]
                            ],
                "line":
                            [
                                [0.0, 0.0, 0.0],
                                [1.0, 0.0, 0.0]
                            ],
                "pin":
                            [
                                [0.0, 0.0, 0.602],
                                [-0.1406, 0.0, 0.6603],
                                [-0.1989, 0.0, 0.8009],
                                [-0.1406, 0.0, 0.9415],
                                [0.0, 0.0, 0.9998],
                                [0.1406, 0.0, 0.9415],
                                [0.1989, 0.0, 0.8009],
                                [0.1406, 0.0, 0.6603],
                                [0.0, 0.0, 0.602],
                                [0.0, 0.0, 0.0]
                            ],
                "rotate":
                            [
                                [-0.4105, 0.3472, -0.1844],
                                [-0.5008, 0.2001, 0.0],
                                [-0.4105, 0.3472, 0.1844],
                                [-0.4105, 0.3472, 0.0965],
                                [-0.2462, 0.4636, 0.0965],
                                [0.0, 0.5212, 0.0965],
                                [0.2462, 0.4636, 0.0965],
                                [0.4105, 0.3472, 0.0965],
                                [0.4105, 0.3472, 0.1844],
                                [0.5008, 0.2001, 0.0],
                                [0.4105, 0.3472, -0.1844],
                                [0.4105, 0.3472, 0.0965],
                                [0.2462, 0.4636, 0.0965],
                                [0.0, 0.5212, 0.0965],
                                [-0.2462, 0.4636, 0.0965],
                                [-0.4105, 0.3472, 0.0965],
                                [-0.4105, 0.3472, -0.1844]
                            ],
                "sphere":
                            [
                                [0.0, 0.0, -0.498],
                                [-0.3522, 0.0, -0.3522],
                                [-0.498, 0.0, 0.0],
                                [-0.3522, 0.0, 0.3522],
                                [0.0, 0.0, 0.498],
                                [0.3522, 0.0, 0.3522],
                                [0.498, 0.0, 0.0],
                                [0.3522, 0.0, -0.3522],
                                [0.0, 0.0, -0.498],
                                [0.0, 0.3522, -0.3522],
                                [0.0, 0.498, 0.0],
                                [0.0, 0.3522, 0.3522],
                                [0.0, 0.0, 0.498],
                                [0.0, -0.3522, 0.3522],
                                [0.0, -0.498, 0.0],
                                [0.0, -0.3522, -0.3522],
                                [0.0, 0.0, -0.498],
                                [-0.3522, 0.0, -0.3522],
                                [-0.498, 0.0, 0.0],
                                [-0.3522, 0.3522, 0.0],
                                [0.0, 0.498, 0.0],
                                [0.3522, 0.3522, 0.0],
                                [0.498, 0.0, 0.0],
                                [0.3522, -0.3522, 0.0],
                                [0.0, -0.498, 0.0],
                                [-0.3522, -0.3522, 0.0],
                                [-0.498, 0.0, 0.0]
                            ],
                "square":
                            [
                                [0.5, 0.0, -0.5],
                                [0.5, 0.0, 0.5],
                                [-0.5, 0.0, 0.5],
                                [-0.5, 0.0, -0.5],
                                [0.5, 0.0, -0.5]
                            ],
                "squareXAligned":
                            [
                                [1.0, 0.0, -0.5],
                                [1.0, 0.0, 0.5],
                                [0.0, 0.0, 0.5],
                                [0.0, 0.0, -0.5],
                                [1.0, 0.0, -0.5]
                            ],
                "triangle":
                            [
                                [1.0, 0.0, 0.0],
                                [0.0, 0.0, -0.5],
                                [0.0, 0.0, 0.5],
                                [1.0, 0.0, 0.0]
                            ],
            }


    def __init__(self, name, shape, parent=None):
        """Initializes Control object.

        Arguments:
        name -- String, Name of model object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(Control, self).__init__(name, parent=parent)
        self.shape = shape
        self.sclOffset = [1,1,1]
        self.rotOffset = [0,0,0]
        self.posOffset = [0,0,0]


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Control, self)._preBuild()

        return True


    def build(self):
        """Build element's definition."""

        self._preBuild()
        self._build()
        self._postBuild()

        return self.definition


    def _postBuild(self):
        """Post-build operations."""

        super(Control, self)._postBuild()

        return True


class Chain(SceneObject):
    """Joint Chain object."""

    __kType__ = "Chain"

    def __init__(self, name, positions, parent=None):
        """Initializes Chain object.

        Arguments:
        name -- String, Name of model object.
        positions -- List, List of [x,y,z] values of joint positions.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(Chain, self).__init__(name, parent=parent)
        self.positions = positions


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Chain, self)._preBuild()

        return True


    def build(self):
        """Build element's definition."""

        self._preBuild()
        self._build()
        self._postBuild()

        return self.definition


    def _postBuild(self):
        """Post-build operations."""

        super(Chain, self)._postBuild()

        return True


class Joint(SceneObject):
    """Joint Joint object."""

    __kType__ = "Joint"

    def __init__(self, name, parent=None):
        """Initializes Joint object.

        Arguments:
        name -- String, Name of model object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(Joint, self).__init__(name, parent=parent)


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Joint, self)._preBuild()

        return True


    def build(self):
        """Build element's definition."""

        self._preBuild()
        self._build()
        self._postBuild()

        return self.definition


    def _postBuild(self):
        """Post-build operations."""

        super(Joint, self)._postBuild()

        return True