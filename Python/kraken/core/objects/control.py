"""Kraken - objects.Controls.Control module.

Classes:
Control - Base Control.

"""

from kraken.core.configs.config import Config
from kraken.core.maths import AXIS_NAME_TO_TUPLE_MAP, Euler, Quat, Vec3, Xfo
from kraken.core.maths import Math_degToRad
from kraken.core.objects.curve import Curve
from kraken.core.objects.ctrlSpace import CtrlSpace


class Control(Curve):
    """Base Control object."""

    def __init__(self, name, parent=None, shape="null"):
        """Initializes control object.

        Args:
            name (str): Name of the constraint.
            parent (Object): Parent object of this object.

        """

        super(Control, self).__init__(name, parent=parent)
        self.shape = shape

        self.setShape(shape)

    # ==============
    # Shape Methods
    # ==============
    def getShape(self):
        """Returns the shape that the control was set to.

        Returns:
            str: Name of the shape that was set.

        """

        return self.shape

    def setShape(self, shape):
        """Sets the shape of the control to the one specified.

        Args:
            shape (str): the desired shape of the control.

        Returns:
            bool: True if successful.

        """

        config = Config.getInstance()
        configShapes = config.getControlShapes()
        if shape not in configShapes.keys():
            raise KeyError("'" + shape + "' is not a valid shape in the loaded config of class [" + config.__class__.__name__ + "]")

        self.setCurveData(configShapes[shape])

        return True


    # ==============
    # Align Methods
    # ==============
    def alignOnXAxis(self, negative=False):
        """Aligns the control shape on the X axis.

        Args:
            negative (bool): Whether to align the control on the negative X axis.

        Returns:
            bool: True if successful.

        """

        furthest = 0.0

        curveData = list(self.getCurveData())

        for eachSubCurve in curveData:
            for eachPoint in eachSubCurve["points"]:

                if negative is False:

                    if eachPoint[0] < furthest:
                        furthest = eachPoint[0]

                else:

                    if eachPoint[0] > furthest:
                        furthest = eachPoint[0]


        offset = 0.0 - furthest

        for eachSubCurve in curveData:
            for eachPoint in eachSubCurve["points"]:
                eachPoint[0] += offset

        self.setCurveData(curveData)

        return True

    def alignOnYAxis(self, negative=False):
        """Aligns the control shape on the Y axis.

        Args:
            negative (bool): Whether to align the control on the negative Y axis.

        Returns:
            bool: True if successful.

        """

        furthest = 0.0

        curveData = list(self.getCurveData())

        for eachSubCurve in curveData:
            for eachPoint in eachSubCurve["points"]:

                if negative is False:

                    if eachPoint[1] < furthest:
                        furthest = eachPoint[1]

                else:

                    if eachPoint[1] > furthest:
                        furthest = eachPoint[1]

        offset = 0.0 - furthest

        for eachSubCurve in curveData:
            for eachPoint in eachSubCurve["points"]:
                eachPoint[1] += offset

        self.setCurveData(curveData)

        return True

    def alignOnZAxis(self, negative=False):
        """Aligns the control shape on the Z axis.

        Args:
            negative (bool): Whether to align the control on the negative Z axis.

        Returns:
            bool: True if successful.

        """

        furthest = 0.0

        curveData = list(self.getCurveData())

        for eachSubCurve in curveData:
            for eachPoint in eachSubCurve["points"]:

                if negative is False:

                    if eachPoint[2] < furthest:
                        furthest = eachPoint[2]

                else:

                    if eachPoint[2] > furthest:
                        furthest = eachPoint[2]

        offset = 0.0 - furthest

        for eachSubCurve in curveData:
            for eachPoint in eachSubCurve["points"]:
                eachPoint[2] += offset

        self.setCurveData(curveData)

        return True


    # ==============
    # Scale Methods
    # ==============
    def scalePointsOnAxis(self, scale, scaleAxis="POSX"):
        """Scales the point positions from it's center along the given axis only.

        Args:
            scale: scale value to apply to the points.
            scaleAxis: which axes to scale and by what direction

        Returns:
            bool: True if successful.

        """

        # would be great if vec3 was iterable
        axis = AXIS_NAME_TO_TUPLE_MAP.get(scaleAxis)

        if axis is None:
            raise KeyError("'" + scaleAxis + "' is not a valid axis. Valid axes are: " + ','.join(AXIS_NAME_TO_TUPLE_MAP.keys()))

        scaleList = [1.0, 1.0, 1.0]
        for i, x in enumerate(axis):
            if x != 0:
                scaleList[i] = scale * axis[i]

        return self.scalePoints(Vec3(scaleList[0], scaleList[1], scaleList[2]))


    # ==============
    # Scale Methods
    # ==============
    def scalePoints(self, scaleVec):
        """Scales the point positions from it's center.

        Args:
            scaleVec (Vec3): scale value to apply to the points.

        Returns:
            bool: True if successful.

        """

        curveData = list(self.getCurveData())

        for eachSubCurve in curveData:
            for eachPoint in eachSubCurve["points"]:
                eachPoint[0] *= scaleVec.x
                eachPoint[1] *= scaleVec.y
                eachPoint[2] *= scaleVec.z

        self.setCurveData(curveData)

        return True


    # ===============
    # Rotate Methods
    # ===============
    def rotatePoints(self, xRot, yRot, zRot):
        """Rotates the points by the input values.

        Args:
            xRot (float): Euler x rotate value.
            yRot (float): Euler y rotate value.
            zRot (float): Euler z rotate value.

        Returns:
            bool: True if successful.

        """

        curveData = list(self.getCurveData())

        quatRot = Quat()
        quatRot.setFromEuler(Euler(Math_degToRad(xRot), Math_degToRad(yRot),
                                   Math_degToRad(zRot)))

        newPoints = []
        for eachSubCurve in curveData:

            for eachPoint in eachSubCurve["points"]:
                pointVec = Vec3(eachPoint[0], eachPoint[1], eachPoint[2])
                rotVec = quatRot.rotateVector(pointVec)
                eachPoint[0] = rotVec.x
                eachPoint[1] = rotVec.y
                eachPoint[2] = rotVec.z

        self.setCurveData(curveData)

        return True


    # ==================
    # Translate Methods
    # ==================
    def translatePoints(self, translateVec):
        """Translates the control points.

        Args:
            translateVec (Vec3): Translation values to apply to the points.

        Returns:
            bool: True if successful.

        """

        curveData = list(self.getCurveData())

        for eachSubCurve in curveData:
            for eachPoint in eachSubCurve["points"]:
                eachPoint[0] += translateVec.x
                eachPoint[1] += translateVec.y
                eachPoint[2] += translateVec.z

        self.setCurveData(curveData)

        return True


    # ===============
    # Helper Methods
    # ===============
    def insertCtrlSpace(self, name=None):
        """Adds a CtrlSpace object above this object

        Args:
            name (string): optional name for this CtrlSpace, default is same as this object

        Returns:
            object: New CtrlSpace object

        """

        if name is None:
            name = self.getName()

        newCtrlSpace = CtrlSpace(name, parent=self.getParent())
        if self.getParent() is not None:
            self.getParent().removeChild(self)

        self.setParent(newCtrlSpace)
        newCtrlSpace.addChild(self)

        newCtrlSpace.xfo = Xfo(self.xfo)

        return newCtrlSpace