"""Kraken - objects.Controls.Control module.

Classes:
Control - Base Control.

"""

from kraken.core.configs.config import Config
from kraken.core.maths import Euler, Quat, Vec3, Xfo
from kraken.core.maths import Math_degToRad
from kraken.core.objects.curve import Curve


class Control(Curve):
    """Base Control object."""

    def __init__(self, name, parent=None, shape="null"):
        """Initializes control object.

        Args:
            name (str): Name of the constraint.
            parent (Object): Parent object of this object.

        """

        super(Control, self).__init__(name, parent=parent)

        config = Config.getInstance()
        configShapes = config.getControlShapes()
        if shape not in configShapes.keys():
            raise KeyError("'" + shape + "' is not a valid shape in the loaded config.")

        self.setCurveData(configShapes[shape])


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
